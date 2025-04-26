from fastapi import APIRouter, HTTPException, Request, Body, Query
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import uuid4
import json
import logging
import httpx
from urllib.parse import urlparse

from user_store import get_user
from project_store import create_project, get_project, update_project, list_projects
from index import index_repository
from api_store import validate_api_key, increment_api_usage
from githubConfig import get_installation_token

# V2 Public API Models
class RepositoryRequest(BaseModel):
    repository: str = Field(..., description="Repository identifier in owner/repo format")
    branch: Optional[str] = Field(None, description="Branch to index, defaults to repository's default branch")

class QueryRequest(BaseModel):
    messages: List[dict] = Field(..., min_items=1, description="List of chat messages")
    repositories: List[dict] = Field(..., min_items=1, description="List of repositories to query")
    stream: bool = Field(False, description="Whether to stream the response")
    include_sources: bool = Field(True, description="Whether to include source texts in the response")
    use_graph_rag: Optional[bool] = Field(None, description="Whether to use GraphRAG for enhanced code structure understanding")
    graph_query_mode: Optional[str] = Field(None, description="GraphRAG query mode: 'auto', 'global', 'local', or 'drift'")

class RepositoryStatus(BaseModel):
    repository: str
    branch: str
    status: str
    progress: dict = {}
    error: Optional[str] = None

# Create router
router = APIRouter(prefix="/v2", tags=["v2-api"])

