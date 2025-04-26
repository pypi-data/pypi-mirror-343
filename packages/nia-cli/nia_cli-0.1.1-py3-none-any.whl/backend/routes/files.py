import base64
from urllib.parse import urlparse
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
import logging
import os
import httpx
from pydantic import BaseModel

from githubConfig import get_installation_token
from models import FileTagCreate, FileTagResponse, FileSearchResult
from file_tag_store import (
    create_file_tag,
    get_file_tags,
    delete_file_tag,
    get_files_by_tag,
    get_all_tags_for_project
)
from project_store import get_project
from user_store import get_user
from utils.validation_utils import validate_github_url
from vector_store import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# Create router with prefix
router = APIRouter(prefix="/projects/{project_id}/files", tags=["files"])
api_router = APIRouter(prefix="/api/files", tags=["files"])

@router.post("/tags", response_model=FileTagResponse)
async def create_file_tag_endpoint(
    project_id: str,
    tag_data: FileTagCreate
):
    """Create a new file tag"""
    if tag_data.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")
    return create_file_tag(tag_data)

@router.get("/tags", response_model=List[FileTagResponse])
async def get_file_tags_endpoint(
    project_id: str,
    user_id: str = Query(...),
    file_path: Optional[str] = Query(None)
):
    """Get all file tags for a project"""
    return get_file_tags(project_id, user_id, file_path)

@router.delete("/tags/{tag_id}")
async def delete_file_tag_endpoint(
    project_id: str,
    tag_id: str,
    user_id: str = Query(...)
):
    """Delete a file tag"""
    success = delete_file_tag(tag_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"success": True}

@router.get("/search", response_model=List[FileSearchResult])
async def search_files_endpoint(
    project_id: str,
    query: str = Query(...),
    user_id: str = Query(...),
    top_k: int = Query(5),
    additional_project_ids: List[str] = Query([])  # Add support for additional projects
):
    """Search for files using semantic search across multiple projects"""
    try:
        logging.info(f"File search request - Primary project: {project_id}")
        logging.info(f"Additional projects: {additional_project_ids}")
        
        # Get primary project - allow community access
        project = get_project(project_id, user_id, allow_community_access=True)
        if not project:
            logging.error(f"Project {project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")

        if not project.get("is_indexed"):
            logging.error(f"Project {project_id} not indexed")
            raise HTTPException(
                status_code=400,
                detail="Project is not indexed yet. Please wait for indexing to complete."
            )

        # Combine all project IDs and validate them
        all_project_ids = [project_id] + (additional_project_ids or [])
        logging.info(f"Processing search across projects: {all_project_ids}")
        
        project_configs = []  # Store configurations for each project
        
        for pid in all_project_ids:
            # Get project details - allow community access
            current_proj = get_project(pid, user_id, allow_community_access=True)
            if not current_proj:
                logging.warning(f"Project {pid} not found, skipping")
                continue
                
            if not current_proj.get("is_indexed"):
                logging.warning(f"Project {pid} not indexed, skipping")
                continue
                
            # Determine correct user ID and index for this project
            is_community = current_proj.get("is_community", False)
            retrieval_user_id = os.getenv("ADMIN_USER_ID") if is_community else user_id
            index_name = os.getenv("COMMUNITY_INDEX_NAME", "community-repos") if is_community else "nia-app"
            
            project_configs.append({
                "project_id": pid,
                "user_id": retrieval_user_id,
                "index_name": index_name,
                "is_community": is_community
            })
            
            logging.info(f"Validated project for search: {pid} (community: {is_community}, index: {index_name})")

        if not project_configs:
            logging.warning("No valid projects found for search")
            return []

        all_results = []
        
        # Search across all valid projects
        for config in project_configs:
            try:
                # Initialize vector store with correct index
                vector_store = PineconeVectorStore(
                    index_name=config["index_name"],
                    dimension=1536,  # OpenAI embedding dimension
                    alpha=1.0  # Pure dense search for file search
                )

                # Use the correct namespace format
                namespace = f"{config['user_id']}/{config['project_id']}"
                logging.info(f"Searching in namespace: {namespace} with query: {query}")

                # Perform semantic search
                search_results = vector_store.semantic_file_search(
                    query=query,
                    namespace=namespace,
                    top_k=top_k
                )

                if search_results:
                    # Add project info to each result
                    for result in search_results:
                        result["project_id"] = config["project_id"]
                        result["is_community"] = config["is_community"]
                    all_results.extend(search_results)
                    logging.info(f"Found {len(search_results)} results in project {config['project_id']}")

            except Exception as e:
                logging.error(f"Search failed for project {config['project_id']}: {e}")
                continue

        if not all_results:
            logging.info(f"No results found for query: {query}")
            return []

        # Sort all results by score
        all_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top_k results from all projects combined
        all_results = all_results[:top_k]

        # Convert results to FileSearchResult objects
        results = [
            FileSearchResult(
                file_path=result["file_path"],
                score=result["score"],
                tags=result["metadata"].get("tags", []),
                description=result["metadata"].get("description"),
                metadata={
                    **result["metadata"],
                    "project_id": result["project_id"],
                    "is_community": result["is_community"]
                }
            )
            for result in all_results
        ]

        logging.info(f"Found {len(results)} files across {len(project_configs)} projects")
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"File search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search files: {str(e)}"
        )

