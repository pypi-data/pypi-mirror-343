"""Vector store abstraction and implementations."""

import logging
import os
from abc import ABC, abstractmethod
from enum import Enum
from functools import cached_property
from typing import Dict, Generator, List, Optional, Tuple, Any
from uuid import uuid4


import nltk
from langchain.retrievers import EnsembleRetriever
from langchain_chroma import Chroma as LangChainChroma
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS, Marqo
from langchain_community.vectorstores import Pinecone as LangChainPinecone
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore as LangChainQdrant
from langchain_voyageai import VoyageAIEmbeddings

# Removed Milvus imports as they're not used in the application
from nltk.data import find
from pinecone import Pinecone, ServerlessSpec
from pinecone_text.sparse import BM25Encoder
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from constants import TEXT_FIELD
from data_manager import DataManager

Vector = Tuple[Dict, List[float]]  # (metadata, embedding)


class VectorStoreProvider(Enum):
    PINECONE = "pinecone"
    MARQO = "marqo"
    CHROMA = "chroma"
    FAISS = "faiss"
    # MILVUS = "milvus"  # Removed as it's not used in the application
    QDRANT = "qdrant"


def is_punkt_downloaded():
    try:
        find("tokenizers/punkt_tab")
        return True
    except LookupError:
        return False


class VectorStore(ABC):
    """Abstract class for a vector store."""

    @abstractmethod
    def ensure_exists(self):
        """Ensures that the vector store exists. Creates it if it doesn't."""

    @abstractmethod
    def upsert_batch(self, vectors: List[Vector], namespace: str):
        """Upserts a batch of vectors."""

    def upsert(self, vectors: Generator[Vector, None, None], namespace: str):
        """Upserts in batches of 100, since vector stores have a limit on upsert size."""
        batch = []
        for metadata, embedding in vectors:
            batch.append((metadata, embedding))
            if len(batch) == 150:
                self.upsert_batch(batch, namespace)
                batch = []
        if batch:
            self.upsert_batch(batch, namespace)

    @abstractmethod
    def as_retriever(self, top_k: int, embeddings: Embeddings, namespace: str):
        """Converts the vector store to a LangChain retriever object."""


