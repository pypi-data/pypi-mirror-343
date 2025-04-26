from fastapi import APIRouter, Body, HTTPException, Request
from typing import List, Dict, Any, Optional
import logging
import os
import httpx
import time
import asyncio
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
from functools import lru_cache

from user_store import get_user, create_user, update_user
from githubConfig import get_installation_token, list_installation_repos
from utils import validate_github_url

# Create separate routers for different path prefixes
github_router = APIRouter(prefix="/github", tags=["github"])
user_github_router = APIRouter(prefix="/user/github", tags=["github"])
api_router = APIRouter(prefix="/api", tags=["github"])

import threading

# Cache lock to prevent race conditions during cache operations
_cache_lock = threading.RLock()

# Cache for GitHub repo refs (branches and commits)
# Cache for 60 minutes (increased from 10 minutes)
@lru_cache(maxsize=100)
def get_cached_repo_refs(repo_short: str, token_present: bool, timestamp: str):
    """Cache key includes token_present to differentiate between authenticated and unauthenticated requests"""
    # The timestamp parameter is used to expire cache entries
    # This function never gets called directly - it's a placeholder for the cache
    return None

def update_cache_entry(repo_short: str, token_present: bool, timestamp: str, data):
    """Thread-safe method to update a specific cache entry without clearing the entire cache"""
    with _cache_lock:
        # Direct manipulation of the cache dict to update a specific entry
        cache_dict = getattr(get_cached_repo_refs, '__wrapped__').__dict__.get('__cache__', {})
        cache_key = (repo_short, token_present, timestamp)
        cache_dict[cache_key] = data
        
# Helper function to generate a timestamp for cache invalidation
# Returns a string that changes every 60 minutes (increased from 10 minutes)
def get_cache_timestamp() -> str:
    """Generate a timestamp string that changes every 60 minutes."""
    dt = datetime.now(timezone.utc)
    return f"{dt.year}-{dt.month}-{dt.day}-{dt.hour}-{dt.minute // 60}"

# GitHub API rate limit handling
async def handle_github_rate_limits(response, client):
    """Check for GitHub rate limit headers and handle rate limiting"""
    try:
        # Check if we're close to hitting rate limits
        rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", "1000"))
        rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", "0"))
        
        if rate_limit_remaining < 5:  # Getting close to the limit
            now = time.time()
            reset_time = rate_limit_reset
            wait_time = reset_time - now
            
            if wait_time > 0:
                logging.warning(f"GitHub API rate limit almost reached. Waiting {wait_time:.1f} seconds")
                try:
                    # Close client safely - it might already be closed
                    await client.aclose()
                except Exception as e:
                    logging.warning(f"Error closing client during rate limit handling: {e}")
                
                # Don't wait more than 5 minutes
                wait_time = min(wait_time, 300)
                try:
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    logging.warning(f"Sleep interrupted during rate limit handling: {e}")
                
                return True  # Indicates we waited for rate limit
        
        # Check if we've hit the rate limit (status code 403 with specific message)
        if response.status_code == 403 and "rate limit" in response.text.lower():
            now = time.time()
            reset_time = rate_limit_reset
            wait_time = reset_time - now
            
            if wait_time > 0:
                logging.warning(f"GitHub API rate limit exceeded. Waiting {wait_time:.1f} seconds")
                try:
                    # Close client safely - it might already be closed
                    await client.aclose()
                except Exception as e:
                    logging.warning(f"Error closing client during rate limit handling: {e}")
                
                # Don't wait more than 10 minutes
                wait_time = min(wait_time, 600)
                try:
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    logging.warning(f"Sleep interrupted during rate limit handling: {e}")
                
                return True  # Indicates we waited for rate limit
        
        return False  # No rate limiting necessary
    except Exception as e:
        logging.error(f"Error in rate limit handling: {e}")
        return False  # Continue execution in case of errors

