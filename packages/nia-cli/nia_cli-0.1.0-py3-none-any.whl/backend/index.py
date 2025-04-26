import logging
import os
import time
import shutil
import asyncio
from types import SimpleNamespace
from contextlib import contextmanager, asynccontextmanager
from typing import Dict, Callable, Any, List
import tenacity
from pathlib import Path
import requests
import json
from functools import lru_cache
import uuid
from datetime import datetime, timezone
import traceback

import configargparse

import config as nozomio_config
from chunker import UniversalFileChunker
from data_manager import GitHubRepoManager, FirecrawlManager
from embedder import build_batch_embedder_from_flags
from githubConfig import GitHubIssuesChunker, GitHubIssuesManager, get_installation_token
from vector_store import VectorStoreProvider, build_vector_store_from_args
from user_store import get_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a cache to minimize GitHub API calls
# Cache structure: {repo_url}:{branch/commit} -> validation_result
_github_validation_cache = {}

# Constants for GitHub API
GITHUB_API_BASE = "https://api.github.com"
GITHUB_RATE_LIMIT_REMAINING_HEADER = "X-RateLimit-Remaining"
GITHUB_RATE_LIMIT_RESET_HEADER = "X-RateLimit-Reset"
GITHUB_RETRY_WAIT_SECONDS = 10
GITHUB_RATE_LIMIT_THRESHOLD = 20  # Increased from 10 to be more conservative

def send_alert(message: str):
    """Send alert to monitoring system about cleanup failures or other critical issues.
    
    This function logs errors and can be extended to send alerts to monitoring systems.
    
    Args:
        message: The alert message to log and send
    """
    logger.error(f"ALERT: {message}")
    
    # Production monitoring implementation
    # This is a placeholder for your preferred alerting mechanism
    try:
        # You can implement various alerting mechanisms here:
        # Option 1: Send to error monitoring service
        # if os.environ.get("SENTRY_DSN"):
        #     import sentry_sdk
        #     sentry_sdk.capture_message(message, level="error")
        
        # Option 2: Send to logging service
        # if os.environ.get("DATADOG_API_KEY"):
        #     from datadog import statsd
        #     statsd.event('Critical Alert', message, alert_type='error')
        
        # Option 3: Send to Slack
        # if os.environ.get("SLACK_WEBHOOK_URL"):
        #     requests.post(
        #         os.environ.get("SLACK_WEBHOOK_URL"),
        #         json={"text": f"🚨 ALERT: {message}"}
        #     )
        pass
    except Exception as e:
        # Don't let alert sending failures cascade
        logger.error(f"Failed to send alert to monitoring system: {e}")
        # Continue execution despite alert failure