@api_router.get("/preview")
async def get_file_preview(
    owner: str,
    repo: str,
    branch_or_commit: str,
    file_path: str,
    user_id: str = None
):
    """Get file preview metadata and content from GitHub."""
    try:
        # Validate repository URL format
        repo_url = f"https://github.com/{owner}/{repo}"
        is_valid, normalized_url, error = validate_github_url(repo_url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        # Extract validated owner/repo
        parsed = urlparse(normalized_url)
        path_parts = [p for p in parsed.path.split('/') if p]
        validated_owner, validated_repo = path_parts

        # Always require user_id and GitHub token for authentication
        if not user_id:
            raise HTTPException(
                status_code=401, 
                detail="Authentication required. Please provide a valid user_id."
            )
            
        user_doc = get_user(user_id)
        if not user_doc or not user_doc.get("github_installation_id"):
            raise HTTPException(
                status_code=400,
                detail="GitHub App installation required. Please install the GitHub App to continue."
            )
        
        # No exception handling to prevent fallback to unauthenticated requests
        installation_id = user_doc["github_installation_id"]
        github_token = get_installation_token(installation_id)
        if not github_token:
            raise HTTPException(
                status_code=401,
                detail="Failed to get GitHub token. Please reinstall the GitHub App."
            )
            
        headers = {"Authorization": f"token {github_token}"}
        
        # Validate and sanitize file path
        if not file_path or '..' in file_path or file_path.startswith('/'):
            raise HTTPException(status_code=400, detail="Invalid file path")
        file_path = file_path.lstrip('/')
        
        # First get the file metadata using validated owner/repo
        api_url = f"https://api.github.com/repos/{validated_owner}/{validated_repo}/contents/{file_path}?ref={branch_or_commit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch file metadata"
                )
            
            data = response.json()
            
            # Get basic metadata
            metadata = {
                "name": data.get("name"),
                "size": data.get("size", 0),
                "type": data.get("type"),
                "encoding": data.get("encoding"),
                "url": data.get("html_url"),
                "download_url": data.get("download_url"),
                "content": None,
                "language": None,
                "last_commit": None
            }
            
            # Get language info using validated owner/repo
            lang_resp = await client.get(
                f"https://api.github.com/repos/{validated_owner}/{validated_repo}/languages",
                headers=headers
            )
            if lang_resp.status_code == 200:
                langs = lang_resp.json()
                # Try to detect language from file extension
                ext = os.path.splitext(file_path)[1].lower()
                ext_to_lang = {
                    ".py": "Python",
                    ".js": "JavaScript",
                    ".ts": "TypeScript",
                    ".tsx": "TypeScript",
                    ".jsx": "JavaScript",
                    ".css": "CSS",
                    ".html": "HTML",
                    ".md": "Markdown",
                    ".json": "JSON",
                    ".yml": "YAML",
                    ".yaml": "YAML",
                    ".sh": "Shell",
                    ".bash": "Shell",
                    ".sql": "SQL",
                    ".go": "Go",
                    ".rs": "Rust",
                    ".java": "Java",
                    ".rb": "Ruby",
                    ".php": "PHP",
                    ".cs": "C#",
                    ".cpp": "C++",
                    ".c": "C",
                    ".swift": "Swift",
                    ".kt": "Kotlin",
                    ".r": "R",
                    ".scala": "Scala"
                }
                metadata["language"] = ext_to_lang.get(ext) or next(iter(langs), None)
            
            # Get last commit info for this file using validated owner/repo
            commit_resp = await client.get(
                f"https://api.github.com/repos/{validated_owner}/{validated_repo}/commits",
                params={"path": file_path, "sha": branch_or_commit, "per_page": 1},
                headers=headers
            )
            if commit_resp.status_code == 200:
                commits = commit_resp.json()
                if commits:
                    last_commit = commits[0]
                    metadata["last_commit"] = {
                        "sha": last_commit["sha"][:7],
                        "message": last_commit["commit"]["message"].split("\n")[0],
                        "author": last_commit["commit"]["author"]["name"],
                        "date": last_commit["commit"]["author"]["date"]
                    }
            
            # Get file content (limited to first ~1000 bytes for preview)
            if data.get("size", 0) <= 100000:  # Only fetch content for files <= 100KB
                if data.get("encoding") == "base64" and data.get("content"):
                    content = base64.b64decode(data["content"]).decode('utf-8')
                    # Limit content to first ~1000 bytes
                    metadata["content"] = content[:1000] + ("..." if len(content) > 1000 else "")
            
            return metadata
        
    except Exception as e:
        logging.error(f"Error fetching file preview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tags/all")
async def get_all_tags_endpoint(
    project_id: str,
    user_id: str = Query(...)
):
    """Get all unique tags used in a project"""
    return {"tags": get_all_tags_for_project(project_id, user_id)} 