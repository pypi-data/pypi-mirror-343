from fastapi import APIRouter, HTTPException, Body, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import uuid4
import logging
import os
import httpx
from urllib.parse import urlparse

from models import CommunityRepoCreate
from community_repo_store import (
    create_community_repo,
    get_community_repo,
    list_community_repos,
    update_community_repo,
    delete_community_repo
)
from user_store import get_user
from project_store import create_project, update_project
from chat_store import create_new_chat
from index import index_repository
from githubConfig import get_installation_token

# Create router with prefix
router = APIRouter(prefix="/community-repos", tags=["community"])

class CommunityRepoChatRequest(BaseModel):
    user_id: str

@router.get("")
async def list_community_repositories():
    """List all indexed community repositories."""
    try:
        repos = list_community_repos()
        return {"repositories": [repo.model_dump() for repo in repos]}
    except Exception as e:
        logging.error(f"Error listing community repos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_github_metadata(repo_url: str, github_token: Optional[str] = None) -> dict:
    """Fetch GitHub repository metadata."""
    try:
        # Extract owner/repo from URL
        parsed = urlparse(repo_url)
        path_parts = [p for p in parsed.path.split('/') if p]
        if len(path_parts) != 2:
            raise ValueError("Invalid GitHub URL format")
        owner, repo = path_parts

        headers = {}
        if github_token:
            headers["Authorization"] = f"token {github_token}"

        async with httpx.AsyncClient() as client:
            # Fetch repository data
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch repository metadata"
                )
            
            repo_data = response.json()
            
            # Extract relevant metadata
            metadata = {
                "stars": repo_data.get("stargazers_count", 0),
                "language": repo_data.get("language"),
                "description": repo_data.get("description"),
                "fork_count": repo_data.get("forks_count", 0),
                "open_issues_count": repo_data.get("open_issues_count", 0),
                "watchers_count": repo_data.get("watchers_count", 0),
                "default_branch": repo_data.get("default_branch"),
                "license": repo_data.get("license", {}).get("name"),
                "topics": repo_data.get("topics", []),
                "owner": {
                    "login": repo_data.get("owner", {}).get("login"),
                    "avatar_url": repo_data.get("owner", {}).get("avatar_url"),
                    "html_url": repo_data.get("owner", {}).get("html_url")
                },
                "github_updated_at": repo_data.get("updated_at"),
                "github_metadata": repo_data  # Store full metadata for future use
            }
            
            return metadata

    except Exception as e:
        logging.error(f"Error fetching GitHub metadata: {e}")
        return {}

def validate_github_url(url: str):
    """Validate GitHub URL format."""
    try:
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            return False, None, "Invalid GitHub repository URL"
        
        path_parts = [p for p in parsed.path.split('/') if p]
        if len(path_parts) < 2:
            return False, None, "Invalid GitHub repository URL format"
        
        owner, repo = path_parts[0], path_parts[1]
        normalized_url = f"https://github.com/{owner}/{repo}"
        
        return True, normalized_url, None
    except Exception as e:
        return False, None, f"Invalid URL: {str(e)}"