# Retry decorator with exponential backoff specifically for GitHub API rate limits
def github_retry(max_attempts=5):
    """
    Decorator to handle GitHub API rate limits with proper retries and backoff.
    Waits if rate limit is exceeded and retries the request.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error_message = str(e).lower()
                    
                    # Check if this is a rate limit error
                    if "rate limit exceeded" in error_message and attempt < max_attempts - 1:
                        wait_time = GITHUB_RETRY_WAIT_SECONDS * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"GitHub API rate limit exceeded. Waiting {wait_time} seconds before retry. Attempt {attempt+1}/{max_attempts}")
                        await asyncio.sleep(wait_time)
                        attempt += 1
                    else:
                        # If it's not a rate limit error or we've exceeded max retries, re-raise
                        raise
            raise Exception(f"Failed after {max_attempts} attempts due to GitHub API rate limits")
        return wrapper
    return decorator

async def check_github_rate_limit(access_token=None):
    """
    Check current GitHub API rate limit status and return remaining requests.
    Logs a warning if rate limit is below threshold.
    Always requires an access token.
    
    NOTE: This is an async function, but internally uses synchronous requests.
    Access token should be a string, not an awaitable.
    """
    if not access_token:
        logger.warning("Checking GitHub rate limits without a token - this should not happen with proper authentication")
        return 0, 0  # Return zero to indicate we should not proceed without a token
    
    # Ensure access_token is a string, not an awaitable or dictionary
    if not isinstance(access_token, str):
        raise TypeError("access_token must be a string, not an awaitable or dictionary")
        
    headers = {"Authorization": f"token {access_token}"}
    
    try:
        # This is a synchronous call in an async function - consider replacing with httpx.AsyncClient
        response = requests.get(f"{GITHUB_API_BASE}/rate_limit", headers=headers)
        
        if response.status_code == 200:
            rate_data = response.json()
            remaining = rate_data.get("resources", {}).get("core", {}).get("remaining", 0)
            reset_time = rate_data.get("resources", {}).get("core", {}).get("reset", 0)
            
            # Calculate time until reset
            now = time.time()
            minutes_to_reset = max(0, (reset_time - now) / 60)
            
            if remaining < GITHUB_RATE_LIMIT_THRESHOLD:
                logger.warning(
                    f"GitHub API rate limit low: {remaining} requests remaining. "
                    f"Resets in {minutes_to_reset:.1f} minutes."
                )
                # Alert if extremely low
                if remaining < 5:
                    send_alert(f"GitHub API rate limit critical: only {remaining} requests remaining")
            
            return remaining, reset_time
        else:
            logger.error(f"Failed to check GitHub rate limit: {response.status_code} {response.text}")
            return None, None
    except Exception as e:
        logger.error(f"Error checking GitHub rate limit: {e}")
        return None, None

@lru_cache(maxsize=128)
def get_normalized_repo_url(repo_url):
    """Normalize GitHub repository URL for consistent caching."""
    return repo_url.replace("https://github.com/", "").replace(".git", "").strip()

async def validate_branch_or_commit(repo_url, commit_hash, access_token=None):
    """
    Validate if a branch or commit exists in a GitHub repository with caching.
    
    Args:
        repo_url: GitHub repository URL
        commit_hash: Branch name or commit hash to validate
        access_token: GitHub access token for authentication (required)
        
    Returns:
        Tuple of (is_valid, message, response_text)
    """
    # No longer proceed without authentication
    if not access_token:
        return False, "Authentication required. GitHub token is mandatory.", None
        
    if not commit_hash:
        return True, "No branch/commit specified, using default", None
    
    # Normalize repository URL for consistent caching
    normalized_repo_url = get_normalized_repo_url(repo_url)
    
    # Check cache first
    cache_key = f"{normalized_repo_url}:{commit_hash}"
    if cache_key in _github_validation_cache:
        cached_result = _github_validation_cache[cache_key]
        # Check if cache entry has expired (60 minutes - increased from 30)
        if time.time() - cached_result.get("timestamp", 0) < 3600:  
            logger.info(f"Using cached validation result for {cache_key}")
            return (
                cached_result.get("is_valid", False),
                cached_result.get("message", ""),
                cached_result.get("response_text", "")
            )
    
    # Check current rate limit before making API calls
    remaining, reset_time = await check_github_rate_limit(access_token)
    if remaining is not None and remaining < 5:
        wait_time = max(0, reset_time - time.time())
        if wait_time > 0 and wait_time < 300:  # Only wait if less than 5 minutes
            logger.warning(f"Rate limit almost exhausted, waiting {wait_time:.1f} seconds for reset")
            await asyncio.sleep(wait_time + 2)  # Add a small buffer
    
    headers = {"Authorization": f"token {access_token}"}
    repo_api_url = f"{GITHUB_API_BASE}/repos/{normalized_repo_url}"
    
    # Log the request we're about to make
    logger.info(f"Validating branch/commit: {commit_hash} for repo {normalized_repo_url} with token")
    
    try:
        # First try as a branch
        branch_url = f"{repo_api_url}/branches/{commit_hash}"
        branch_resp = requests.get(branch_url, headers=headers)
        
        # Check and log rate limit headers
        remaining = branch_resp.headers.get(GITHUB_RATE_LIMIT_REMAINING_HEADER)
        if remaining and int(remaining) < GITHUB_RATE_LIMIT_THRESHOLD:
            reset_time = branch_resp.headers.get(GITHUB_RATE_LIMIT_RESET_HEADER, 0)
            current_time = time.time()
            minutes_to_reset = max(0, (int(reset_time) - current_time) / 60)
            logger.warning(
                f"GitHub API rate limit low after branch check: {remaining} requests remaining. "
                f"Resets in {minutes_to_reset:.1f} minutes."
            )
        
        if branch_resp.status_code == 200:
            # Found as branch
            result = (True, f"Valid branch: {commit_hash}", None)
            _github_validation_cache[cache_key] = {
                "is_valid": True,
                "message": f"Valid branch: {commit_hash}", 
                "timestamp": time.time()
            }
            return result
            
        elif branch_resp.status_code == 404:
            # Not a branch, try as a commit
            commit_url = f"{repo_api_url}/commits/{commit_hash}"
            commit_resp = requests.get(commit_url, headers=headers)
            
            # Check rate limit again
            remaining = commit_resp.headers.get(GITHUB_RATE_LIMIT_REMAINING_HEADER)
            if remaining and int(remaining) < GITHUB_RATE_LIMIT_THRESHOLD:
                logger.warning(f"GitHub API rate limit low after commit check: {remaining} requests remaining")
            
            if commit_resp.status_code == 200:
                # Found as commit
                result = (True, f"Valid commit: {commit_hash}", None)
                _github_validation_cache[cache_key] = {
                    "is_valid": True,
                    "message": f"Valid commit: {commit_hash}", 
                    "timestamp": time.time()
                }
                return result
            else:
                # Neither branch nor commit
                error_text = commit_resp.text
                status_code = commit_resp.status_code
                
                # Better error message based on status code
                error_message = f"Branch or commit '{commit_hash}' not found"
                
                # If this is an authentication issue and we don't have a token
                if status_code == 401 and not access_token:
                    error_message = "Authentication required - consider installing GitHub App for private repositories"
                elif status_code == 403:
                    error_message = "Permission denied - check repository access rights or install GitHub App"
                elif status_code == 404:
                    # Specific 404 message
                    error_message = f"Branch or commit '{commit_hash}' not found in repository"
                elif status_code >= 500:
                    error_message = f"GitHub server error (status: {status_code}) - try again later"
                
                logger.error(f"GitHub API error validating commit: {error_message} (status: {status_code})")
                
                result = (False, error_message, error_text)
                _github_validation_cache[cache_key] = {
                    "is_valid": False,
                    "message": error_message, 
                    "response_text": error_text,
                    "timestamp": time.time()
                }
                return result
                
        elif "rate limit exceeded" in branch_resp.text.lower():
            # Handle rate limiting explicitly
            error_text = branch_resp.text
            logger.error(f"GitHub API rate limit exceeded: {error_text}")
            raise ValueError(f"GitHub API rate limit exceeded. Please try again later or use an authenticated token.")
            
        else:
            # Some other error with the branch request
            error_text = branch_resp.text
            status_code = branch_resp.status_code
            error_message = f"Failed to validate branch/commit (status: {status_code}): {error_text[:200]}"
            logger.error(f"GitHub API error: {error_message}")
            
            # If this is an authentication issue and we don't have a token
            if status_code == 401 and not access_token:
                error_message = "Authentication required - consider installing GitHub App for private repositories"
            elif status_code == 403:
                error_message = "Permission denied - check repository access rights or install GitHub App"
            elif status_code >= 500:
                error_message = f"GitHub server error (status: {status_code}) - try again later"
                
            result = (False, error_message, error_text)
            _github_validation_cache[cache_key] = {
                "is_valid": False,
                "message": error_message, 
                "response_text": error_text,
                "timestamp": time.time()
            }
            return result
            
    except requests.exceptions.RequestException as e:
        error_message = f"Network error validating branch/commit: {str(e)}"
        return False, error_message, str(e)

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type(OSError),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry attempt {retry_state.attempt_number} for cleanup after error: {retry_state.outcome.exception()}"
    )
)
def safe_cleanup(path: str):
    """Safely clean up a directory with retries and proper error handling."""
    try:
        if not os.path.exists(path):
            return
            
        # Safety check: don't clean up system directories
        system_dirs = ['/tmp', '/var', '/usr', '/etc', '/home', '/', '/opt']
        if path in system_dirs:
            logger.error(f"Refusing to clean up system directory: {path}")
            return
        
        # Use shutil.rmtree with onerror handler to handle permission issues gracefully
        def handle_remove_error(func, path, exc_info):
            """Handle permission errors during removal"""
            logger.warning(f"Error removing {path}: {exc_info[1]}")
            
            # Try to make writable and retry
            try:
                if os.path.isdir(path):
                    os.chmod(path, 0o755)
                else:
                    os.chmod(path, 0o644)
                func(path)
            except Exception as e:
                logger.warning(f"Failed secondary removal attempt for {path}: {e}")
        
        # Remove the directory and its contents
        shutil.rmtree(path, onerror=handle_remove_error)
        logger.info(f"Successfully cleaned up directory: {path}")
        
    except Exception as e:
        error_msg = f"Failed to clean up directory {path}: {str(e)}"
        logger.error(error_msg)
        send_alert(error_msg)
        raise

@contextmanager
def temporary_directory(path: str, prefix=None):
    """Context manager for handling temporary directory cleanup with enhanced error handling and monitoring."""
    # Create a unique subdirectory within the specified path
    if path == '/tmp':
        # Generate a unique subdirectory in /tmp
        unique_dirname = f"nia_repo_{prefix or uuid.uuid4()}"
        path = os.path.join(path, unique_dirname)
    
    path = os.path.abspath(path)  # Get absolute path
    
    try:
        # Initial cleanup of existing directory
        if os.path.exists(path):
            safe_cleanup(path)
        
        # Create fresh directory
        os.makedirs(path, exist_ok=True)
        logger.info(f"Created temporary directory: {path}")
        
        yield path
        
    finally:
        try:
            if os.path.exists(path):
                # Verify we're not trying to delete a system directory
                system_dirs = ['/tmp', '/var', '/usr', '/etc', '/home', '/']
                if path in system_dirs:
                    logger.error(f"Refusing to clean up system directory: {path}")
                    return
                
                # Get directory size before cleanup for logging
                try:
                    total_size = sum(
                        os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, _, filenames in os.walk(path)
                        for filename in filenames
                    )
                except Exception as e:
                    total_size = 0
                    logger.warning(f"Failed to calculate directory size: {e}")
                
                safe_cleanup(path)
                logger.info(f"Cleaned up temporary directory: {path} (Size: {total_size/1024/1024:.2f} MB)")
                
        except Exception as e:
            error_msg = f"Error during temporary directory cleanup: {str(e)}"
            logger.error(error_msg)
            send_alert(error_msg)

@github_retry(max_attempts=3)
async def index_repository(
    repo_url: str,
    commit_hash: str = None,
    local_dir: str = "/tmp",
    pinecone_index: str = "nia-app",
    max_tokens: int = 800,  # Set optimal chunk size from research
    overlap: int = 100,
    user_id: str = "unknown",
    project_id: str = "unknown",
    progress_callback: Callable = None,
    access_token: str = None,
    namespace: str = None,  # Add namespace parameter
    use_nuanced: bool = True,  # Add Nuanced integration flag
    use_graph_rag: bool = False  # Add GraphRAG integration flag
) -> Dict[str, Any]:
    """
    Index a GitHub repository into a vector store with optimized settings.
    
    Args:
        repo_url: The URL of the repository to index
        commit_hash: The commit hash or branch name to index (defaults to main branch)
        local_dir: Local directory to clone the repository into
        pinecone_index: Name of the Pinecone index to use
        max_tokens: Maximum number of tokens per chunk (800 is optimal from research)
        overlap: Number of overlapping tokens between chunks
        user_id: User ID for tracking
        project_id: Project ID for tracking
        progress_callback: Optional callback for progress updates
        access_token: GitHub access token for private repos
        namespace: Optional namespace for vector store
        use_nuanced: Flag to enable Nuanced integration
        use_graph_rag: Flag to enable GraphRAG integration
        
    Returns:
        Dict with indexing results and progress information
    """
    # Initialize progress tracking
    progress = {
        "stage": "initializing",
        "message": "Starting indexing process",
        "progress": 0,
        "total_files": 0,
        "processed_files": 0
    }

    # Define update_progress outside the try block so it's available in all scopes
    async def update_progress(stage: str, message: str, progress_value: int, **kwargs):
        progress.update({
            "stage": stage,
            "message": message,
            "progress": progress_value,
            **kwargs  # Allow additional fields to be updated
        })
        logger.info(f"[index_repository] Progress => Stage: {stage}, Message: {message}, progress: {progress_value}")
        if progress_callback:
            try:
                # Pass details about files processed if available
                details = {
                    "total_files": progress.get("total_files", 0),
                    "processed_files": progress.get("processed_files", 0),
                    **kwargs
                }
                # Call with positional arguments in the correct order
                await progress_callback(stage, message, float(progress_value), details)
            except Exception as e:
                logger.error(f"Progress callback failed: {e}")
    
    try:
        # Get installation token if no access token provided - do this FIRST before any GitHub API calls
        # But for public repositories, we might proceed without a token
        is_public_repo = None
        
        if not access_token:
            try:
                user_doc = get_user(user_id)
                if user_doc and user_doc.get("github_installation_id"):
                    # The get_installation_token function is synchronous - don't use await
                    token_result = get_installation_token(user_doc["github_installation_id"])
                    
                    # Handle different return types from get_installation_token
                    if isinstance(token_result, dict) and "token" in token_result:
                        access_token = token_result["token"]
                    else:
                        access_token = token_result
                        
                    logger.info(f"[index_repository] Using GitHub App installation token for user {user_id}")
                else:
                    logger.warning(f"[index_repository] No GitHub installation found for user {user_id}")
                    # Check if repo is public before failing
                    try:
                        # Extract repo name from URL
                        repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
                        response = requests.get(f"https://api.github.com/repos/{repo_name}")
                        is_public_repo = response.status_code == 200
                        if is_public_repo:
                            logger.info(f"[index_repository] Repository {repo_url} is public, proceeding without token")
                        else:
                            raise ValueError("GitHub token required for private repositories. Please install the GitHub App.")
                    except requests.RequestException as e:
                        logger.error(f"[index_repository] Error checking if repo is public: {e}")
                        # Assume we'll try without token
                        logger.warning(f"[index_repository] Will attempt to access repo without token")
            except ValueError as ve:
                # Re-raise ValueError for private repos
                raise ve
            except Exception as e:
                logger.error(f"[index_repository] Failed to get installation token: {e}")
                logger.warning(f"[index_repository] Will attempt to access repo without token")
                
        # Check GitHub rate limits early - access_token must be a string, not a dict
        try:
            # Make sure we have a string token, not a dict
            token_to_use = access_token
            if isinstance(access_token, dict) and "token" in access_token:
                token_to_use = access_token["token"]
            elif not isinstance(access_token, str) and access_token is not None:
                logger.warning(f"[index_repository] Unexpected token type: {type(access_token)}, converting to string")
                token_to_use = str(access_token)
                
            await check_github_rate_limit(token_to_use)
        except Exception as e:
            logger.error(f"[index_repository] Rate limit check failed: {e}")
            # Continue with indexing even if rate limit check fails

        # Validate the branch/commit exists using our improved validation function
        # Ensure token is a string
        token_to_use = access_token
        if isinstance(access_token, dict) and "token" in access_token:
            token_to_use = access_token["token"]
        elif not isinstance(access_token, str) and access_token is not None:
            logger.warning(f"[index_repository] Unexpected token type in validate_branch_or_commit: {type(access_token)}")
            token_to_use = str(access_token)
            
        is_valid, message, error_text = await validate_branch_or_commit(repo_url, commit_hash, token_to_use)
        if not is_valid:
            if error_text and "rate limit exceeded" in error_text.lower():
                raise ValueError(f"GitHub API rate limit exceeded. Please try again later.")
            elif error_text:
                # Add diagnostic info to the log to help with troubleshooting
                logger.error(f"Branch/commit validation failed: {message}")
                logger.error(f"Error text from GitHub API: {error_text[:500]}")
                raise ValueError(message)
            else:
                # Just in case error_text is None
                raise ValueError(message or "Failed to validate branch or commit")

        logger.info(f"[index_repository] Indexing repository: {repo_url} for user {user_id}, project {project_id}")
        logger.info(f"[index_repository] Using temporary directory: {local_dir}")
        logger.info(f"[index_repository] Branch/commit validation: {message}")
        logger.info(f"[index_repository] UseNuanced: {use_nuanced}, UseGraphRAG: {use_graph_rag}")

        # Set up the repo manager with the specified branch/commit
        # Ensure token is a string
        token_for_manager = token_to_use  # Use the already-fixed token
            
        repo_manager = GitHubRepoManager(
            repo_id=repo_url.replace("https://github.com/", "").replace(".git", ""),
            commit_hash=commit_hash,
            access_token=token_for_manager,
            local_dir=local_dir
        )

        # Get the actual default branch
        default_branch = repo_manager.default_branch

        # Update metadata to include branch/commit info
        base_metadata = {
            "user_id": user_id if user_id else "unknown",
            "repo_url": repo_url,
            "indexed_at": time.time(),
            "branch_or_commit": commit_hash or default_branch,  # Use actual default branch
            "use_nuanced": use_nuanced,  # Include the Nuanced flag in metadata
            "use_graph_rag": use_graph_rag  # Include the GraphRAG flag in metadata
        }

        # Only add project_id if it's a valid value
        if project_id and project_id != "unknown" and project_id.strip() != "":
            base_metadata["project_id"] = project_id
            
        with temporary_directory(local_dir, prefix=project_id) as temp_dir:
            try:
                # -----------------------------------------
                # 1) Cloning stage
                # -----------------------------------------
                await update_progress("cloning", "Cloning repository", 10)

                repo_manager = GitHubRepoManager(
                    repo_id=repo_url.replace("https://github.com/", "").replace(".git", ""),
                    commit_hash=commit_hash,
                    access_token=token_for_manager,  # Pass the properly formatted token here
                    local_dir=temp_dir,
                    inclusion_file=None,
                    exclusion_file="sample-exclude.txt",  # use sample-exclude to skip big/unnecessary files
                )
                
                # First check if repo exists and is accessible
                try:
                    # Check if the repository is private and we don't have a valid token
                    if not repo_manager.is_public and not token_for_manager:
                        raise ValueError("This repository is private. Please provide a GitHub token by installing the GitHub App.")
                except requests.exceptions.RequestException as e:
                    if "rate limit exceeded" in str(e).lower():
                        raise ValueError("GitHub API rate limit exceeded. Please try again later.")
                    raise RuntimeError(f"Failed to check repository status: {str(e)}")
                
                # Try to clone the repository
                if not repo_manager.download():
                    error_msg = "Failed to clone the repository. "
                    if not access_token:
                        error_msg += "If this is a private repository, please provide a GitHub token. "
                    error_msg += "Otherwise, please verify the repository exists and is accessible."
                    raise RuntimeError(error_msg)

                # Generate Nuanced call graph if enabled
                graph_data = None
                if use_nuanced or use_graph_rag:  # Also generate graph data if GraphRAG is enabled
                    try:
                        from services.nuanced_service import NuancedService
                        
                        # Print clear Nuanced banner in logs
                        logger.info("")
                        logger.info("==== 🔍 NUANCED CALL GRAPH GENERATION ====")
                        logger.info(f"Repository: {repo_url}")
                        logger.info(f"Local directory: {temp_dir}")
                        
                        if NuancedService.is_installed():
                            logger.info("✅ NUANCED STATUS: Installed and available")
                            
                            await update_progress(
                                "nuanced_init", 
                                "Generating code call graph with Nuanced...", 
                                25
                            )
                            
                            logger.info(f"🔄 GENERATING GRAPH: Initializing for {temp_dir}")
                            start_time = time.time()
                            
                            nuanced_graph_path = NuancedService.init_graph(temp_dir)
                            generation_time = time.time() - start_time
                            
                            if nuanced_graph_path:
                                # Graph successfully generated
                                try:
                                    graph_size = os.path.getsize(nuanced_graph_path) / 1024  # KB
                                    
                                    # Check how many functions were processed
                                    with open(nuanced_graph_path, 'r') as f:
                                        graph_data = json.load(f)
                                        
                                        # Check graph format
                                        if "functions" in graph_data and "modules" in graph_data:
                                            # Traditional format
                                            function_count = len(graph_data.get("functions", {}))
                                            module_count = len(graph_data.get("modules", {}))
                                            graph_format = "traditional"
                                        else:
                                            # Flat format (function names as keys)
                                            function_count = len(graph_data)
                                            module_count = 0
                                            graph_format = "flat"
                                            
                                            # Count call relationships
                                            relationship_count = 0
                                            for _, func_data in graph_data.items():
                                                relationship_count += len(func_data.get("callees", []))
                                            
                                            logger.info(f"Detected flat graph structure with {relationship_count} relationships")
                                    
                                    logger.info(f"✅ GRAPH GENERATED: {nuanced_graph_path}")
                                    logger.info(f"  - Format: {graph_format}")
                                    logger.info(f"  - Size: {graph_size:.2f} KB")
                                    logger.info(f"  - Generation time: {generation_time:.2f} seconds")
                                    logger.info(f"  - Functions mapped: {function_count}")
                                    logger.info(f"  - Modules analyzed: {module_count}")
                                    
                                    # Create compact graph for Pinecone metadata
                                    compact_graph = NuancedService.extract_compact_graph(nuanced_graph_path)
                                    if compact_graph:
                                        # Store compact version in base metadata (will be saved to Pinecone)
                                        base_metadata["nuanced_graph_compact"] = compact_graph
                                        base_metadata["nuanced_function_count"] = function_count
                                        base_metadata["nuanced_module_count"] = module_count
                                        base_metadata["nuanced_graph_format"] = graph_format
                                        
                                        # Load graph data first, then store it compressed - more efficient
                                        try:
                                            # Store graph data directly for better compression
                                            storage_result = NuancedService.store_graph_in_db(project_id, graph_data=graph_data)
                                            logger.info(f"Graph data storage result: {storage_result}")
                                        except Exception as direct_error:
                                            logger.warning(f"Error storing graph data directly: {direct_error}")
                                            # Fall back to file-based storage
                                            storage_result = NuancedService.store_graph_in_db(project_id, graph_path=nuanced_graph_path)
                                            logger.info(f"Fallback graph data storage result: {storage_result}")
                                            
                                        if storage_result:
                                            logger.info(f"✅ Nuanced graph stored in database for project {project_id}")
                                            
                                            # Create a permanent copy of the repository for GraphRAG
                                            if use_graph_rag:
                                                try:
                                                    permanent_repo_path = f"/tmp/my_local_repo_{project_id}"
                                                    logger.info(f"Creating permanent repository copy for GraphRAG at {permanent_repo_path}")
                                                    
                                                    # Make sure the directory doesn't exist first
                                                    if os.path.exists(permanent_repo_path):
                                                        logger.info(f"Removing existing repository directory at {permanent_repo_path}")
                                                        shutil.rmtree(permanent_repo_path)
                                                    
                                                    # Make a copy of the repository
                                                    shutil.copytree(temp_dir, permanent_repo_path)
                                                    
                                                    # Fix permissions to ensure it's accessible later
                                                    os.chmod(permanent_repo_path, 0o755)
                                                    for root, dirs, files in os.walk(permanent_repo_path):
                                                        for d in dirs:
                                                            os.chmod(os.path.join(root, d), 0o755)
                                                        for f in files:
                                                            os.chmod(os.path.join(root, f), 0o644)
                                                        
                                                    logger.info(f"Successfully created permanent copy of repository for GraphRAG")
                                                    
                                                    # Store the repository path in project metadata
                                                    try:
                                                        from db import MongoDB
                                                        db = MongoDB()
                                                        
                                                        # Update project metadata with GraphRAG information
                                                        db.db.projects.update_one(
                                                            {"project_id": project_id},
                                                            {"$set": {
                                                                "graphrag_enabled": True,
                                                                "graphrag_repo_path": permanent_repo_path,
                                                                "use_graph_rag": True
                                                            }}
                                                        )
                                                        
                                                        # Also store graph data in the database for redundancy
                                                        try:
                                                            if NuancedService.is_installed():
                                                                graph_data = NuancedService.get_graph_data(permanent_repo_path)
                                                                if graph_data:
                                                                    logger.info(f"Storing GraphRAG data in database for project {project_id}")
                                                                    NuancedService.store_graph_in_db(project_id, graph_data)
                                                        except Exception as graph_error:
                                                            logger.warning(f"Failed to store graph data in database: {graph_error}")
                                                        
                                                        logger.info(f"Updated project metadata with GraphRAG information")
                                                    except Exception as db_error:
                                                        logger.warning(f"Failed to update project metadata: {db_error}")
                                                    
                                                except Exception as e:
                                                    logger.warning(f"Failed to create permanent repository copy: {e}")
                                                    # Continue with indexing even if permanent copy creation fails
                                    else:
                                        # Fallback to just path reference if compact extraction fails
                                        base_metadata["nuanced_graph_path"] = nuanced_graph_path
                                        base_metadata["nuanced_function_count"] = function_count
                                        base_metadata["nuanced_module_count"] = module_count
                                        base_metadata["nuanced_graph_format"] = graph_format

                                    # If GraphRAG is enabled, install optional dependencies
                                    if use_graph_rag:
                                        try:
                                            import pip
                                            logger.info("Installing GraphRAG dependencies...")
                                            
                                            required_packages = ["networkx", "igraph", "leidenalg", "cdlib", "python-Levenshtein"]
                                            for package in required_packages:
                                                try:
                                                    __import__(package)
                                                    logger.info(f"Dependency already installed: {package}")
                                                except ImportError:
                                                    logger.info(f"Installing missing dependency: {package}")
                                                    pip.main(["install", "-q", package])
                                            
                                            # Add GraphRAG metadata flag
                                            base_metadata["graphrag_enabled"] = True
                                            
                                        except Exception as deps_error:
                                            logger.error(f"Error installing GraphRAG dependencies: {deps_error}")
                                except Exception as analysis_error:
                                    logger.error(f"Error analyzing graph: {analysis_error}")
                                    base_metadata["nuanced_graph_path"] = nuanced_graph_path
                            else:
                                logger.warning("❌ GRAPH GENERATION FAILED: Continuing without Nuanced enhancement")
                        else:
                            logger.warning("❌ NUANCED NOT INSTALLED: Install with 'pip install nuanced'")
                            
                        logger.info("=========================================")
                    except ImportError:
                        logger.warning("❌ NUANCED IMPORT ERROR: Service module not available")
                        logger.info("=========================================")
                    except Exception as e:
                        logger.error(f"❌ NUANCED ERROR: {e}")
                        logger.error(f"Stack trace: {e.__traceback__}")
                        logger.info("=========================================")
                        # Continue without Nuanced

                # -----------------------------------------
                # 2) Analyze / Setup chunker
                # -----------------------------------------
                await update_progress("analyzing", "Analyzing repository structure", 30)
                chunker = UniversalFileChunker(max_tokens=max_tokens)  # Now uses dynamic sizing by default when max_tokens is None

                # -----------------------------------------
                # 3) Build embedder
                # -----------------------------------------

               
                await update_progress("preparing", "Building embedder", 40)
                args_dict = {
                    "embedding_provider": "openai",
                    "embedding_model": "text-embedding-3-small",
                    "embedding_size": 1536,
                    "tokens_per_chunk": 8192,  # not strictly used if chunker is set up already
                    "chunks_per_batch": 256,
                    "max_embedding_jobs": 4,
                    "llm_retriever": False,
                    "vector_store_provider": "pinecone",
                    "index_name": pinecone_index,
                    "index_namespace": f"{user_id}/{project_id}",
                    "retrieval_alpha": 1.0,
                    "multi_query_retriever": True,
                    "llm_provider": "anthropic",
                    "llm_model": "claude-3-7-sonnet-20250219",
                    "index_repo": True,
                    "index_issues": False,
                    "local_dir": temp_dir,
                    "repo_id": repo_url.replace("https://github.com/", "").replace(".git", ""),
                    "commit_hash": commit_hash,
                    "use_nuanced": use_nuanced,
                    "use_graph_rag": use_graph_rag,
                    "graph_data": graph_data  # Pass the graph data to the args
                }
                args = SimpleNamespace(**args_dict)

                # 4) Actually run the embedding job
                await update_progress("embedding", "Computing embeddings", 50)
                embedder = build_batch_embedder_from_flags(repo_manager, chunker, args)
                metadata_file = await embedder.embed_dataset(chunks_per_batch=args.chunks_per_batch)

                # After embedding completes, we can log the final embedder stats:
                logger.info(f"[index_repository] Embedding Stats => "
                            f"Files processed: {getattr(embedder, 'files_processed', 'N/A')}, "
                            f"Chunks produced: {getattr(embedder, 'chunks_produced', 'N/A')}, "
                            f"Tokens in chunks: {getattr(embedder, 'tokens_in_chunks', 'N/A')}, "
                            f"API calls: {getattr(embedder, 'api_call_count', 'N/A')}")

                # -----------------------------------------
                # 5) Upsert to vector store
                # -----------------------------------------
                await update_progress("processing", "Preparing to store embeddings in vector database", 70)

                vector_store = build_vector_store_from_args(args, repo_manager)
                vector_store.ensure_exists()
                count_inserted = 0
                total_embeddings = 0
                embeddings_list = []

                try:
                    # Load all embeddings into memory first
                    async for metadata, embedding in embedder.download_embeddings(metadata_file):
                        # Update each document's metadata with GraphRAG and Nuanced flags
                        metadata.update({
                            "use_nuanced": use_nuanced,
                            "use_graph_rag": use_graph_rag
                        })
                        embeddings_list.append((metadata, embedding))
                        total_embeddings += 1

                    # Now process in batches
                    batch_size = 150  # Reduced from 200 to stay under Pinecone's 2MB limit
                    for i in range(0, total_embeddings, batch_size):
                        current_batch = embeddings_list[i:i + batch_size]
                        vector_store.upsert_batch(current_batch, namespace=args_dict["index_namespace"])
                        count_inserted += len(current_batch)
                        
                        # Update progress based on how many embeddings we've processed
                        progress_percentage = min(95, 70 + (count_inserted / total_embeddings * 25))
                        await update_progress(
                            "processing", 
                            f"Storing embeddings in vector database ({count_inserted}/{total_embeddings})", 
                            int(progress_percentage)
                        )

                    if count_inserted > 0:
                        await update_progress("processing", f"Completed storing {count_inserted} embeddings", 95)

                except Exception as e:
                    logger.error(f"[index_repository] Error upserting to vector store: {e}", exc_info=True)
                    raise RuntimeError(f"[index_repository] Failed to upsert embeddings to vector store: {e}")

                # -----------------------------------------
                # 6) Done, finalize
                # -----------------------------------------
                await update_progress("completed", "Indexing completed", 100)
                logger.info(f"[index_repository] Successfully indexed {count_inserted} chunks for {repo_url}")

                return {
                    "repo_url": repo_url,
                    "commit": commit_hash or "main",
                    "num_chunks": count_inserted,
                    "pinecone_index": pinecone_index,
                    "message": f"Successfully indexed {count_inserted} chunks for {repo_url}",
                    "progress": progress,
                    "metadata": base_metadata,
                    "use_nuanced": use_nuanced,
                    "use_graph_rag": use_graph_rag
                }

            except Exception as e:
                await update_progress("error", f"Error during indexing: {str(e)}", -1)
                logger.error(f"[index_repository] Indexing error: {e}", exc_info=True)
                raise

    except Exception as e:
        # Still in scope since update_progress is defined at the top level of the function
        error_message = str(e)
        # Check if this is a rate limit error and provide a clearer message
        if "rate limit exceeded" in error_message.lower():
            error_message = "GitHub API rate limit exceeded. Please try again later or use a GitHub token."
            
        await update_progress("error", f"Error during indexing: {error_message}", -1)
        logger.error(f"[index_repository] Indexing error: {e}", exc_info=True)
        raise ValueError(error_message)

async def index_web_source(
    url: str,
    allowed_patterns: List[str] = None,  # Will be mapped to allowedUrls in Firecrawl
    local_dir: str = "/tmp",
    pinecone_index: str = "web-sources",
    max_tokens: int = 800,
    overlap: int = 100,  # Keep this parameter for backward compatibility, but don't use it
    user_id: str = "unknown",
    project_id: str = "unknown",
    progress_callback: Callable = None,
    namespace: str = None,
    api_key: str = None
) -> Dict[str, Any]:
    """
    Index a web source into a vector store with optimized settings.
    
    Args:
        url: The URL of the website to index
        allowed_patterns: List of URL patterns to include in the crawl
        local_dir: Local directory to store temporary files
        pinecone_index: Name of the Pinecone index to use (default: web-sources)
        max_tokens: Maximum number of tokens per chunk
        overlap: Number of overlapping tokens between chunks (not used in current chunker implementation)
        user_id: User ID for tracking
        project_id: Project ID for tracking
        progress_callback: Optional callback for progress updates
        namespace: Optional namespace for vector store
        api_key: Firecrawl API key
        
    Returns:
        Dict with indexing results and progress information
        
    Note:
        According to current Firecrawl API (2025), the correct parameters are:
        - limit: Maximum number of pages to crawl (integer)
        - scrapeOptions: Object containing format options like {"formats": ["markdown"]}
        - excludePaths: Array of paths to exclude from crawling
        - allowBackwardLinks: Boolean to control whether to follow links outside the path
    """
    # Initialize progress tracking
    progress = {
        "stage": "initializing",
        "message": "Starting web source indexing process",
        "progress": 0,
        "url": url,
        "project_id": project_id,
        "user_id": user_id
    }
    
    # Create a unique ID for this indexing job
    job_id = str(uuid.uuid4())
    
    # Define a function to update progress
    async def update_progress(stage: str, message: str, progress_value: int, **kwargs):
        nonlocal progress
        progress.update({
            "stage": stage,
            "message": message,
            "progress": progress_value,
            **kwargs
        })
        
        if progress_callback:
            await progress_callback(progress)
        
        logger.info(f"Progress [{progress_value}%] {stage}: {message}")
    
    try:
        # Update progress
        await update_progress("initializing", "Validating web source", 5)
        
        # Validate URL format
        if not url.startswith(("http://", "https://")):
            return {
                "success": False,
                "message": "Invalid URL format. URL must start with http:// or https://",
                "progress": progress
            }
        
        # Create a temporary directory for this job
        temp_dir = os.path.join(local_dir, f"web_source_{job_id}")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Update progress
            await update_progress("downloading", f"Downloading content from {url}", 10)
            
            # Initialize FirecrawlManager
            # Make sure allowed_patterns is correctly handled based on latest Firecrawl docs
            processed_allowed_patterns = []
            if allowed_patterns and len(allowed_patterns) > 0:
                # Process patterns for compatibility with current Firecrawl API
                processed_allowed_patterns = allowed_patterns
                logger.info(f"Using allowed patterns: {processed_allowed_patterns}")
            
            data_manager = FirecrawlManager(
                url=url,
                project_id=project_id,
                allowed_patterns=processed_allowed_patterns,
                api_key=api_key,
                local_cache_dir=temp_dir
            )
            
            # Download content - use async method for better concurrency
            download_success = await data_manager.download_async()
            if not download_success:
                return {
                    "success": False,
                    "message": f"Failed to download content from {url}",
                    "progress": progress
                }
            
            # Update progress
            await update_progress("processing", "Processing downloaded content", 30)
            
            # Initialize chunker - Note: UniversalFileChunker no longer accepts overlap parameter
            chunker = UniversalFileChunker(
                max_tokens=max_tokens
            )
            
            # Initialize embedder
            embedder = build_batch_embedder_from_flags(
                data_manager=data_manager,
                chunker=chunker,
                args=SimpleNamespace(
                    local_dir=temp_dir,
                    embedding_model="text-embedding-3-small",
                    embedding_size=1536,
                    embedding_provider="openai"  # Add embedding_provider parameter
                )
            )
            
            # Update progress
            await update_progress("embedding", "Generating embeddings", 50)
            
            # Generate embeddings
            metadata_file = await embedder.embed_dataset(chunks_per_batch=100)
            
            if not embedder.embeddings_are_ready(metadata_file):
                return {
                    "success": False,
                    "message": "Failed to generate embeddings",
                    "progress": progress
                }
            
            # Update progress
            await update_progress("storing", "Storing embeddings in vector database", 70)
            
            # Initialize vector store
            vector_store = build_vector_store_from_args(
                SimpleNamespace(
                    provider=VectorStoreProvider.PINECONE.value,
                    pinecone_index=pinecone_index,
                    embedding_size=1536,
                    alpha=1,
                    vector_store_provider="pinecone",  # Add required vector_store_provider
                    embedding_provider="openai",       # Add required embedding_provider
                    embedding_model="text-embedding-3-small",  # Add required embedding_model
                    index_name=pinecone_index,         # Add required index_name
                    retrieval_alpha=1,               # Add required retrieval_alpha
                    index_namespace=namespace or f"web-sources_{user_id}_{job_id}"  # Use new isolated namespace format
                ),
                data_manager
            )
            
            # Ensure vector store exists
            vector_store.ensure_exists()
            
            # Use namespace if provided, otherwise create one with user isolation
            effective_namespace = namespace or f"web-sources_{user_id}_{job_id}"
            logger.info(f"Using web sources dedicated index: {pinecone_index}")
            logger.info(f"Using isolated namespace format: {effective_namespace}")
            
            # Store embeddings
            document_count = 0
            async for vector in embedder.download_embeddings(metadata_file):
                # Unpack the tuple (metadata, embedding) 
                metadata, embedding = vector
                
                # Update metadata with additional fields
                # Clean metadata to ensure all values are valid types for Pinecone
                cleaned_metadata = {}
                for key, value in metadata.items():
                    # Handle the favicon key that's causing the error
                    if key == 'favicon' and isinstance(value, dict) and not value:
                        # Skip empty dictionary favicon
                        continue
                    # Handle other dictionaries or complex types
                    elif isinstance(value, dict):
                        # Convert dict to string to prevent errors
                        cleaned_metadata[key] = json.dumps(value)
                    else:
                        cleaned_metadata[key] = value
                
                # Add our standard fields
                standard_fields = {
                    "user_id": user_id if user_id else "unknown",
                    "source_type": "web",
                    "source_url": url,
                    "indexed_at": time.time()
                }
                
                # Only add project_id if it's not None or "unknown" or empty string
                if project_id and project_id != "unknown" and project_id.strip() != "":
                    standard_fields["project_id"] = project_id
                
                cleaned_metadata.update(standard_fields)
                
                # Store in vector database with cleaned metadata
                vector_with_cleaned_metadata = (cleaned_metadata, embedding)
                vector_store.upsert([vector_with_cleaned_metadata], effective_namespace)
                document_count += 1
            
            # Update progress
            await update_progress(
                "completed", 
                f"Indexing completed successfully. Indexed {document_count} documents.", 
                100,
                document_count=document_count
            )
            
            return {
                "success": True,
                "message": f"Successfully indexed {url}",
                "progress": progress,
                "document_count": document_count,
                "namespace": effective_namespace
            }
            
        finally:
            # Clean up temporary directory
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.error(f"Error cleaning up temporary directory: {e}")
    
    except Exception as e:
        error_message = f"Error indexing web source {url}: {str(e)}"
        logger.error(error_message)
        
        # Update progress with error
        await update_progress("error", error_message, 0)
        
        return {
            "success": False,
            "message": error_message,
            "progress": progress
        }