class PineconeVectorStore(VectorStore):
    """Vector store implementation using Pinecone."""

    def __init__(self, index_name: str, dimension: int, alpha: float, bm25_cache: Optional[str] = None):
        """
        Args:
            index_name: The name of the Pinecone index to use. If it doesn't exist already, we'll create it.
            dimension: The dimension of the vectors.
            alpha: The alpha parameter for hybrid search: alpha == 1.0 means pure dense search, alpha == 0.0 means pure
                BM25, and 0.0 < alpha < 1.0 means a hybrid of the two.
            bm25_cache: The path to the BM25 encoder file. If not specified, we'll use the default BM25 (fitted on the
                MS MARCO dataset).
        """
        self.index_name = index_name
        self.dimension = dimension
        self.client = Pinecone()
        self.alpha = alpha
        if alpha < 1.0:
            if bm25_cache and os.path.exists(bm25_cache):
                logging.info("Loading BM25 encoder from cache.")
                # We need nltk tokenizers for bm25 tokenization
                if is_punkt_downloaded():
                    print("punkt is already downloaded")
                else:
                    print("punkt is not downloaded")
                    # Optionally download it
                    nltk.download("punkt_tab")
                self.bm25_encoder = BM25Encoder()
                self.bm25_encoder.load(path=bm25_cache)
            else:
                logging.info("Using default BM25 encoder (fitted to MS MARCO).")
                self.bm25_encoder = BM25Encoder.default()
        else:
            self.bm25_encoder = None

    @cached_property
    def index(self):
        self.ensure_exists()
        index = self.client.Index(self.index_name)

        # Hack around the fact that PineconeRetriever expects the content of the chunk to be in a "text" field,
        # while PineconeHybridSearchRetrieve expects it to be in a "context" field.
        original_query = index.query

        def patched_query(*args, **kwargs):
            result = original_query(*args, **kwargs)
            for res in result["matches"]:
                if TEXT_FIELD in res["metadata"]:
                    res["metadata"]["context"] = res["metadata"][TEXT_FIELD]
            return result

        index.query = patched_query
        return index

    def ensure_exists(self):
        if self.index_name not in self.client.list_indexes().names():
            self.client.create_index(
                name=self.index_name,
                dimension=self.dimension,
                # See https://www.pinecone.io/learn/hybrid-search-intro/
                metric="dotproduct" if self.bm25_encoder else "cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

    def upsert_batch(self, vectors: List[Vector], namespace: str):
        pinecone_vectors = []
        for i, (metadata, embedding) in enumerate(vectors):
            vector = {"id": metadata.get("id", str(i)), "values": embedding, "metadata": metadata}
            if self.bm25_encoder:
                vector["sparse_values"] = self.bm25_encoder.encode_documents(metadata[TEXT_FIELD])
            pinecone_vectors.append(vector)

        self.index.upsert(vectors=pinecone_vectors, namespace=namespace)

    def as_retriever(self, top_k: int, embeddings: Embeddings, namespace: str):
        bm25_retriever = (
            BM25Retriever(
                embeddings=embeddings,
                sparse_encoder=self.bm25_encoder,
                index=self.index,
                namespace=namespace,
                top_k=top_k,
            )
            if self.bm25_encoder
            else None
        )

        dense_retriever = LangChainPinecone.from_existing_index(
            index_name=self.index_name, embedding=embeddings, namespace=namespace
        ).as_retriever(search_kwargs={"k": top_k})

        if bm25_retriever:
            return EnsembleRetriever(retrievers=[dense_retriever, bm25_retriever], weights=[self.alpha, 1 - self.alpha])
        else:
            return dense_retriever

    def semantic_file_search(self, query: str, namespace: str, top_k: int = 7) -> List[Dict[str, Any]]:
        """
        Perform semantic search to find relevant files based on query.
        Returns list of file paths with similarity scores.
        """
        try:
            # Initialize embeddings
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Get query embedding
            query_embedding = embeddings.embed_query(query)
            
            logging.info(f"Searching in namespace: {namespace} with query: {query}")
            
            # Query the vector store
            query_response = self.index.query(
                namespace=namespace,
                top_k=top_k,
                include_metadata=True,
                vector=query_embedding,
                alpha=1
            )

            if not query_response or "matches" not in query_response:
                logging.warning(f"No matches found in namespace: {namespace}")
                return []

            # Process and deduplicate results by file path
            seen_files = set()
            results = []
            
            for match in query_response["matches"]:
                metadata = match.get("metadata", {})
                file_path = metadata.get("file_path")
                if file_path and file_path not in seen_files:
                    seen_files.add(file_path)
                    results.append({
                        "file_path": file_path,
                        "score": float(match["score"]),
                        "metadata": metadata
                    })
            
            logging.info(f"Found {len(results)} unique files")
            return results
            
        except Exception as e:
            logging.error(f"Error in semantic file search: {str(e)}")
            raise


def build_vector_store_from_args(
    args,  # Can be dict or SimpleNamespace
    data_manager: Optional[DataManager] = None,
) -> VectorStore:
    """Builds a vector store from the given command-line arguments.

    When `data_manager` is specified and hybrid retrieval is requested, we'll use it to fit a BM25 encoder on the corpus
    of documents.
    
    Args:
        args: Can be either a dict or SimpleNamespace object containing the configuration
        data_manager: Optional DataManager for BM25 encoding
    """
    # Convert to dict if SimpleNamespace
    args_dict = vars(args) if hasattr(args, '__dict__') else args

    # Milvus check removed as it's not used in the application

    if args_dict["embedding_provider"] == "openai":
        embeddings = OpenAIEmbeddings(model=args_dict["embedding_model"])
    elif args_dict["embedding_provider"] == "voyage":
        embeddings = VoyageAIEmbeddings(model=args_dict["embedding_model"])
    elif args_dict["embedding_provider"] == "gemini":
        embeddings = GoogleGenerativeAIEmbeddings(model=args_dict["embedding_model"])

    if args_dict["vector_store_provider"] == "pinecone":
        bm25_cache = os.path.join(".bm25_cache", args_dict["index_namespace"], "bm25_encoder.json")
        if args_dict["retrieval_alpha"] < 1.0 and not os.path.exists(bm25_cache) and data_manager:
            logging.info("Fitting BM25 encoder on the corpus...")
            if is_punkt_downloaded():
                print("punkt is already downloaded")
            else:
                print("punkt is not downloaded")
                # Optionally download it
                nltk.download("punkt_tab")
            corpus = [content for content, _ in data_manager.walk()]
            bm25_encoder = BM25Encoder()
            bm25_encoder.fit(corpus)
            # Make sure the folder exists, before we dump the encoder.
            bm25_folder = os.path.dirname(bm25_cache)
            if not os.path.exists(bm25_folder):
                os.makedirs(bm25_folder)
            bm25_encoder.dump(bm25_cache)

        return PineconeVectorStore(
            index_name=args_dict["index_name"],
            dimension=args_dict.get("embedding_size", 1536),  # Default to 1536 if not specified
            alpha=args_dict["retrieval_alpha"],
            bm25_cache=bm25_cache,
        )
    else:
        raise ValueError(f"Unrecognized vector store type {args_dict['vector_store_provider']}")