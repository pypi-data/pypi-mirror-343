"""Utility classes to maniuplate GitHub repositories and external data sources."""

import logging
import os
import json
import tempfile
import time
import asyncio
import uuid
from abc import abstractmethod
from functools import cached_property
from typing import Any, Dict, Generator, Tuple, List, Optional

import requests
from git import GitCommandError, Repo


class DataManager:
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id

    @abstractmethod
    def download(self) -> bool:
        """Downloads the data from a remote location."""

    @abstractmethod
    def walk(self) -> Generator[Tuple[Any, Dict], None, None]:
        """Yields a tuple of (data, metadata) for each data item in the dataset."""


class GitHubRepoManager(DataManager):
    """Class to manage a local clone of a GitHub repository."""

    def __init__(
        self,
        repo_id: str,
        commit_hash: str = None,
        access_token: str = None,
        local_dir: str = None,
        inclusion_file: str = None,
        exclusion_file: str= "sample-exclude.txt",
    ):
        """
        Args:
            repo_id: The identifier of the repository in owner/repo format, e.g. "Storia-AI/sage".
            commit_hash: Optional commit hash to checkout. If not specified, we pull the latest version of the repo.
            access_token: A GitHub access token to use for cloning private repositories. Not needed for public repos.
            local_dir: The local directory where the repository will be cloned.
            inclusion_file: A file with a lists of files/directories/extensions to include. Each line must be in one of
                the following formats: "ext:.my-extension", "file:my-file.py", or "dir:my-directory".
            exclusion_file: A file with a lists of files/directories/extensions to exclude. Each line must be in one of
                the following formats: "ext:.my-extension", "file:my-file.py", or "dir:my-directory".
        """
        super().__init__(dataset_id=repo_id)
        self.repo_id = repo_id
        self.commit_hash = commit_hash
        self.access_token = access_token

        self.local_dir = local_dir or "/tmp/"
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)
        self.local_path = os.path.join(self.local_dir, repo_id)

        self.log_dir = os.path.join(self.local_dir, "logs", repo_id)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        if inclusion_file and exclusion_file:
            raise ValueError("Only one of inclusion_file or exclusion_file should be provided.")

        self.inclusions = self._parse_filter_file(inclusion_file) if inclusion_file else None
        self.exclusions = self._parse_filter_file(exclusion_file) if exclusion_file else None

    @cached_property
    def is_public(self) -> bool:
        """Checks whether a GitHub repository is publicly visible."""
        # Only check using authentication
        if not self.access_token:
            raise ValueError("Authentication token required to check repository visibility")
        
        headers = {"Authorization": f"token {self.access_token}"}
        response = requests.get(f"https://api.github.com/repos/{self.repo_id}", headers=headers, timeout=10)
        # Note that the response will be 404 for both private and non-existent repos.
        return response.status_code == 200

    @cached_property
    def default_branch(self) -> str:
        """Fetches the default branch of the repository from GitHub."""
        # Always require token
        if not self.access_token:
            raise ValueError("Authentication token required to fetch repository information")
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.access_token}"
        }

        try:
            response = requests.get(f"https://api.github.com/repos/{self.repo_id}", headers=headers, timeout=10)
            if response.status_code == 200:
                branch = response.json().get("default_branch")
                if not branch:
                    raise ValueError("Repository exists but no default branch found")
                return branch
            elif response.status_code == 404:
                raise ValueError(f"Repository {self.repo_id} not found")
            else:
                raise ValueError(f"Failed to fetch repository info: {response.text}")
        except Exception as e:
            logging.error(f"Error fetching default branch for {self.repo_id}: {str(e)}")
            raise ValueError(f"Failed to determine default branch: {str(e)}")

    def download(self) -> bool:
        """Clones the repository to the local directory, if it's not already cloned."""
        if os.path.exists(self.local_path):
            # The repository is already cloned.
            return True

        try:
            # First check if repo exists and is accessible
            try:
                is_public = self.is_public
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to check if repository is public: {str(e)}")
                # If we can't check, assume it's private
                is_public = False

            if not is_public and not self.access_token:
                raise ValueError(f"Repository {self.repo_id} is private or doesn't exist")

            # For public repos, use simple HTTPS URL
            # For private repos or when token is provided, use token auth
            if self.access_token:
                clone_url = f"https://x-access-token:{self.access_token}@github.com/{self.repo_id}.git"
            else:
                clone_url = f"https://github.com/{self.repo_id}.git"

            # Set GIT_LFS_SKIP_SMUDGE=1 to skip downloading LFS files
            os.environ["GIT_LFS_SKIP_SMUDGE"] = "1"
            
            try:
                logging.info(f"Attempting to clone {self.repo_id} (public: {is_public})")
                # Always clone with --no-single-branch to ensure we can access all branches
                repo = Repo.clone_from(clone_url, self.local_path, no_single_branch=True)
                
                if self.commit_hash:
                    try:
                        # First try to fetch the branch/commit
                        repo.git.fetch('origin', self.commit_hash)
                        # Then try to checkout
                        repo.git.checkout(self.commit_hash)
                        logging.info(f"Successfully checked out {self.commit_hash}")
                    except GitCommandError as e:
                        logging.error(f"Failed to checkout {self.commit_hash}, falling back to default branch: {e}")
                        # If checkout fails, we still have the repo cloned with default branch
                
                logging.info(f"Successfully cloned {self.repo_id}")
                return True
                
            except GitCommandError as e:
                error_msg = str(e)
                if "Authentication failed" in error_msg:
                    logging.error(f"Authentication failed for {self.repo_id}. Repository might be private.")
                    return False
                elif "Repository not found" in error_msg:
                    logging.error(f"Repository {self.repo_id} not found")
                    return False
                else:
                    logging.error(f"Failed to clone {self.repo_id}: {error_msg}")
                    return False
            finally:
                # Reset the environment variable
                if "GIT_LFS_SKIP_SMUDGE" in os.environ:
                    del os.environ["GIT_LFS_SKIP_SMUDGE"]
                
        except Exception as e:
            logging.error(f"Error in download for {self.repo_id}: {str(e)}")
            return False

    def _parse_filter_file(self, file_path: str) -> bool:
        """Parses a file with files/directories/extensions to include/exclude.

        Lines are expected to be in the format:
        # Comment that will be ignored, or
        ext:.my-extension, or
        file:my-file.py, or
        dir:my-directory
        """
        with open(file_path, "r") as f:
            lines = f.readlines()

        parsed_data = {"ext": [], "file": [], "dir": []}
        for line in lines:
            if line.startswith("#"):
                # This is a comment line.
                continue
            key, value = line.strip().split(":")
            if key in parsed_data:
                parsed_data[key].append(value)
            else:
                logging.error("Unrecognized key in line: %s. Skipping.", line)

        return parsed_data

    def _should_include(self, file_path: str) -> bool:
        """Checks whether the file should be indexed."""
        # Exclude symlinks.
        if os.path.islink(file_path):
            return False

        # Exclude hidden files and directories.
        if any(part.startswith(".") for part in file_path.split(os.path.sep)):
            return False

        if not self.inclusions and not self.exclusions:
            return True

        # Filter based on file extensions, file names and directory names.
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        file_name = os.path.basename(file_path)
        dirs = os.path.dirname(file_path).split("/")

        if self.inclusions:
            return (
                extension in self.inclusions.get("ext", [])
                or file_name in self.inclusions.get("file", [])
                or any(d in dirs for d in self.inclusions.get("dir", []))
            )
        elif self.exclusions:
            return (
                extension not in self.exclusions.get("ext", [])
                and file_name not in self.exclusions.get("file", [])
                and all(d not in dirs for d in self.exclusions.get("dir", []))
            )
        return True

    def walk(self, get_content: bool = True) -> Generator[Tuple[Any, Dict], None, None]:
        """Walks the local repository path and yields a tuple of (content, metadata) for each file.
        The filepath is relative to the root of the repository (e.g. "org/repo/your/file/path.py").

        Args:
            get_content: When set to True, yields (content, metadata) tuples. When set to False, yields metadata only.
        """
        # We will keep appending to these files during the iteration, so we need to clear them first.
        repo_name = self.repo_id.replace("/", "_")
        included_log_file = os.path.join(self.log_dir, f"included_{repo_name}.txt")
        excluded_log_file = os.path.join(self.log_dir, f"excluded_{repo_name}.txt")
        if os.path.exists(included_log_file):
            os.remove(included_log_file)
            logging.info("Logging included files at %s", included_log_file)
        if os.path.exists(excluded_log_file):
            os.remove(excluded_log_file)
            logging.info("Logging excluded files at %s", excluded_log_file)

        for root, _, files in os.walk(self.local_path):
            file_paths = [os.path.join(root, file) for file in files]
            included_file_paths = [f for f in file_paths if self._should_include(f)]

            with open(included_log_file, "a") as f:
                for path in included_file_paths:
                    f.write(path + "\n")

            excluded_file_paths = set(file_paths).difference(set(included_file_paths))
            with open(excluded_log_file, "a") as f:
                for path in excluded_file_paths:
                    f.write(path + "\n")

            for file_path in included_file_paths:
                relative_file_path = file_path[len(self.local_dir) + 1 :]
                metadata = {
                    "file_path": relative_file_path,
                    "url": self.url_for_file(relative_file_path),
                }

                if not get_content:
                    yield metadata
                    continue

                contents = self.read_file(relative_file_path)
                if contents:
                    yield contents, metadata

    def url_for_file(self, file_path: str) -> str:
        """Converts a repository file path to a GitHub link."""
        file_path = file_path[len(self.repo_id) + 1 :]
        branch_or_commit = self.commit_hash or self.default_branch
        return f"https://github.com/{self.repo_id}/blob/{branch_or_commit}/{file_path}"

    def read_file(self, relative_file_path: str) -> str:
        """Reads the contents of a file in the repository."""
        absolute_file_path = os.path.join(self.local_dir, relative_file_path)
        with open(absolute_file_path, "r") as f:
            try:
                contents = f.read()
                return contents
            except UnicodeDecodeError:
                logging.warning("Unable to decode file %s.", absolute_file_path)
                return None

    def from_args(args: Dict):
        """Creates a GitHubRepoManager from command-line arguments and clones the underlying repository."""
        repo_manager = GitHubRepoManager(
            repo_id=args.repo_id,
            commit_hash=args.commit_hash,
            access_token=args.get("github_token"),  # Use passed token instead of env var
            local_dir=args.local_dir,
            inclusion_file=args.include,
            exclusion_file=args.exclude,
        )
        success = repo_manager.download()
        if not success:
            raise ValueError(
                f"Unable to clone {args.repo_id}. Please check that it exists and you have access to it. "
                "For private repositories, you need to install the GitHub App."
            )
        return repo_manager


