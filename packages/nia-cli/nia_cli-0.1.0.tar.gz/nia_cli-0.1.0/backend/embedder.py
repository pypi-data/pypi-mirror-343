import asyncio
import json
import logging
import os
import time
from abc import ABC, abstractmethod
from collections import Counter, deque
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import AsyncGenerator, Dict, Generator, List, Optional, Tuple, Any, Deque
import aiohttp
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)
from tqdm import tqdm
from openai import OpenAI, AsyncOpenAI, RateLimitError
import aiohttp
from asyncio import Semaphore
from dataclasses import dataclass, field
from pathlib import Path

from chunker import Chunk, Chunker
from constants import TEXT_FIELD
from data_manager import DataManager

Vector = Tuple[Dict, List[float]]  # (metadata, embedding)

# --------------------------------------
# ADJUST concurrency to avoid short-term bursts
# --------------------------------------
MAX_CONCURRENT_EMBEDDINGS = 4

# Batching & Buffer
CHUNK_QUEUE_SIZE = 50
MAX_BATCH_SIZE = 150
RESULTS_BUFFER_SIZE = 200

@dataclass
class TokenRateTracker:
    """Tracks token usage over a rolling time window."""
    max_tokens_per_minute: int = 1_000_000
    window_seconds: int = 60
    usage_window: Deque[Tuple[float, int]] = field(default_factory=deque)
    
    def add_usage(self, tokens: int) -> None:
        """Record token usage at current time."""
        now = time.time()
        self.usage_window.append((now, tokens))
        self._clear_old_entries(now)
    
    def _clear_old_entries(self, current_time: float) -> None:
        """Remove entries older than window_seconds."""
        while self.usage_window and (current_time - self.usage_window[0][0]) > self.window_seconds:
            self.usage_window.popleft()
    
    async def wait_if_needed(self, planned_tokens: int) -> None:
        """Wait if adding planned_tokens would exceed the rate limit."""
        while True:
            now = time.time()
            self._clear_old_entries(now)
            
            current_usage = sum(tokens for _, tokens in self.usage_window)
            if current_usage + planned_tokens <= self.max_tokens_per_minute:
                break
                
            # Sleep for a short interval and check again
            await asyncio.sleep(2)

def process_file(args: Tuple[str, Dict, Chunker]) -> List[Chunk]:
    """
    Process a single file, chunking it with the provided chunker.
    This runs in a ThreadPool to parallelize file processing.
    """
    try:
        content, metadata, chunker = args
        result = chunker.chunk(content, metadata)
        # Handle case where chunk might be returning a coroutine (async function)
        if hasattr(result, "__await__"):
            # We can't await in a synchronous function, so this is an error
            # but we'll return an empty list to avoid crashing the system
            logging.error(f"[process_file] Error chunking file {metadata.get('file_path', 'unknown')}: 'coroutine' object is not iterable")
            return []
        return result
    except Exception as e:
        logging.error(f"[process_file] Error chunking file {metadata.get('file_path')}: {e}", exc_info=True)
        return []


class BatchEmbedder(ABC):
    """Abstract class for batch embedding of a dataset."""

    @abstractmethod
    async def embed_dataset(self, chunks_per_batch: int, max_embedding_jobs: int = None):
        """Issues embedding calls for the entire dataset. Possibly chunked/batched in small sets."""

    @abstractmethod
    def embeddings_are_ready(self, jobs_file: str) -> bool:
        """Returns True if all the embeddings are ready."""

    @abstractmethod
    async def download_embeddings(self, metadata_file: str) -> AsyncGenerator[Vector, None]:
        """Yields (metadata, embedding) pairs from the metadata file."""