# ------------------
# GITHUB INSTALLATION ENDPOINTS
# ------------------
@user_github_router.post("/installation")
async def save_github_installation(user_id: str = Body(...), installation_id: int = Body(...)):
    """Save a GitHub App installation ID for a user."""
    try:
        logging.info(f"Saving GitHub installation for user {user_id}: {installation_id}")
        user_doc = get_user(user_id)
        if not user_doc:
            logging.info(f"Creating new user document for {user_id}")
            user_doc = create_user(user_id)

        updated = update_user(user_id, {"github_installation_id": installation_id})
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update user")
        logging.info(f"Successfully saved GitHub installation for user {user_id}")
        return {"success": True, "user": updated}
    except Exception as e:
        logging.error(f"Error saving GitHub installation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@user_github_router.post("/uninstall")
async def uninstall_github_app(user_id: str = Body(...), installation_id: str = Body(...)):
    """Remove a GitHub App installation for a user."""
    try:
        logging.info(f"Removing GitHub installation for user {user_id}")
        user_doc = get_user(user_id)
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Ensure consistent type handling for installation ID
        try:
            # Try to convert input installation_id to int if possible
            # This maintains compatibility with existing code that might store it as int
            input_installation_id = int(installation_id)
        except (ValueError, TypeError):
            # If not convertible to int, keep as string
            input_installation_id = installation_id
            
        # Handle the case where github_installation_id might be None
        stored_installation_id = user_doc.get("github_installation_id")
        
        # Document explicitly what we're doing for clarity
        logging.debug(f"Installation ID comparison - stored: {stored_installation_id} ({type(stored_installation_id).__name__}), " +
                     f"input: {input_installation_id} ({type(input_installation_id).__name__})")
        
        # If no installation ID exists in the user document
        if stored_installation_id is None:
            logging.warning(f"User {user_id} does not have a GitHub installation to uninstall")
            return {"success": True, "message": "No GitHub installation found"}
        
        # First try direct comparison (handles case where types match)
        if stored_installation_id == input_installation_id:
            pass  # IDs match, proceed with uninstall
        # Then try string comparison as fallback
        elif str(stored_installation_id) == str(input_installation_id):
            logging.info(f"Installation IDs matched after string conversion")
        else:
            # Truly different values
            logging.warning(f"Installation ID mismatch for user {user_id}. Stored: {stored_installation_id}, Requested: {input_installation_id}")
            raise HTTPException(status_code=400, detail="Installation ID mismatch")

        updated = update_user(user_id, {"github_installation_id": None})
        if not updated:
            logging.error(f"Failed to update user {user_id}")
            raise HTTPException(status_code=500, detail="Failed to update user")
        logging.info(f"Successfully removed GitHub installation for user {user_id}")
        return {"success": True}
    except Exception as e:
        logging.error(f"Error removing GitHub installation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@github_router.get("/list-repos")
async def list_github_repos(user_id: str):
    """List repositories available to the user through their GitHub App installation."""
    try:
        user_doc = get_user(user_id)
        if not user_doc or not user_doc.get("github_installation_id"):
            # Return empty list for missing or no installation
            return {"repositories": []}
        try:
            # Get installation token synchronously
            installation_id = user_doc["github_installation_id"]
            token = get_installation_token(installation_id)
            
            repos = list_installation_repos(token)
            return {
                "repositories": [
                    {
                        "full_name": repo["full_name"],
                        "name": repo["name"],
                        "private": repo["private"],
                        "url": repo["html_url"],
                        "clone_url": repo["clone_url"],
                        "description": repo.get("description"),
                        "default_branch": repo["default_branch"],
                        "size": repo["size"],
                        "language": repo.get("language")
                    }
                    for repo in repos
                ]
            }
        except Exception as e:
            logging.error(f"Failed to list repositories: {e}")
            return {"repositories": []}
    except Exception as e:
        logging.error(f"Error in list_github_repos: {e}")
        return {"repositories": []}

# ------------------
# REPOSITORY INFORMATION
# ------------------
@api_router.get("/projects/{project_id}/repo-refs")
async def get_project_repo_refs(project_id: str, user_id: str):
    """
    Return all branches and the 50 most recent commits for a project's GitHub repository.
    With caching and rate limit handling.
    """
    from project_store import get_project
    
    # 1) Fetch the project
    proj = get_project(project_id, user_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2) Parse the GitHub org/repo from the project's repoUrl
    repo_url = proj["repoUrl"]
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")
    repo_short = repo_url.replace("https://github.com/", "").replace(".git", "")

    # 3) Get the GitHub token (from user's installation if available)
    user_doc = get_user(user_id)
    if not user_doc or not user_doc.get("github_installation_id"):
        raise HTTPException(
            status_code=400,
            detail="GitHub App installation required. Please install the GitHub App to continue."
        )
    
    # Always require a token - no exception handling to allow fallback
    installation_id = user_doc["github_installation_id"]
    github_token = get_installation_token(installation_id)
    if not github_token:
        raise HTTPException(
            status_code=401,
            detail="Failed to get GitHub token. Please reinstall the GitHub App."
        )
    
    # Check cache first using the helper function for timestamp
    cache_timestamp = get_cache_timestamp()
    
    # Thread-safe cache lookup
    with _cache_lock:
        cached_result = get_cached_repo_refs(repo_short, True, cache_timestamp)
        if cached_result is not None:
            logging.info(f"Using cached repo refs for {repo_short}")
            return cached_result
    
    # 4) Use GitHub API to fetch branches & commits - always with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}"
    }
    
    # Implementation with rate limit handling
    all_branches = []
    commits_list = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Fetch all branches with pagination and rate limit handling
        page = 1
        per_page = 100  # GitHub's max per page
        retry_count = 0
        max_retries = 3
        
        while True:
            if retry_count >= max_retries:
                logging.error(f"Max retries reached while fetching branches")
                break
                
            try:
                branches_resp = await client.get(
                    f"https://api.github.com/repos/{repo_short}/branches",
                    params={
                        "page": page,
                        "per_page": per_page
                    },
                    headers=headers
                )
                
                # Check for rate limits
                if await handle_github_rate_limits(branches_resp, client):
                    retry_count += 1
                    continue  # Retry after waiting for rate limit
                
                if branches_resp.status_code == 404:
                    raise HTTPException(status_code=404, detail="Repository not found")
                elif branches_resp.status_code != 200:
                    logging.error(f"Failed to fetch branches: {branches_resp.status_code}, {branches_resp.text}")
                    retry_count += 1
                    backoff_time = 2 ** retry_count
                    await asyncio.sleep(backoff_time)
                    continue
                
                branches_data = branches_resp.json()
                if not branches_data:  # No more branches
                    break
                
                # Add branches from this page
                all_branches.extend([
                    {
                        "name": b["name"],
                        "commitSha": b["commit"]["sha"] if b.get("commit") else None,
                        "protected": b.get("protected", False),
                    }
                    for b in branches_data
                ])
                
                if len(branches_data) < per_page:  # Last page
                    break
                
                page += 1
                retry_count = 0  # Reset retry counter on successful request
                
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logging.error(f"Network error fetching branches: {e}")
                retry_count += 1
                backoff_time = 2 ** retry_count
                await asyncio.sleep(backoff_time)
        
        # Sort branches alphabetically for better UX
        all_branches.sort(key=lambda x: x["name"].lower())
        
        # Fetch 50 most recent commits with retry and rate limit handling
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                commits_resp = await client.get(
                    f"https://api.github.com/repos/{repo_short}/commits",
                    params={
                        "per_page": 50,
                        "sort": "committer-date",
                        "order": "desc"
                    },
                    headers=headers
                )
                
                # Check for rate limits
                if await handle_github_rate_limits(commits_resp, client):
                    retry_count += 1
                    continue  # Retry after waiting for rate limit
                
                if commits_resp.status_code == 404:
                    raise HTTPException(status_code=404, detail="Repository not found")
                elif commits_resp.status_code != 200:
                    logging.error(f"Failed to fetch commits: {commits_resp.status_code}, {commits_resp.text}")
                    retry_count += 1
                    backoff_time = 2 ** retry_count
                    await asyncio.sleep(backoff_time)
                    continue
                
                commits_data = commits_resp.json()
                commits_list = [
                    {
                        "sha": commit["sha"],
                        "message": commit["commit"]["message"].split("\n")[0]  # first line only
                    }
                    for commit in commits_data
                ]
                break  # Success, exit retry loop
                
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logging.error(f"Network error fetching commits: {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    logging.error(f"Max retries reached while fetching commits")
                    # Return with whatever branches we have, but empty commits
                    commits_list = []
                    break
                backoff_time = 2 ** retry_count
                await asyncio.sleep(backoff_time)
        
        # Store result in cache and return
        result = {
            "branches": all_branches,
            "commits": commits_list
        }
        
        # Update only this specific cache entry without clearing the entire cache
        update_cache_entry(repo_short, True, cache_timestamp, result)
        
        return result

# GitHub webhook endpoint
@api_router.post("/github/webhook")
async def github_webhook(request: Request):
    """Handle GitHub webhook events."""
    try:
        # Get the webhook payload
        payload = await request.json()
        event_type = request.headers.get("X-GitHub-Event")
        
        # Log the webhook event
        logging.info(f"Received GitHub webhook event: {event_type}")
        
        if event_type == "installation":
            # Handle installation events
            action = payload.get("action")
            installation = payload.get("installation", {})
            installation_id = installation.get("id")
            account = installation.get("account", {})
            user_login = account.get("login")
            
            logging.info(f"Installation event: {action} for {user_login}, id={installation_id}")
            
            if action == "created" or action == "added":
                # New installation created - we'll save it when the user logs in
                logging.info(f"GitHub App installed for {user_login} with installation_id {installation_id}")
                return {"status": "success", "message": "Installation received"}
                
            elif action == "deleted":
                # Installation was deleted - we should update user records
                logging.info(f"GitHub App uninstalled for {user_login}")
                # Find users with this installation ID and reset their GitHub connection
                # This is more complex as we'd need to find users by installation ID, but we'll do it async
                return {"status": "success", "message": "Uninstallation received"}
                
        elif event_type == "installation_repositories":
            # Handle repository addition/removal events
            action = payload.get("action")
            installation = payload.get("installation", {})
            installation_id = installation.get("id")
            
            logging.info(f"Installation repositories event: {action} for installation {installation_id}")
            return {"status": "success", "message": "Repository event received"}
            
        # Return a generic success response for all other events
        return {"status": "success", "event": event_type}
        
    except Exception as e:
        logging.error(f"Error processing GitHub webhook: {e}")
        return {"status": "error", "message": str(e)}


# Export all routers to be included in main.py
router = [github_router, user_github_router, api_router]