def get_api_key_from_header(request: Request) -> Dict[str, Any]:
    """Extract and validate API key from Authorization header."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing API key")
    
    key = auth.replace("Bearer ", "")
    api_key_doc = validate_api_key(key)
    if not api_key_doc:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key_doc

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

@router.get("/repositories")
async def list_repositories_v2(request: Request):
    """List all repositories for the authenticated user via the v2 API."""
    try:
        # Get API key details
        api_key_doc = get_api_key_from_header(request)
        user_id = api_key_doc["user_id"]
        
        # Check if this is a CLI request (for special handling)
        user_agent = request.headers.get("User-Agent", "")
        is_cli_request = "nia-cli" in user_agent or request.headers.get("X-Nia-Client") == "nia-cli"
        
        # Get user's projects
        projects = list_projects(user_id)
        if not projects:
            return []
        
        # Convert projects to v2 API format
        repositories = []
        for project_id, project_data in projects.items():
            # Skip non-dictionary objects (sometimes projects might be integers or other types)
            if not isinstance(project_data, dict):
                logging.warning(f"Skipping non-dictionary project data for ID {project_id}: {type(project_data)}")
                continue
                
            # Skip projects that aren't repos or aren't owned by this user
            if not project_data.get("repoUrl") or project_data.get("user_id") != user_id:
                continue
                
            # Extract repo and branch from URL
            repo_url = project_data.get("repoUrl", "")
            parsed = urlparse(repo_url)
            path_parts = [p for p in parsed.path.split('/') if p]
            repository = "/".join(path_parts[:2]) if len(path_parts) >= 2 else ""
            
            # Create repository object in v2 API format
            repo_obj = {
                "repository_id": project_id,
                "repository": repository,
                "branch": project_data.get("branch_or_commit", "main"),
                "status": project_data.get("status", "unknown"),
            }
            
            # Add progress information if available
            if project_data.get("indexing_progress"):
                progress_data = project_data["indexing_progress"]
                # Ensure indexing_progress is a dictionary
                if isinstance(progress_data, dict):
                    repo_obj["progress"] = {
                        "percentage": progress_data.get("progress", 0),
                        "stage": progress_data.get("stage", ""),
                        "message": progress_data.get("message", "")
                    }
            
            # Add error information if available
            if project_data.get("status") == "error" and project_data.get("error"):
                repo_obj["error"] = project_data["error"]
                
            repositories.append(repo_obj)
            
        return repositories
        
    except Exception as e:
        logging.error(f"Error listing repositories: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while listing repositories: {str(e)}"
        )

@router.post("/repositories")
async def index_repository_v2(
    request: Request,
    body: RepositoryRequest
):
    """Index a repository via the public API."""
    try:
        api_key_doc = get_api_key_from_header(request)
        user_id = api_key_doc["user_id"]
        
        # Get GitHub token from header (optional)
        github_token = request.headers.get("X-GitHub-Token")
        
        # Validate repository URL format
        repo_url = f"https://github.com/{body.repository}"
        is_valid, normalized_url, error = validate_github_url(repo_url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        # Extract owner/repo from validated URL
        parsed = urlparse(normalized_url)
        path_parts = [p for p in parsed.path.split('/') if p]
        owner, repo = path_parts

        # Try to get installation token if not provided in header
        if not github_token:
            user_doc = get_user(user_id)
            if not user_doc or not user_doc.get("github_installation_id"):
                raise HTTPException(
                    status_code=400, 
                    detail="GitHub App installation required. Please install the GitHub App or provide a valid token."
                )
            
            # No exception handling - let error propagate up
            installation_id = user_doc["github_installation_id"]
            github_token = get_installation_token(installation_id)
            if not github_token:
                raise HTTPException(
                    status_code=401,
                    detail="Failed to get GitHub token. Please reinstall the GitHub App."
                )
        
        # Check if repository exists and get default branch
        async with httpx.AsyncClient() as client:
            headers = {}
            if github_token:
                headers["Authorization"] = f"token {github_token}"
            
            # Use validated owner/repo for API requests
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/branches",
                headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Repository not found or not accessible"
                )
            
            repo_data = response.json()
            if not repo_data:
                raise HTTPException(
                    status_code=400,
                    detail="No branches found in repository"
                )

            # Get the default branch from the repository
            repo_info = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=headers
            )
            if repo_info.status_code != 200:
                raise HTTPException(
                    status_code=repo_info.status_code,
                    detail="Failed to fetch repository information"
                )
            
            default_branch = repo_info.json().get("default_branch")
            if not default_branch:
                raise HTTPException(
                    status_code=400,
                    detail="Could not determine default branch"
                )

        # Create project with validated URL
        project_id = str(uuid4())
        project = create_project(
            project_id,
            name=f"{owner}/{repo}:{body.branch or default_branch}",
            repoUrl=normalized_url,  # Use normalized URL
            user_id=user_id,
            status="indexing",
            api_project=True,
            api_key_id=api_key_doc["id"]
        )
        
        # Start indexing as a background task using Hatchet workflow
        try:
            # Check if Nuanced is available
            try:
                from services.nuanced_service import NuancedService
                nuanced_available = NuancedService.is_installed()
                logging.info(f"Nuanced is available and will be used for indexing")
            except ImportError:
                nuanced_available = False
                logging.info(f"Nuanced is not available, indexing without enhancement")
                
            # Initialize Hatchet client
            from hatchet_sdk import Hatchet
            hatchet = Hatchet()
            
            # Prepare workflow input
            workflow_input = {
                "project_id": project_id,
                "user_id": user_id,
                "repo_url": f"{normalized_url}.git",  # Add .git for cloning
                "branch_or_commit": body.branch or default_branch,
                "github_token": github_token,
                "pinecone_index": "nia-app",
                "use_nuanced": nuanced_available,  # Enable Nuanced enhancement if available
                "api_initiated": True  # Mark this as an API-initiated job for logging and tracking
            }
            
            # Start the workflow
            logging.info(f"Starting Hatchet workflow for API indexing of project {project_id}")
            # Use the correct method (it's not async, but the method will return quickly)
            workflow_run = hatchet.client.admin.run_workflow(
                "IndexRepositoryWorkflow", 
                workflow_input
            )
            
            # Extract workflow run ID
            workflow_run_id = workflow_run.id if hasattr(workflow_run, 'id') else str(workflow_run)
            
            # Update project with workflow information
            update_project(
                project_id,
                user_id,
                status="indexing",
                branch=body.branch or default_branch,
                details={
                    "stage": "queued",
                    "message": "Indexing job started through API",
                    "progress": 5,
                    "workflow_run_id": str(workflow_run_id),
                    "started_at": datetime.now(timezone.utc).isoformat(),
                    "api_initiated": True
                }
            )
            
            # Increment API usage
            await increment_api_usage(api_key_doc["key"], requests=1)
            
            return {
                "success": True,
                "data": {
                    "repository_id": project_id,
                    "status": "indexing",
                    "status_url": f"/v2/repositories/{project_id}"
                }
            }
            
        except Exception as e:
            # Update project status on error, but keep it as a workflow error
            # rather than a full indexing error (since indexing itself hasn't started yet)
            error_message = f"Failed to start indexing workflow: {str(e)}"
            update_project(
                project_id,
                user_id,
                status="error",
                error=error_message,
                details={
                    "stage": "error",
                    "message": error_message,
                    "progress": -1,
                    "workflow_error": True,
                    "error_time": datetime.now(timezone.utc).isoformat()
                }
            )
            logging.error(f"Workflow initialization error: {str(e)}")
            logging.error(f"Stack trace:", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to start indexing workflow: {str(e)}"
            )
                
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@router.get("/repositories/{repository_id}", response_model=RepositoryStatus)
async def get_repository_status_v2(
    request: Request,
    repository_id: str
):
    """Get repository indexing status."""
    api_key_doc = get_api_key_from_header(request)
    user_id = api_key_doc["user_id"]
    
    # Try standard project lookup first
    project = get_project(repository_id, user_id, allow_community_access=True)
    
    # If not found, try MongoDB ObjectID lookup (for CLI compatibility)
    if not project:
        try:
            from bson.objectid import ObjectId
            from db import db
            doc = db.projects.find_one({"_id": ObjectId(repository_id)})
            if doc:
                # Convert MongoDB document to dict and remove _id
                doc_dict = dict(doc)
                doc_dict.pop("_id", None)
                project = doc_dict
                logging.info(f"Found project using MongoDB ObjectID: {repository_id}")
        except Exception as e:
            logging.warning(f"Error looking up by ObjectID: {e}")
    
    if not project:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Verify this is an API project owned by this API key
    # Allow access if the project belongs to the same user OR if it's an API project created by this API key
    if not ((project.get("user_id") == user_id) or 
            (project.get("api_project") and project.get("api_key_id") == api_key_doc["id"])):
        raise HTTPException(status_code=403, detail="Not authorized to access this repository")
    
    # Extract repo information from the URL
    repo_url = project["repoUrl"]
    # Remove .git extension if present
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]
    # Extract owner/repo from URL
    repo_path = repo_url.replace("https://github.com/", "")
    
    # Increment API usage
    await increment_api_usage(api_key_doc["key"], requests=1)
    
    # Get the branch from the project if available, otherwise default to main
    branch = project.get("branch", "main")
    
    # Convert project's details/progress field to a dict for the response
    # Details might contain progress information
    progress_info = {}
    details = project.get("details", {})
    if details:
        # Add progress percentage if available
        if "progress" in details:
            progress_info["percentage"] = details["progress"]
        # Add current stage if available
        if "stage" in details:
            progress_info["stage"] = details["stage"]
        # Add status message if available
        if "message" in details:
            progress_info["message"] = details["message"]
    
    return {
        "repository": repo_path,
        "branch": branch,
        "status": project["status"],
        "progress": progress_info,
        "error": project.get("error")
    }

@router.post("/query")
async def query_repositories_v2(
    request: Request,
    body: QueryRequest
):
    """Query indexed repositories."""
    api_key_doc = get_api_key_from_header(request)
    user_id = api_key_doc["user_id"]
    
    if not body.messages:
        raise HTTPException(status_code=400, detail="No messages provided")
    if not body.repositories:
        raise HTTPException(status_code=400, detail="No repositories specified")
    
    # Get the latest user message
    user_message = body.messages[-1]["content"]
    
    # Map repository identifiers to project IDs
    project_ids = []
    matching_projects = []  # Store full project info
    
    for repo in body.repositories:
        repo_identifier = repo.get("repository")
        if not repo_identifier:
            continue
            
        # Generate both possible URL formats
        repo_url_with_git = f"https://github.com/{repo_identifier}.git"
        repo_url_without_git = f"https://github.com/{repo_identifier}"
        
        # Get projects dictionary and filter for matching project
        projects_dict = list_projects(user_id)
        
        # Find matching project
        for project_id, project in projects_dict.items():
            project_url = project.get("repoUrl", "")
            
            # Check if URLs match (with or without .git)
            urls_match = (
                project_url == repo_url_with_git or 
                project_url == repo_url_without_git
            )
            
            # Check if project is properly indexed
            is_indexed = (
                project.get("is_indexed") is True and 
                project.get("status") == "indexed"
            )
            
            if urls_match:
                logging.info(f"Found URL match for {repo_identifier}:")
                logging.info(f"  Project ID: {project.get('id')}")
                logging.info(f"  API Project: {project.get('api_project')}")
                logging.info(f"  API Key ID Match: {project.get('api_key_id') == api_key_doc['id']}")
                logging.info(f"  Is Indexed: {is_indexed}")
                logging.info(f"  Status: {project.get('status')}")
                logging.info(f"  is_indexed flag: {project.get('is_indexed')}")
            
            # Allow access if:
            # 1. Project was created through API by this API key OR
            # 2. Project belongs to the same user that owns the API key
            if (urls_match and is_indexed and 
                (
                    # API-created project with this API key
                    (project.get("api_project") is True and project.get("api_key_id") == api_key_doc["id"]) or 
                    # OR, project belongs to the API key's user (including UI-created projects)
                    (project.get("user_id") == user_id)
                )):
                project_ids.append(project.get("id"))  # Use the project's id field
                matching_projects.append(project)
                logging.info(f"Found matching indexed project: {project.get('id')} for repo: {repo_identifier}")
                logging.info(f"Access granted via: {'API key ownership' if project.get('api_key_id') == api_key_doc['id'] else 'User ownership'}")
                break
    
    if not project_ids:
        raise HTTPException(
            status_code=400,
            detail="No indexed repositories found matching the provided identifiers. Make sure the repositories are fully indexed and accessible with your API key. Repositories must either be created through the API with this key or belong to the API key owner's account."
        )
    
    # Import here to avoid circular imports
    from routes.projects import chat_with_project
    
    # Create chat session
    chat_id = str(uuid4())
    
    # Import here to avoid circular imports
    from chat_store import create_new_chat
    create_new_chat(project_ids[0], user_id, "API Query")
    
    try:
        # Check if Nuanced is available for enhanced context
        try:
            from services.nuanced_service import NuancedService
            nuanced_available = NuancedService.is_installed()
            logging.info(f"Nuanced is available and will be used for query enhancement")
        except ImportError:
            nuanced_available = False
            logging.info(f"Nuanced is not available, querying without enhancement")
        
        # Check if GraphRAG should be enabled
        use_graph_rag = body.use_graph_rag
        graph_query_mode = body.graph_query_mode or "auto"
        
        # If not explicitly specified, check project metadata
        if use_graph_rag is None:
            try:
                # Import helper function to get project metadata
                from retriever import get_project_metadata
                
                # Get project metadata
                project_metadata = get_project_metadata(project_ids[0])
                if project_metadata:
                    use_graph_rag = project_metadata.get('use_graph_rag', False) or project_metadata.get('graphrag_enabled', False)
                    
                    # Additionally, check if the query is appropriate for GraphRAG
                    if not use_graph_rag:
                        # Import is_graph_appropriate_query function
                        from routes.openai_compat import is_graph_appropriate_query
                        if is_graph_appropriate_query(user_message):
                            use_graph_rag = True
                            logging.info(f"GraphRAG activated based on query content")
            except Exception as e:
                logging.warning(f"Failed to check GraphRAG metadata: {e}")
                use_graph_rag = False
                
        logging.info(f"GraphRAG enabled: {use_graph_rag}, mode: {graph_query_mode}")
        
        # Log project details before querying
        logging.info(f"Querying project with ID: {project_ids[0]}")
        logging.info(f"Project details: {matching_projects[0]}")
        
        # Create a deterministic idempotency key for this API request
        idempotency_key = f"query_{api_key_doc['id']}_{chat_id}"
        
        # Calculate input tokens more accurately based on input
        input_tokens = len(user_message.split())
        
        # Get the explicit stream flag from the request
        stream = bool(body.stream) if body.stream is not None else False
        
        # Format the messages for sending to chat_with_project
        # The messages need to be in JSON string format
        formatted_messages = json.dumps(body.messages)
        
        # Format additional_project_ids as a JSON string
        additional_project_ids_json = json.dumps(project_ids[1:] if len(project_ids) > 1 else [])
        
        # Handle streaming vs non-streaming responses differently
        if stream:
            # For streaming responses, return a StreamingResponse
            response = await chat_with_project(
                request=request,
                project_id=project_ids[0],
                user_id=user_id,
                prompt=user_message,
                chat_id=chat_id,
                messages=formatted_messages,
                max_tokens=4096,
                temperature=0.7,
                use_nuanced=nuanced_available,
                use_graph_rag=use_graph_rag,
                graph_query_mode=graph_query_mode,
                stream=True,
                additional_project_ids=additional_project_ids_json,
                include_external_sources=body.include_sources if hasattr(body, 'include_sources') else True,
                include_sources=body.include_sources
            )
            
            # Increment API usage for streaming (can't accurately count output tokens)
            await increment_api_usage(
                api_key_doc["key"],
                requests=1,
                tokens=input_tokens + 100,  # Buffer for encoding differences
                idempotency_key=idempotency_key
            )
            
            # Return the streaming response directly
            return response
        else:
            # For non-streaming responses, get a complete response
            # Note: chat_with_project always returns a StreamingResponse, so we need to 
            # collect and process the full response before returning
            from fastapi.responses import StreamingResponse
            
            # Call chat_with_project with stream=False
            # But since it always returns a StreamingResponse, we'll need to consume it
            stream_generator = await chat_with_project(
                request=request,
                project_id=project_ids[0],
                user_id=user_id,
                prompt=user_message,
                chat_id=chat_id,
                messages=formatted_messages,
                max_tokens=4096,
                temperature=0.7,
                use_nuanced=nuanced_available,
                use_graph_rag=use_graph_rag,
                graph_query_mode=graph_query_mode,
                stream=False,  # Still set to False to communicate intent
                additional_project_ids=additional_project_ids_json,
                include_external_sources=body.include_sources if hasattr(body, 'include_sources') else True,  # Pass source inclusion preference
                include_sources=body.include_sources
            )
            
            # Consume the streaming response to get the full content
            full_content = ""
            sources = []
            
            # If chat_with_project returns a StreamingResponse, we need to extract the generator
            if isinstance(stream_generator, StreamingResponse):
                generator = stream_generator.body_iterator
            else:
                generator = stream_generator
            
            # Collect all content from the stream
            async for chunk in generator:
                if isinstance(chunk, bytes):
                    # Handle bytes data
                    if chunk.startswith(b'data: '):
                        try:
                            data = json.loads(chunk[6:].decode('utf-8'))
                            if "sources" in data:
                                sources = data["sources"]
                            elif "content" in data and data["content"] != "[DONE]":
                                full_content += data["content"]
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            continue
                else:
                    # Handle string data
                    chunk_str = str(chunk)
                    if chunk_str.startswith('data: '):
                        try:
                            data = json.loads(chunk_str[6:])
                            if "sources" in data:
                                sources = data["sources"]
                            elif "content" in data and data["content"] != "[DONE]":
                                full_content += data["content"]
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            continue
            
            # Create a non-streaming response
            response = {
                "content": full_content
            }
            
            # Only include sources if requested
            include_sources = body.include_sources if hasattr(body, 'include_sources') else True
            if include_sources:
                response["sources"] = sources
            else:
                # Include just file paths without content
                response["source_paths"] = [src if isinstance(src, str) else src.get('file_path', '') for src in sources]
            
            # Calculate output tokens for non-streaming
            output_tokens = len(full_content.split())
            
            # Increment API usage with more accurate token count
            await increment_api_usage(
                api_key_doc["key"],
                requests=1,
                tokens=input_tokens + output_tokens + 100,  # Buffer for encoding differences
                idempotency_key=idempotency_key
            )
            
            return response
        
    except Exception as e:
        logging.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 