class OpenAIRealTimeEmbedder(BatchEmbedder):
    """
    Real-time embedding using async OpenAI API calls and parallel processing for chunking.
    """

    def __init__(
        self,
        data_manager: DataManager,
        chunker: Chunker,
        local_dir: str,
        embedding_model: str,
        embedding_size: int,
    ):
        self.data_manager = data_manager
        self.chunker = chunker
        self.local_dir = local_dir
        self.embedding_model = embedding_model
        self.embedding_size = embedding_size

        # Results management
        self._results: List[Vector] = []
        self._results_count = 0
        self.results_file = None
        self.results_file_path = None

        # Initialize the OpenAI clients
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Please set OPENAI_API_KEY in your environment.")
        self.client = OpenAI()         # not heavily used, but available
        self.async_client = AsyncOpenAI()

        # Concurrency semaphore
        self.semaphore = Semaphore(MAX_CONCURRENT_EMBEDDINGS)
        
        # Initialize token rate tracker
        self.token_tracker = TokenRateTracker()

        # Chunk queue for producer-consumer pattern
        self.chunk_queue = asyncio.Queue(maxsize=CHUNK_QUEUE_SIZE)

        # Counters for logging
        self.api_call_count = 0
        self.files_processed = 0
        self.chunks_produced = 0
        self.tokens_in_chunks = 0
        self.file_errors = 0

    def _initialize_results_file(self) -> None:
        """Initialize the results file with a unique timestamp."""
        if not self.results_file:
            timestamp = int(time.time())
            self.results_file_path = os.path.join(
                self.local_dir,
                f"{self.data_manager.dataset_id}_embeddings_{timestamp}.jsonl"
            )
            self.results_file = open(self.results_file_path, 'a')
            logging.info(f"[OpenAIRealTimeEmbedder] Initialized results file: {self.results_file_path}")

    def _write_results_to_disk(self) -> None:
        """
        Write current results buffer to disk and clear memory.
        """
        if not self.results_file:
            self._initialize_results_file()

        try:
            for metadata, embedding in self._results:
                json.dump({"metadata": metadata, "embedding": embedding}, self.results_file)
                self.results_file.write('\n')

            self.results_file.flush()
            buffer_count = len(self._results)
            self._results.clear()
            logging.debug(f"[OpenAIRealTimeEmbedder] Wrote {buffer_count} results to disk. "
                          f"Total processed so far: {self._results_count}")

        except Exception as e:
            logging.error(f"[OpenAIRealTimeEmbedder] Error writing results to disk: {e}", exc_info=True)
            raise

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
        retry=retry_if_exception_type(RateLimitError)
    )
    async def create_embeddings_with_backoff(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings with rate limiting using rolling window token counter.
        """
        # Estimate tokens (rough approximation)
        estimated_tokens = sum(len(text.split()) * 1.3 for text in texts)  # 1.3 multiplier for safety margin
        
        async with self.semaphore:
            # Wait if we would exceed token rate limit
            await self.token_tracker.wait_if_needed(int(estimated_tokens))
            
            self.api_call_count += 1
            logging.info(f"[OpenAIRealTimeEmbedder] Embedding API call #{self.api_call_count}, "
                         f"batch size: {len(texts)}")
            try:
                resp = await self.async_client.embeddings.create(
                    model=self.embedding_model,
                    input=texts
                )
                
                # -------------------------------------------------------
                # Fix: usage is top-level, not on individual embeddings:
                # -------------------------------------------------------
                actual_tokens = 0
                if getattr(resp, "usage", None) and hasattr(resp.usage, "total_tokens"):
                    actual_tokens = resp.usage.total_tokens

                self.token_tracker.add_usage(actual_tokens)
                return [item.embedding for item in resp.data]
            
            except Exception as e:
                logging.error(f"[OpenAIRealTimeEmbedder] Error in API call #{self.api_call_count}: {e}", exc_info=True)
                raise

    async def process_chunk_batch(self, batch: List[Chunk]) -> None:
        """
        Process a batch of chunks asynchronously with rate limiting.
        """
        if not batch:
            return

        # Split into sub-batches if needed
        sub_batches = [batch[i:i + MAX_BATCH_SIZE] for i in range(0, len(batch), MAX_BATCH_SIZE)]

        for sub_batch in sub_batches:
            text_buffer = [c.content for c in sub_batch]
            meta_buffer = [c.metadata for c in sub_batch]

            try:
                embeddings = await self.create_embeddings_with_backoff(text_buffer)
                for i, embedding in enumerate(embeddings):
                    chunk_metadata = meta_buffer[i]
                    self._results.append((chunk_metadata, embedding))
                    self._results_count += 1

                    # Write to disk if buffer is full
                    if len(self._results) >= RESULTS_BUFFER_SIZE:
                        self._write_results_to_disk()

            except Exception as e:
                # Log and skip this sub-batch, do not crash the entire indexing
                logging.error(f"[OpenAIRealTimeEmbedder] Error processing sub-batch: {str(e)}", exc_info=True)
                continue

    async def chunk_producer(self, file_paths: List[Dict]):
        """
        Produces chunks from files using parallel processing.
        `file_paths` is a list of dicts with { 'content': ..., 'metadata': ... }.
        We'll pass them to the chunker in a process pool.
        """
        try:
            chunk_args = []
            total_files = len(file_paths)

            for file_info in file_paths:
                content, metadata = file_info["content"], file_info["metadata"]
                chunk_args.append((content, metadata, self.chunker))

            # ThreadPoolExecutor is used for I/O-bound tasks (file processing)
            # Consider using ProcessPoolExecutor for CPU-bound tasks with Hatchet.run
            # Note: ProcessPoolExecutor requires all objects to be picklable
            with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
                for chunks in executor.map(process_file, chunk_args):
                    if chunks:
                        for ch in chunks:
                            self.chunks_produced += 1
                            self.tokens_in_chunks += ch.num_tokens
                            await self.chunk_queue.put(ch)
                    else:
                        self.file_errors += 1

                    self.files_processed += 1
                    logging.info(f"[chunk_producer] Files processed: {self.files_processed}, "
                                 f"Chunks produced so far: {self.chunks_produced}, "
                                 f"Total tokens so far: {self.tokens_in_chunks}")

            # Signal the consumer that we're done
            await self.chunk_queue.put(None)
        except Exception as e:
            logging.error(f"[chunk_producer] Error in producer: {e}")
            await self.chunk_queue.put(None)  # Signal consumer to stop
            raise

    async def embedding_consumer(self, chunks_per_batch: int) -> None:
        """
        Consumes chunks from the queue and creates embeddings in batches of up to `chunks_per_batch`.
        """
        current_batch = []

        while True:
            try:
                chunk = await self.chunk_queue.get()

                if chunk is None:
                    if current_batch:
                        await self.process_chunk_batch(current_batch)
                    break

                current_batch.append(chunk)

                if len(current_batch) >= chunks_per_batch:
                    await self.process_chunk_batch(current_batch)
                    current_batch = []

            except Exception as e:
                logging.error(f"[embedding_consumer] Error in consumer: {e}", exc_info=True)
                break
            finally:
                self.chunk_queue.task_done()

    async def embed_dataset(self, chunks_per_batch: int, max_embedding_jobs: int = None) -> str:
        """
        Processes the dataset using parallel chunking and async embedding.
        """
        chunks_per_batch = min(chunks_per_batch, MAX_BATCH_SIZE)

        self._results.clear()
        self._results_count = 0

        # Retrieve file info from the data_manager
        file_infos = []
        for content, metadata in self.data_manager.walk():
            file_infos.append({"content": content, "metadata": metadata})
        total_files = len(file_infos)
        logging.info(f"[embed_dataset] Starting chunking. Number of files to process: {total_files}")

        self._initialize_results_file()

        producer = asyncio.create_task(self.chunk_producer(file_infos))
        consumer = asyncio.create_task(self.embedding_consumer(chunks_per_batch))

        pbar = tqdm(total=total_files, desc="Processing files", unit="file")

        try:
            # Wait for producer + consumer to finish
            await asyncio.gather(producer, consumer)

            # Write any leftover results
            if self._results:
                self._write_results_to_disk()

        except Exception as e:
            logging.error(f"[embed_dataset] Error during embedding pipeline: {e}", exc_info=True)
            raise
        finally:
            pbar.close()
            if self.results_file:
                self.results_file.close()
                self.results_file = None

        logging.info("=== [embed_dataset] Finished embedding ===")
        logging.info(f"Files processed: {self.files_processed}")
        logging.info(f"File-level errors: {self.file_errors}")
        logging.info(f"Chunks produced: {self.chunks_produced}")
        logging.info(f"Total tokens in chunks: {self.tokens_in_chunks}")
        logging.info(f"Embedding API calls: {self.api_call_count}")
        logging.info(f"Embeddings stored: {self._results_count}")
        logging.info(f"Results file: {self.results_file_path}")

        return self.results_file_path

    def embeddings_are_ready(self, jobs_file: str) -> bool:
        """
        Returns True if all the embeddings are ready.
        """
        if not os.path.exists(jobs_file):
            return False
        try:
            with open(jobs_file, 'r') as f:
                first_line = f.readline()
                return bool(first_line and json.loads(first_line))
        except Exception as e:
            logging.error(f"[OpenAIRealTimeEmbedder] Error checking embeddings status: {e}", exc_info=True)
            return False

    async def download_embeddings(self, metadata_file: str) -> AsyncGenerator[Vector, None]:
        """
        Yields (metadata, embedding) pairs from the metadata file.
        """
        try:
            with open(metadata_file, 'r') as f:
                for line in f:
                    try:
                        item = json.loads(line)
                        yield (item["metadata"], item["embedding"])
                    except json.JSONDecodeError as e:
                        logging.error(f"[OpenAIRealTimeEmbedder] JSON decode error in line: {e}", exc_info=True)
                        continue
        except Exception as e:
            logging.error(f"[OpenAIRealTimeEmbedder] Error downloading embeddings: {e}", exc_info=True)
            return


# -----------------------------------------------------------------------------
# The function that was missing: build_batch_embedder_from_flags
# -----------------------------------------------------------------------------
def build_batch_embedder_from_flags(
    data_manager: DataManager,
    chunker: Chunker,
    args
) -> BatchEmbedder:
    """
    Creates a BatchEmbedder instance based on command-line arguments or config.
    If you want to add a switch for other providers (Marqo, etc.), do it here.
    """
    # Convert to dict if needed
    args_dict = vars(args) if hasattr(args, '__dict__') else args

    if args_dict["embedding_provider"] == "openai":
        # Create our real-time embedder with the chunker
        return OpenAIRealTimeEmbedder(
            data_manager=data_manager,
            chunker=chunker,
            local_dir=args_dict["local_dir"],
            embedding_model=args_dict["embedding_model"],
            embedding_size=args_dict.get("embedding_size", 1536)
        )
    else:
        raise ValueError(f"Unrecognized embedder type {args_dict['embedding_provider']}")