class FirecrawlManager(DataManager):
    """
    Manages web content crawled via FireCrawl API.
    Responsible for fetching web content and preparing it for indexing.
    
    Optimized for multi-user concurrent access with proper rate limiting.
    """
    
    # Class-level rate limiter to ensure API isn't overloaded
    # These are shared across all instances to prevent API throttling
    _last_api_call = 0
    _min_api_interval = 0.5  # seconds between API calls
    _api_semaphore = None  # Will be initialized on first use
    
    def __init__(
        self,
        url: str,
        project_id: str,
        allowed_patterns: List[str] = None,
        api_key: str = os.getenv("FIRECRAWL_API_KEY"),
        local_cache_dir: str = None,
    ):
        """
        Initialize the FirecrawlManager.
        
        Args:
            url: The URL to scrape
            project_id: Project ID to associate the data with
            allowed_patterns: URL patterns to include in the scrape
            api_key: Firecrawl API key (defaults to env var)
            local_cache_dir: Directory to cache scraped content
        """
        # Sanitize URL for use as dataset_id - remove protocol and replace special chars
        sanitized_url = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
        super().__init__(dataset_id=sanitized_url)
        
        self.url = url
        self.project_id = project_id
        self.allowed_patterns = allowed_patterns or []
        self.api_key = api_key
        self.local_cache_dir = local_cache_dir or tempfile.mkdtemp()
        
        # Create unique request ID for tracking
        self.request_id = str(uuid.uuid4())[:8]
        
        # Log initialization info
        logging.info(f"[{self.request_id}] Initialized FirecrawlManager for URL: {url}")
        if self.allowed_patterns:
            logging.info(f"[{self.request_id}] Using allowed patterns: {self.allowed_patterns}")
        
        # Initialize API semaphore if needed
        if FirecrawlManager._api_semaphore is None:
            # Allow up to 3 concurrent API calls - adjust based on API provider's limits
            FirecrawlManager._api_semaphore = asyncio.Semaphore(3)
        
        # Import here to avoid dependency issues if Firecrawl SDK is not installed
        try:
            from firecrawl import FirecrawlApp
            self.firecrawl = FirecrawlApp(api_key=self.api_key)
        except ImportError:
            logging.error(f"[{self.request_id}] Firecrawl SDK not installed. Run 'pip install firecrawl-py'")
            self.firecrawl = None
        
    async def _rate_limited_api_call(self, func_name, *args, **kwargs):
        """
        Execute an API call with rate limiting.
        This method ensures we don't overwhelm the API by using semaphores and time delays.
        
        Args:
            func_name: Name of the API function to call
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            The API call result
        """
        # Get the function from the firecrawl instance
        api_func = getattr(self.firecrawl, func_name)
        
        # Acquire semaphore to limit concurrent API calls
        async with FirecrawlManager._api_semaphore:
            # Calculate time since last API call
            now = time.time()
            time_since_last_call = now - FirecrawlManager._last_api_call
            
            # Sleep if we need to wait for rate limit
            if time_since_last_call < FirecrawlManager._min_api_interval:
                wait_time = FirecrawlManager._min_api_interval - time_since_last_call
                logging.debug(f"[{self.request_id}] Rate limiting: waiting {wait_time:.2f}s before API call")
                await asyncio.sleep(wait_time)
            
            # Update last call time
            FirecrawlManager._last_api_call = time.time()
            
            # Make the API call
            try:
                if asyncio.iscoroutinefunction(api_func):
                    result = await api_func(*args, **kwargs)
                else:
                    # Run blocking API call in a thread pool
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        None, lambda: api_func(*args, **kwargs)
                    )
                return result
            except Exception as e:
                logging.error(f"[{self.request_id}] API call error ({func_name}): {e}")
                raise
    
    async def download_async(self) -> bool:
        """
        Async version of download method for better concurrency.
        Scrape the website using FireCrawl API and cache the markdown locally.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.firecrawl:
            logging.error(f"[{self.request_id}] Firecrawl SDK not initialized")
            return False
            
        try:
            logging.info(f"[{self.request_id}] Scraping URL: {self.url}")
            
            # Use scrape endpoint for single URL with rate limiting
            result = await self._rate_limited_api_call(
                "scrape_url", 
                self.url,
                params={
                    "formats": ["markdown", "html"],  # Get both formats for flexibility
                }
            )
            
            # Save scrape results to local cache
            os.makedirs(self.local_cache_dir, exist_ok=True)
            
            # Handle single page result
            page_path = os.path.join(self.local_cache_dir, "page.json")
            with open(page_path, "w") as f:
                json.dump(result, f)
                
            # If URL patterns are provided, also crawl those specific subpages
            if self.allowed_patterns and len(self.allowed_patterns) > 0:
                logging.info(f"[{self.request_id}] Crawling subpages with patterns: {self.allowed_patterns}")
                
                try:
                    # Use the crawl endpoint with updated API parameters
                    crawl_result = await self._rate_limited_api_call(
                        "crawl_url",
                        self.url,
                        params={
                            "limit": 50,  # Controls max number of pages to crawl
                            "scrapeOptions": {
                                "formats": ["markdown"]
                            },
                            "allowBackwardLinks": True,
                        },
                        poll_interval=30  # Wait for results with polling
                    )
                    
                    # Handle different response format based on Firecrawl docs
                    if isinstance(crawl_result, dict) and "data" in crawl_result:
                        # New format has a data array
                        for i, page in enumerate(crawl_result.get("data", [])):
                            subpage_path = os.path.join(self.local_cache_dir, f"subpage_{i}.json")
                            with open(subpage_path, "w") as f:
                                json.dump(page, f)
                        logging.info(f"[{self.request_id}] Successfully saved {len(crawl_result.get('data', []))} subpages")
                    elif isinstance(crawl_result, dict) and "pages" in crawl_result:
                        # Fallback for old format
                        for i, page in enumerate(crawl_result["pages"]):
                            subpage_path = os.path.join(self.local_cache_dir, f"subpage_{i}.json")
                            with open(subpage_path, "w") as f:
                                json.dump(page, f)
                        logging.info(f"[{self.request_id}] Successfully saved {len(crawl_result.get('pages', []))} subpages (old format)")
                    else:
                        logging.warning(f"[{self.request_id}] Unexpected crawl result format: {type(crawl_result)}")
                        
                except Exception as e:
                    logging.error(f"[{self.request_id}] Crawl error: {e}")
                    error_msg = str(e)
                    
                    # Try alternate format if parameters might have changed
                    if "unrecognized_keys" in error_msg.lower() or "bad request" in error_msg.lower():
                        logging.warning(f"[{self.request_id}] Trying alternate crawl parameter format...")
                        try:
                            # Try with even simpler parameters
                            crawl_result = await self._rate_limited_api_call(
                                "crawl_url",
                                self.url,
                                params={
                                    "limit": 50,
                                    "scrapeOptions": {"formats": ["markdown"]},
                                },
                                poll_interval=30
                            )
                            
                            # Save the results
                            if isinstance(crawl_result, dict) and "data" in crawl_result:
                                for i, page in enumerate(crawl_result.get("data", [])):
                                    subpage_path = os.path.join(self.local_cache_dir, f"subpage_{i}.json")
                                    with open(subpage_path, "w") as f:
                                        json.dump(page, f)
                                logging.info(f"[{self.request_id}] Successfully crawled with simplified parameters")
                            else:
                                logging.warning(f"[{self.request_id}] Unexpected crawl result format: {type(crawl_result)}")
                        except Exception as e2:
                            logging.error(f"[{self.request_id}] Second crawl attempt also failed: {e2}")
                            
                            # Make a final attempt with absolute minimum parameters
                            try:
                                logging.warning(f"[{self.request_id}] Making final attempt with minimum parameters")
                                crawl_result = await self._rate_limited_api_call(
                                    "crawl_url",
                                    self.url,
                                    params={"limit": 10},  # Lower limit for safety
                                    poll_interval=30
                                )
                                
                                if isinstance(crawl_result, dict) and "data" in crawl_result:
                                    for i, page in enumerate(crawl_result.get("data", [])):
                                        subpage_path = os.path.join(self.local_cache_dir, f"subpage_{i}.json")
                                        with open(subpage_path, "w") as f:
                                            json.dump(page, f)
                                    logging.info(f"[{self.request_id}] Final minimal crawl attempt succeeded")
                                    return True
                            except Exception as e3:
                                logging.error(f"[{self.request_id}] Final crawl attempt also failed: {e3}")
                                logging.warning(f"[{self.request_id}] Continuing with just the main page results")
                    else:
                        # Don't fail the entire process if just the crawling part fails
                        logging.warning(f"[{self.request_id}] Continuing with just the main page results")
            
            return True
        except Exception as e:
            logging.error(f"[{self.request_id}] Error downloading content from {self.url}: {e}")
            return False
    
    def download(self) -> bool:
        """
        Synchronous version of download method (for backward compatibility).
        Creates an event loop to run the async version.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create event loop if needed
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # No event loop in current thread, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            # Run the async version
            return loop.run_until_complete(self.download_async())
        except Exception as e:
            logging.error(f"[{self.request_id}] Error in download: {e}")
            return False
            
    def walk(self, get_content: bool = True) -> Generator[Tuple[str, Dict], None, None]:
        """
        Yields markdown content from the cached scrape results with metadata.
        
        Args:
            get_content: Whether to include the content in the results
            
        Yields:
            tuple: (content, metadata)
        """
        if not os.path.exists(self.local_cache_dir):
            logging.warning(f"Cache directory does not exist: {self.local_cache_dir}")
            return
            
        for filename in os.listdir(self.local_cache_dir):
            if not filename.endswith(".json"):
                continue
                
            file_path = os.path.join(self.local_cache_dir, filename)
            try:
                with open(file_path, "r") as f:
                    page_data = json.load(f)
                
                content = page_data.get("markdown", "")
                metadata = page_data.get("metadata", {})
                
                # Add source info to metadata
                if "sourceURL" not in metadata:
                    metadata["sourceURL"] = self.url
                    
                # Add additional metadata for tracking
                metadata["source_type"] = "web"
                metadata["file_path"] = metadata.get("sourceURL", self.url)  # Use URL as file path for consistency
                
                # Safely add project_id only if it's valid
                if self.project_id and self.project_id != "unknown" and str(self.project_id).strip() != "":
                    metadata["project_id"] = self.project_id
                
                # Use title as document name if available
                if "title" in metadata:
                    metadata["document_name"] = metadata["title"]
                else:
                    metadata["document_name"] = os.path.basename(metadata.get("sourceURL", self.url))
                
                yield content, metadata
            except Exception as e:
                logging.error(f"Error processing cached content from {file_path}: {e}")