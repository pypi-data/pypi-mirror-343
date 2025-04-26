import time
import logging
import asyncio
import os
import traceback
import json
import requests
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv


load_dotenv()

# Redis import removed - now using MongoDB directly for status updates
from project_store import get_project, update_project
from index import index_repository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def with_connection_retry(max_retries=3, retry_delay=1.0):
    """
    Decorator that adds connection retry logic to async functions.
    Handles network-related errors with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    result = await func(*args, **kwargs)
                    # Check if result is a dictionary with error info
                    if isinstance(result, dict) and result.get("success") is False and "error" in result:
                        # Don't treat this as success - continue with retries
                        last_exception = Exception(result["error"])
                        if attempt < max_retries:
                            wait_time = retry_delay * (2 ** attempt)
                            logger.warning(f"Operation failed in {func.__name__}, retry {attempt+1}/{max_retries} "
                                        f"after {wait_time:.2f}s: {result['error']}")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            logger.error(f"Max retries reached for {func.__name__}: {result['error']}")
                    # Otherwise return the result
                    return result
                except (BrokenPipeError, ConnectionError, OSError, requests.exceptions.RequestException) as e:
                    last_exception = e
                    error_type = type(e).__name__
                    if attempt < max_retries:
                        wait_time = retry_delay * (2 ** attempt)
                        logger.warning(f"Network error in {func.__name__}, retry {attempt+1}/{max_retries} "
                                       f"after {wait_time:.2f}s: {error_type} - {str(e)}")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Max retries reached for {func.__name__}: {error_type} - {str(e)}")
                        logger.error(f"Error trace: {traceback.format_exc()}")
            
            # If we reach here, all retries failed
            # Return a failure result rather than raising the error
            logger.error(f"All retries failed for {func.__name__}, continuing with fallback")
            return {"success": False, "error": str(last_exception)}
        return wrapper
    return decorator


async def process_repository_job(job_data: dict):
    """
    This function processes the repository indexing job:
    1. Extract needed fields from job_data
    2. Call the index_repository(...) function
    3. Update redis/mongo with status
    """
    project_id = job_data["project_id"]
    user_id = job_data["user_id"]
    repo_url = job_data["repo_url"]
    branch_or_commit = job_data["branch_or_commit"]
    github_token = job_data["github_token"]

    # Create job diagnostic info for tracking
    job_start_time = datetime.now()
    job_metadata = {
        "job_id": project_id,
        "user_id": user_id,
        "started_at": job_start_time.isoformat(),
        "repo_url": repo_url,
        "status_updates_count": 0
    }
    
    def log_job_event(event_type, details=None):
        """Helper to log job-specific events with consistent format"""
        log_data = {
            "event": event_type,
            "job_id": project_id,
            "user_id": user_id,
            "time": datetime.now().isoformat(),
            "job_runtime_seconds": (datetime.now() - job_start_time).total_seconds(),
        }
        if details:
            log_data.update(details)
        logger.info(f"JOB_EVENT: {json.dumps(log_data)}")

    log_job_event("job_started")

    try:
        # Indicate that indexing is starting
        start_time = int(time.time())
        initial_status = {
            "status": "indexing",
            "progress": {
                "stage": "initializing",
                "message": "Starting indexing from worker",
                "progress": 0,
                "start_time": start_time,
                "current_file": None,
                "files_processed": 0,
                "total_files": 0,
                "bytes_processed": 0,
                "branch_or_commit": branch_or_commit  # Include branch/commit info in status
            }
        }
        
        # Critical function to update status with fallback to direct DB updates
        @with_connection_retry(max_retries=3, retry_delay=0.5)
        async def update_status(status_data, is_critical=False):
            """Update status with Redis, falling back to direct MongoDB update if Redis fails"""
            nonlocal job_metadata
            
            job_metadata["status_updates_count"] += 1
            update_count = job_metadata["status_updates_count"]
            
            # Update MongoDB directly
            try:
                log_job_event("mongodb_update_attempt", {"update_count": update_count})
                
                # Check if this is the final "indexed" status
                is_indexed = status_data.get("status") == "indexed"
                
                update_project(
                    project_id, 
                    user_id, 
                    status=status_data.get("status", "indexing"), 
                    progress=status_data.get("progress", {}),
                    branch_or_commit=branch_or_commit if "branch_or_commit" not in status_data.get("progress", {}) else None,
                    is_indexed=is_indexed
                )
                log_job_event("mongodb_update_success")
            except Exception as db_err:
                log_job_event("mongodb_update_failed", {"error": str(db_err)})
                logger.error(f"Critical error: Failed to update MongoDB status: {db_err}")
                
        # Initialize status
        await update_status(initial_status)

        # Batch progress updates using a queue
        progress_queue = asyncio.Queue()
        last_update_time = time.time()
        MIN_UPDATE_INTERVAL = 0.3  # Reduced from 1.0 to 0.3 seconds for smoother updates
        last_progress = 0  # Track last reported progress
        
        # Define progress thresholds for important stages
        PROGRESS_THRESHOLDS = {
            "initializing": 0,
            "cloning": 5,
            "analyzing": 10,
            "preparing": 15,
            "indexing": 20,  # Starting point for actual indexing
            "completed": 100
        }

        async def progress_callback(stage: str, message: str, progress: float, details: dict = None):
            """Callback to update progress during indexing with batching"""
            nonlocal last_progress
            
            # Check cancellation by checking project status in MongoDB
            try:
                proj = get_project(project_id, user_id)
                if proj and proj.get("status") == "cancelled":
                    log_job_event("cancellation_detected")
                    logger.info(f"[worker] Cancellation requested for project {project_id}")
                    raise Exception("Job cancelled by user")
            except Exception as e:
                # Don't fail the whole job if cancel check fails
                log_job_event("cancellation_check_error", {"error": str(e)})
                logger.warning(f"Error checking cancellation status: {e}")
            
            # Enhance GitHub rate limit messaging
            if stage == "error" and "rate limit exceeded" in message.lower():
                message = "GitHub API rate limit exceeded. Your job will be automatically retried later. You may need to add a GitHub token to your account for better performance."
            
            # Ensure progress is within stage bounds
            base_progress = PROGRESS_THRESHOLDS.get(stage, last_progress)
            if stage == "indexing":
                # Scale the indexing progress from 20-95%
                adjusted_progress = base_progress + (progress * 0.75)  # 75% of remaining progress
            else:
                adjusted_progress = base_progress
            
            # Ensure progress never goes backwards
            adjusted_progress = max(last_progress, adjusted_progress)
            
            # Force update on significant progress changes or stage changes
            force_update = (
                abs(adjusted_progress - last_progress) >= 5 or  # Progress changed by 5% or more
                stage != getattr(progress_callback, 'last_stage', None) or  # Stage changed
                "error" in stage.lower()  # Always force update on errors
            )
            
            status_data = {
                "status": "indexing",
                "progress": {
                    "stage": stage,
                    "message": message,
                    "progress": round(adjusted_progress, 1),  # Round to 1 decimal place
                    "start_time": start_time,
                    **(details if details else {})
                },
                "force_update": force_update  # Flag for forced updates
            }
            
            # Update tracking variables
            last_progress = adjusted_progress
            progress_callback.last_stage = stage
            
            # Add to queue for batched processing
            try:
                await progress_queue.put(status_data)
                log_job_event("progress_update_queued", {"stage": stage, "progress": adjusted_progress})
            except Exception as e:
                log_job_event("progress_queue_error", {"error": str(e)})
                logger.error(f"Error adding to progress queue: {e}")

        async def process_progress_updates():
            """Process progress updates in batches with smoother UI updates"""
            nonlocal last_update_time
            
            while True:
                try:
                    # Get the first update
                    status_data = await progress_queue.get()
                    current_time = time.time()
                    force_update = status_data.pop("force_update", False)
                    
                    # Update if:
                    # 1. Enough time has passed since last update OR
                    # 2. This is a forced update (significant progress change or stage change)
                    if force_update or current_time - last_update_time >= MIN_UPDATE_INTERVAL:
                        # For non-forced updates, drain queue to get latest status
                        if not force_update:
                            try:
                                while not progress_queue.empty():
                                    next_status = await progress_queue.get_nowait()
                                    next_force_update = next_status.pop("force_update", False)
                                    if next_force_update:
                                        # If we find a forced update, use it instead
                                        status_data = next_status
                                        break
                                    status_data = next_status
                                    progress_queue.task_done()
                            except asyncio.QueueEmpty:
                                # Queue might have been emptied by another task
                                pass
                        
                        # Update Redis and MongoDB with retry logic
                        try:
                            # Make sure we're awaiting a coroutine, not using a dict in await
                            status_update_result = await update_status(status_data)
                            last_update_time = current_time
                        except Exception as e:
                            log_job_event("progress_update_error", {"error": str(e)})
                            logger.error(f"Error updating status: {e}")
                    
                    progress_queue.task_done()
                    
                except asyncio.CancelledError:
                    # Handle cancellation gracefully
                    log_job_event("progress_processor_cancelled")
                    logger.info(f"Progress processor for project {project_id} cancelled")
                    break
                except Exception as e:
                    log_job_event("progress_processor_error", {"error": str(e)})
                    logger.error(f"Error processing progress updates: {e}")
                    # Don't break the loop on error
                    await asyncio.sleep(0.5)  # Brief delay to avoid tight loops on persistent errors

        # Start progress processor task
        progress_processor = asyncio.create_task(process_progress_updates())
        log_job_event("progress_processor_started")

        try:
            MAX_RETRIES = 3
            retry_count = 0
            retry_delay = 5  # Initial delay in seconds
            
            while retry_count < MAX_RETRIES:
                try:
                    # Create a unique local directory for each job with project ID
                    local_dir = f"/tmp/nia_repo_{project_id}_{int(time.time())}"
                    log_job_event("directory_created", {"path": local_dir})
                    
                    # Clean up previous repo directory if it exists
                    try:
                        import shutil
                        if os.path.exists(local_dir):
                            shutil.rmtree(local_dir)
                        os.makedirs(local_dir, exist_ok=True)
                        log_job_event("directory_cleaned")
                    except Exception as cleanup_error:
                        log_job_event("cleanup_error", {"error": str(cleanup_error)})
                        logger.warning(f"Failed to clean up repository directory: {cleanup_error}")
                    
                    # Attempt to index the repository with timeout
                    log_job_event("indexing_started")
                    result = await asyncio.wait_for(
                        index_repository(
                            repo_url=repo_url,
                            commit_hash=branch_or_commit,
                            local_dir=local_dir,
                            pinecone_index="nia-app",
                            max_tokens=800,
                            overlap=100,
                            user_id=user_id,
                            project_id=project_id,
                            access_token=github_token,
                            progress_callback=progress_callback
                        ),
                        timeout=3600  # 1 hour timeout for the entire operation
                    )
                    
                    log_job_event("indexing_completed")
                    # If we get here, indexing was successful
                    break
                    
                except asyncio.TimeoutError:
                    log_job_event("indexing_timeout")
                    logger.error(f"[worker] Timeout while indexing project {project_id}")
                    raise Exception("Indexing operation timed out. The repository might be too large.")
                    
                except (BrokenPipeError, ConnectionError, OSError, requests.exceptions.RequestException) as e:
                    error_type = type(e).__name__
                    log_job_event("network_error", {"error_type": error_type, "message": str(e)})
                    
                    if retry_count < MAX_RETRIES - 1:
                        retry_count += 1
                        wait_time = retry_delay * (2 ** retry_count)
                        logger.warning(f"[worker] Network error for project {project_id}: {error_type} - {str(e)}. "
                                     f"Retry {retry_count}/{MAX_RETRIES} after {wait_time}s")
                        
                        # Update status to show we're waiting for retry
                        retry_message = f"Network connection issue. Retrying... ({retry_count}/{MAX_RETRIES})"
                        await progress_callback("waiting", retry_message, last_progress)
                        
                        log_job_event("network_retry", {"attempt": retry_count, "wait_time": wait_time})
                        # Wait before retry
                        await asyncio.sleep(wait_time)
                    else:
                        log_job_event("network_retry_exhausted")
                        logger.error(f"[worker] Max retries reached for network error: {error_type} - {str(e)}")
                        raise
                        
                except ValueError as e:
                    error_message = str(e).lower()
                    log_job_event("value_error", {"message": error_message})
                    
                    # Check if this is a rate limit error
                    if "rate limit exceeded" in error_message and retry_count < MAX_RETRIES - 1:
                        retry_count += 1
                        wait_time = retry_delay * (2 ** retry_count)  # Exponential backoff
                        
                        logger.warning(f"[worker] GitHub rate limit hit for project {project_id}. Retry {retry_count}/{MAX_RETRIES} after {wait_time}s")
                        
                        # Update status to show we're waiting for rate limit
                        rate_limit_message = f"GitHub API rate limit exceeded. Waiting to retry... ({retry_count}/{MAX_RETRIES})"
                        await progress_callback("waiting", rate_limit_message, last_progress)
                        
                        log_job_event("rate_limit_retry", {"attempt": retry_count, "wait_time": wait_time})
                        # Wait before retry
                        await asyncio.sleep(wait_time)
                    else:
                        # Not a rate limit error or max retries reached
                        raise
                except Exception as e:
                    # Any other error should be re-raised immediately
                    log_job_event("indexing_error", {"error": str(e)})
                    logger.error(f"[worker] Error during indexing: {str(e)}", exc_info=True)
                    raise

            # No need to clear cancellation flag - all status is in MongoDB now
            log_job_event("job_completing_successfully")

            # Final status update
            final_status = {
                "status": "indexed",
                "progress": {
                    "stage": "completed",
                    "message": "Indexing completed successfully",
                    "progress": 100,
                    "completion_time": int(time.time()),
                    "start_time": start_time
                }
            }
            log_job_event("setting_final_status")
            await update_status(final_status, is_critical=True)  # This is a critical update
            
            # Also update the MongoDB is_indexed flag directly
            try:
                log_job_event("updating_is_indexed_flag")
                update_project(project_id, user_id, is_indexed=True)
                log_job_event("is_indexed_flag_updated")
            except Exception as e:
                log_job_event("is_indexed_update_failed", {"error": str(e)})
                logger.error(f"Failed to update is_indexed flag: {e}")
            
            log_job_event("job_completed_successfully")
            logger.info(f"[worker] Successfully indexed project {project_id} with {repo_url}")

        except BrokenPipeError as e:
            # Handle broken pipe errors gracefully
            error_message = f"Network connection error: {str(e)}"
            log_job_event("broken_pipe_error", {"error": str(e)})
            logger.error(f"[worker] Broken pipe error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(error_message)

        except ConnectionError as e:
            # Handle other connection errors
            error_message = f"Network connection error: {str(e)}"
            log_job_event("connection_error", {"error": str(e)})
            logger.error(f"[worker] Connection error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(error_message)

        except Exception as e:
            # Re-raise the exception to be handled by the outer try/except
            log_job_event("indexing_exception", {"error": str(e)})
            logger.error(f"[worker] Error during indexing: {e}", exc_info=True)
            raise

        finally:
            # Cancel and wait for progress processor to complete
            log_job_event("cleanup_started")
            try:
                if not progress_processor.done():
                    progress_processor.cancel()
                    # Set a timeout for waiting for the task to complete
                    try:
                        await asyncio.wait_for(progress_processor, timeout=2.0)
                        log_job_event("progress_processor_cancelled_successfully")
                    except asyncio.TimeoutError:
                        log_job_event("progress_processor_cancel_timeout")
                        logger.warning(f"Timeout waiting for progress processor to complete for project {project_id}")
                    except asyncio.CancelledError:
                        log_job_event("progress_processor_cancelled_normally")
                        # Task was cancelled successfully
                        pass
            except Exception as e:
                log_job_event("progress_processor_cancel_error", {"error": str(e)})
                logger.error(f"Error cancelling progress processor: {e}")
            
            # Clean up the temporary repository directory
            try:
                import shutil
                if os.path.exists(local_dir):
                    shutil.rmtree(local_dir)
                    log_job_event("repo_directory_cleaned")
            except Exception as cleanup_error:
                log_job_event("repo_cleanup_error", {"error": str(cleanup_error)})
                logger.warning(f"Failed to clean up repository directory: {cleanup_error}")

    except Exception as e:
        error_message = str(e)
        log_job_event("job_error", {"error": error_message})
        
        if "Job cancelled by user" in error_message:
            status = "cancelled"
            message = "Indexing cancelled by user"
            log_job_event("job_cancelled")
        elif "rate limit exceeded" in error_message.lower():
            # Special handling for rate limit errors
            status = "rate_limited"
            message = "GitHub API rate limit exceeded. Your job will be automatically retried later. Consider installing the GitHub App to prevent rate limits."
            log_job_event("job_rate_limited")
            # Requeue the job with a delay if possible
            try:
                # Enqueue with a delay of 30-60 minutes
                delay = 1800 + (hash(project_id) % 1800)  # 30-60 minute delay with some randomization
                log_job_event("requeueing_rate_limited", {"delay": delay})
                logger.info(f"[worker] Requeueing rate-limited job {project_id} with {delay}s delay")
                # This assumes there's a method to enqueue with delay, modify as needed:
                # redis_service.enqueue_job_with_delay(job_data, delay_seconds=delay)
            except Exception as req_err:
                log_job_event("requeue_error", {"error": str(req_err)})
                logger.error(f"[worker] Failed to requeue rate-limited job: {req_err}")
        elif "Broken pipe" in error_message or "[Errno 32]" in error_message:
            status = "error"
            message = "Network connection error during indexing. Please try again."
            log_job_event("broken_pipe_final_error")
        else:
            status = "error"
            message = f"Error during indexing: {error_message}"
            log_job_event("general_error")
            logger.exception(f"[worker] Error processing repository job: {e}")

        error_status = {
            "status": status,
            "progress": {
                "stage": status,
                "message": message,
                "progress": -1,
                "error_time": int(time.time()),
                "start_time": start_time
            }
        }
        
        # Try to update status with extra retries for error state
        try:
            log_job_event("setting_error_status")
            # Use special update function for critical updates
            await update_status(error_status, is_critical=True)
            log_job_event("error_status_set")
        except Exception as status_err:
            log_job_event("error_status_update_failed", {"error": str(status_err)})
            logger.error(f"[worker] Failed to update error status: {status_err}")
            
            # Super-critical direct MongoDB fallback
            try:
                log_job_event("critical_mongodb_fallback")
                update_project(project_id, user_id, status=status, error=message, 
                              progress=error_status["progress"], is_indexed=False)
                log_job_event("critical_mongodb_success")
            except Exception as db_err:
                log_job_event("critical_mongodb_failed", {"error": str(db_err)})
                logger.critical(f"CRITICAL: Failed all attempts to update project status: {db_err}")
        
        # No need to clear cancellation flag - using MongoDB for status
        log_job_event("job_error_handled")
    
    finally:
        job_end_time = datetime.now()
        job_duration = (job_end_time - job_start_time).total_seconds()
        log_job_event("job_finalized", {
            "duration_seconds": job_duration,
            "redis_success_count": job_metadata["redis_success_count"],
            "redis_error_count": job_metadata["redis_error_count"],
            "status_updates_count": job_metadata["status_updates_count"]
        })


async def worker_loop():
    """Main worker loop that processes jobs from the queue with efficient polling"""
    worker_id = int(os.getenv("WORKER_ID", 0))
    logger.info(f"Starting worker {worker_id}")
    
    # Track worker statistics
    worker_stats = {
        "start_time": datetime.now(),
        "jobs_processed": 0,
        "jobs_failed": 0,
        "last_active": datetime.now(),
        "last_success": None,
        "last_error": None
    }
    
    # No more Redis connection check needed
    logger.info(f"[Worker {worker_id}] Worker starting up")
    
    # Polling configuration
    min_sleep = 0.5  # Minimum sleep time in seconds
    max_sleep = 5.0  # Maximum sleep time in seconds
    current_sleep = min_sleep
    consecutive_empty = 0
    backoff_factor = 1.5
    
    # Rate limit tracking for this worker
    rate_limit_hits = 0
    last_rate_limit_time = 0
    
    logger.info(f"[Worker {worker_id}] Entering main processing loop")
    
    while True:
        worker_stats["last_active"] = datetime.now()
        uptime = (worker_stats["last_active"] - worker_stats["start_time"]).total_seconds()
        
        try:
            # Check if we've hit rate limits recently and need to back off
            current_time = time.time()
            if rate_limit_hits > 3 and current_time - last_rate_limit_time < 300:  # 5 minutes
                # We've hit multiple rate limits recently, back off for a while
                backoff_time = min(60 * rate_limit_hits, 1800)  # Up to 30 minutes
                logger.warning(f"[Worker {worker_id}] Backing off for {backoff_time}s due to repeated rate limits")
                await asyncio.sleep(backoff_time)
                rate_limit_hits = 0  # Reset after backing off
                
            # Log polling attempt periodically
            if consecutive_empty % 10 == 0:
                logger.debug(f"[Worker {worker_id}] Polling for jobs (attempt {consecutive_empty})")
                
                # Log worker stats periodically
                if consecutive_empty % 60 == 0:
                    logger.info(f"[Worker {worker_id}] Stats: Uptime={uptime:.1f}s, "
                               f"Jobs processed={worker_stats['jobs_processed']}, "
                               f"Failed={worker_stats['jobs_failed']}")
            
            # This worker process is no longer responsible for dequeuing jobs 
            # Hatchet workers handle that now, so we'll just sleep and periodically log status
            consecutive_empty += 1
            if consecutive_empty > 100:  # Reset counter periodically
                consecutive_empty = 0
                logger.info(f"[Worker {worker_id}] Worker is idle - Hatchet workers handle jobs now")
            await asyncio.sleep(max_sleep)
                
        except Exception as e:
            worker_stats["last_error"] = datetime.now()
            logger.error(f"[Worker {worker_id}] Error in worker loop: {str(e)}")
            logger.error(f"Error trace: {traceback.format_exc()}")
            # On error, sleep briefly
            await asyncio.sleep(min_sleep)
            continue


def main():
    logger.info("[worker] Starting Hatchet worker...")
    
    try:
        logger.info("[worker] Starting worker loop...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(worker_loop())
    except Exception as e:
        logger.critical(f"[worker] Fatal error in main worker process: {e}", exc_info=True)
        # Exit with error code so the process manager can restart the worker
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