@router.post("")
async def create_community_repository(
    repo_data: CommunityRepoCreate,
    user_id: str = Body(...),
    user_email: str = Body(...),
):
    """Create and index a new community repository. Only admin can do this."""
    try:
        # Check if user is admin using email
        if user_email != os.getenv("ADMIN_EMAIL"):
            raise HTTPException(status_code=403, detail="Only admin can create community repos")

        # Validate repository URL
        is_valid, normalized_url, error = validate_github_url(repo_data.repo_url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        # Update repo_data with normalized URL
        repo_data.repo_url = normalized_url

        # Get GitHub token from user installation - recommended for admin to install GitHub App
        github_token = None
        user_doc = get_user(user_id)
        if user_doc and user_doc.get("github_installation_id"):
            try:
                github_token = get_installation_token(user_doc["github_installation_id"])
                logging.info(f"Using GitHub App installation token for admin user {user_id}")
            except Exception as e:
                logging.error(f"Failed to get installation token: {e}")
                logging.warning("Proceeding without GitHub token - may hit rate limits")
        else:
            logging.warning(f"No GitHub installation found for admin user {user_id}")
            logging.warning("Proceeding without GitHub token - may hit rate limits")

        # Fetch GitHub metadata
        metadata = await fetch_github_metadata(normalized_url, github_token)
        
        # Create a new dictionary with flattened metadata structure
        repo_data_dict = repo_data.model_dump()
        
        # If no description was provided, use the GitHub description
        if not repo_data_dict.get("description") and metadata.get("description"):
            repo_data_dict["description"] = metadata.get("description")
            
        # Update with flattened metadata
        repo_data_dict.update({
            "stars": metadata.get("stars", 0),
            "language": metadata.get("language"),
            "fork_count": metadata.get("fork_count", 0),
            "open_issues_count": metadata.get("open_issues_count", 0),
            "watchers_count": metadata.get("watchers_count", 0),
            "default_branch": metadata.get("default_branch"),
            "license": metadata.get("license"),
            "topics": metadata.get("topics", []),
            "owner": metadata.get("owner"),
            "github_updated_at": metadata.get("github_updated_at"),
            "github_metadata": metadata  # Store full metadata for future use
        })

        # Create repo with flattened metadata
        repo = create_community_repo(CommunityRepoCreate(**repo_data_dict))

        # Create a single project for this community repo
        project_id = str(uuid4())
        project = create_project(
            project_id=project_id,
            name=repo.name,
            repoUrl=normalized_url,  # Use normalized URL
            user_id=user_id,  # Admin user is the owner
            status="indexing",
            is_community=True,
            branch_or_commit=metadata.get("default_branch")  # Store the default branch
        )

        # Start indexing in background
        try:
            result = await index_repository(
                repo_url=f"{normalized_url}.git",  # Add .git for cloning
                commit_hash=metadata.get("default_branch"),  # Use default branch from GitHub
                local_dir=f"/tmp/community_repo_{repo.id}",
                pinecone_index=os.getenv("COMMUNITY_INDEX_NAME", "community-repos"),
                user_id=user_id,
                project_id=project_id,  # Use the single project ID
                namespace=f"{user_id}/{project_id}"  # Use user_id/project_id format for namespace
            )

            if result["progress"]["stage"] == "completed":
                update_community_repo(
                    repo.id,
                    {
                        "status": "indexed",
                        "is_indexed": True,
                        "indexing_progress": result["progress"],
                        "project_id": project_id,  # Store the project ID
                        "branch": metadata.get("default_branch")  # Store the branch
                    }
                )
                # Also update the project
                update_project(
                    project_id,
                    user_id,
                    status="indexed",
                    is_indexed=True,
                    branch_or_commit=metadata.get("default_branch")  # Store the branch
                )
            elif result["progress"]["stage"] == "error":
                update_community_repo(
                    repo.id,
                    {
                        "status": "error",
                        "indexing_progress": result["progress"]
                    }
                )
                update_project(
                    project_id,
                    user_id,
                    status="error"
                )

        except Exception as e:
            logging.error(f"Error indexing community repo: {e}")
            update_community_repo(
                repo.id,
                {
                    "status": "error",
                    "indexing_progress": {
                        "stage": "error",
                        "message": str(e),
                        "progress": -1
                    }
                }
            )
            update_project(
                project_id,
                user_id,
                status="error"
            )
            raise HTTPException(status_code=500, detail=f"Failed to index repository: {str(e)}")

        return repo.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating community repo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{repo_id}/chat")
async def create_community_repo_chat(
    repo_id: str,
    request: CommunityRepoChatRequest
):
    """Create a new chat for a community repository, reusing the existing indexed project."""
    try:
        # Get community repo
        repo = get_community_repo(repo_id)
        if not repo:
            raise HTTPException(status_code=404, detail="Community repository not found")

        if not repo.is_indexed:
            raise HTTPException(
                status_code=400,
                detail="Repository is not indexed yet"
            )

        # Get the existing project ID from the community repo
        community_project_id = getattr(repo, "project_id", None)
        if not community_project_id:
            raise HTTPException(status_code=500, detail="No project_id set on community repo")

        # Get the admin's user ID (who indexed the repo)
        admin_user_id = os.getenv("ADMIN_USER_ID")
        if not admin_user_id:
            raise HTTPException(status_code=500, detail="Admin user ID not configured")

        # Create a new chat using the existing project
        chat_id = create_new_chat(
            project_id=community_project_id,
            user_id=request.user_id,
            title=f"Chat with {repo.name}"
        )

        # Update project to ensure it's marked as a community repo and has branch info
        update_project(
            project_id=community_project_id,
            user_id=admin_user_id,  # Use admin's user ID since they own the project
            is_community=True,  # Ensure this flag is set
            branch_or_commit=getattr(repo, "branch", None)  # Pass the branch info
        )

        logging.info(f"Created community repo chat - Project: {community_project_id}, Chat: {chat_id}, User: {request.user_id}")

        return {
            "project_id": community_project_id,
            "chat_id": chat_id,
            "name": repo.name,
            "admin_user_id": admin_user_id,  # Return this so the frontend knows which namespace to use
            "branch": getattr(repo, "branch", None)  # Return branch info
        }

    except Exception as e:
        logging.error(f"Error creating community repo chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-metadata")
async def update_community_repos_metadata(
    user_email: str = Body(...),
):
    """Update GitHub metadata for all community repositories. Only admin can do this."""
    try:
        # Check if user is admin
        if user_email != os.getenv("ADMIN_EMAIL"):
            raise HTTPException(status_code=403, detail="Only admin can update community repos metadata")

        # Get admin user for GitHub token
        admin_user_id = os.getenv("ADMIN_USER_ID")
        if not admin_user_id:
            raise HTTPException(status_code=500, detail="Admin user ID not configured")

        admin_user = get_user(admin_user_id)
        github_token = None
        if admin_user and admin_user.get("github_installation_id"):
            try:
                github_token = get_installation_token(admin_user["github_installation_id"])
                logging.info(f"Using GitHub App installation token for admin user {admin_user_id}")
            except Exception as e:
                logging.error(f"Failed to get installation token: {e}")
                logging.warning("Proceeding without GitHub token - may hit rate limits")
        else:
            logging.warning(f"No GitHub installation found for admin user {admin_user_id}")
            logging.warning("Proceeding without GitHub token - may hit rate limits")

        # Get all community repos
        repos = list_community_repos()
        updated_count = 0
        failed_count = 0

        for repo in repos:
            try:
                # Fetch latest metadata
                metadata = await fetch_github_metadata(repo.repo_url, github_token)
                if metadata:
                    # Flatten metadata structure
                    flattened_metadata = {
                        "stars": metadata.get("stars", 0),
                        "language": metadata.get("language"),
                        "description": metadata.get("description", repo.description),  # Keep existing if not in metadata
                        "fork_count": metadata.get("fork_count", 0),
                        "open_issues_count": metadata.get("open_issues_count", 0),
                        "watchers_count": metadata.get("watchers_count", 0),
                        "default_branch": metadata.get("default_branch"),
                        "license": metadata.get("license"),
                        "topics": metadata.get("topics", []),
                        "owner": metadata.get("owner"),
                        "github_updated_at": metadata.get("github_updated_at"),
                        "github_metadata": metadata  # Store full metadata for future use
                    }
                    # Update repo with flattened metadata
                    update_community_repo(repo.id, flattened_metadata)
                    updated_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                logging.error(f"Failed to update metadata for repo {repo.id}: {e}")
                failed_count += 1

        return {
            "success": True,
            "total": len(repos),
            "updated": updated_count,
            "failed": failed_count
        }

    except Exception as e:
        logging.error(f"Error updating community repos metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 