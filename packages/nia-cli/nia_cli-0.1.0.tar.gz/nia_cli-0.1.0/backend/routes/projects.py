import base64
from urllib.parse import urlparse
from fastapi import APIRouter, Body, Query, HTTPException, BackgroundTasks, Request, Form
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
import logging
import asyncio
import os
import json
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
import httpx
from pydantic import BaseModel
from time import perf_counter

from db import db
from githubConfig import get_installation_token
from project_store import (
    list_projects,
    create_project,
    get_project,
    update_project,
    delete_project,
    ProjectStore
)
from chat_store import (
    get_chat_messages,
    add_chat_message,
    reset_chat,
    get_project_chats,
    create_new_chat,
    update_chat_title,
    delete_chat
)
from user_store import get_user, get_or_create_user
from utils import (
    validate_github_url,
    build_advanced_retriever,
    fallback_pinecone_retrieval,
    log_to_keywords_ai
)
from utils.validation_utils import validate_safe_path
from utils.formatting_utils import format_context, process_code_blocks
from utils.logging_utils import safe_json_dumps
# Using MongoDB directly for status tracking
from llm import get_available_models
from community_repo_store import list_community_repos
from models import (
    FileTagCreate,
    FileTagResponse,
    FileSearchResult,
    CommunityRepoCreate
)

router = APIRouter(prefix="/projects", tags=["projects"])
api_router = APIRouter(prefix="/api/projects", tags=["api-projects"])

# ------------------
# PROJECTS CRUD
# ------------------
@router.get("")
def list_user_projects(
    user_id: str,
    include_community: bool = Query(False, description="Whether to include community repos in the response")
):
    """List projects with optional inclusion of community repos"""
    # Get user's own projects
    user_projects = list_projects(user_id)
    
    # Include community repos only if requested
    if include_community:
        try:
            logging.info(f"Including community repos for user {user_id}")
            community_repos = list_community_repos()
            logging.info(f"Found {len(community_repos)} community repos")
            
            admin_id = os.getenv("ADMIN_USER_ID")
            if not admin_id:
                logging.error("ADMIN_USER_ID not set in environment")
                return user_projects
                
            for repo in community_repos:
                if repo.is_indexed and repo.project_id:
                    proj = get_project(repo.project_id, admin_id)
                    if proj and proj.get("is_indexed"):
                        user_projects[repo.project_id] = {
                            **proj,
                            "is_community": True,
                            "community_repo_id": repo.id,
                            "name": repo.name
                        }
                    else:
                        logging.warning(f"Community repo {repo.name} has project_id {repo.project_id} but project not found or not indexed")
        except Exception as e:
            logging.error(f"Error including community repos: {e}")
            # Continue with just user projects if community repos fail
            pass
    
    return user_projects

@router.post("")
def create_user_project(
    name: str = Body(...),
    repoUrl: str = Body(...),
    user_id: str = Body(...),
    status: str = Body("new")
):
    """Create a new project in local JSON store (sets status='new')."""
    # Validate repository URL
    is_valid, normalized_url, error = validate_github_url(repoUrl)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    project_id = str(uuid4())
    create_project(project_id, name, normalized_url, user_id)
    return {"projectId": project_id, "name": name, "repoUrl": normalized_url, "status": status}

@router.get("/{project_id}")
def get_user_project(project_id: str, user_id: str):
    proj = get_project(project_id, user_id, allow_community_access=True)
    if not proj:
        raise HTTPException(status_code=404, detail="No such project")
    return {"projectId": project_id, **proj}

@router.patch("/{project_id}")
def patch_user_project(
    project_id: str, 
    user_id: str = Body(...), 
    name: str = Body(None),
    include_external_sources: bool = Body(None)
):
    updated = update_project(
        project_id, 
        user_id, 
        name=name, 
        include_external_sources=include_external_sources
    )
    if not updated:
        raise HTTPException(status_code=404, detail="No such project")
    return {"success": True, "updated": updated}

@router.delete("/{project_id}")
def delete_user_project(project_id: str, user_id: str):
    ok = delete_project(project_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="No such project")
    return {"success": True}

# ------------------
# PROJECT INDEXING
# ------------------
def _background_index_project(
    project_id: str,
    user_id: str,
    repo_url: str,
    branch_or_commit: str,
    github_token: str
):
    """Background task for repository indexing using Hatchet."""
    from hatchet_sdk import Hatchet
    
    try:
        # Get project from MongoDB
        proj = get_project(project_id, user_id)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found")

        # Update project status to "indexing"
        update_project(
            project_id,
            user_id,
            status="indexing",
            progress={
                "stage": "starting",
                "message": "Starting indexing process...",
                "progress": 0
            }
        )

        # Initialize Hatchet client
        hatchet = Hatchet()
        
        # Trigger Hatchet workflow for indexing
        workflow_input = {
            "project_id": project_id,
            "user_id": user_id,
            "repo_url": repo_url,
            "branch_or_commit": branch_or_commit,
            "github_token": github_token
        }
        
        # Run the workflow
        try:
            workflow_run = hatchet.client.admin.run_workflow(
                "IndexRepositoryWorkflow", 
                workflow_input
            )
            
            # Important: Extract the string ID from the WorkflowRunRef object 
            # to avoid JSON serialization issues
            workflow_run_id = workflow_run.id if hasattr(workflow_run, 'id') else str(workflow_run)
            
            logging.info(f"Started Hatchet workflow for indexing project {project_id}: {workflow_run_id}")
            
            # Update project with workflow run ID (as string)
            update_project(
                project_id,
                user_id,
                status="indexing",
                details={
                    "stage": "queued",
                    "message": f"Indexing job started",
                    "progress": 5,
                    "workflow_run_id": workflow_run_id,
                    "started_at": datetime.now(timezone.utc).isoformat()
                }
            )
            
            # Return immediately with status (ensure all values are JSON-serializable)
            return {
                "status": "indexing",
                "message": "Indexing job started",
                "workflow_run_id": str(workflow_run_id)
            }
            
        except Exception as workflow_error:
            logging.error(f"Failed to start Hatchet workflow: {workflow_error}")
            raise Exception(f"Failed to start indexing workflow: {str(workflow_error)}")

    except Exception as e:
        logging.error(f"Background indexing error: {e}")
        # Update both the details and the top-level error field to ensure consistent error reporting
        # This helps with the status endpoint showing the correct error state
        update_project(
            project_id,
            user_id,
            status="error",
            error=str(e),  # Set top-level error field
            details={
                "stage": "error",
                "message": str(e),
                "progress": -1,
                "error": str(e),
                "error_time": datetime.now(timezone.utc).isoformat()
            }
        )
        
        # Log more details about the exception
        import traceback
        logging.error(f"Indexing error details: {traceback.format_exc()}")
        raise

@router.post("/{project_id}/index")
async def index_project_repo(
    project_id: str,
    background_tasks: BackgroundTasks,
    user_id: str = Body(...),
    branchOrCommit: str = Body(None),
):
    """Start indexing a project's repository."""
    try:
        # Get project from MongoDB
        proj = get_project(project_id, user_id)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found")
            
        # If project already has an error, clear it before starting a new indexing job
        if proj.get("error"):
            logging.info(f"Clearing previous error state for project {project_id}: {proj.get('error')}")
            update_project(project_id, user_id, error=None)

        # Get GitHub token if available - helps with rate limits but not required for public repos
        github_token = None
        try:
            # Get user from MongoDB to check for GitHub installation
            user = await get_or_create_user(user_id)
            if user and user.get("github_installation_id"):
                # IMPORTANT: get_installation_token is synchronous - do not use await
                installation_id = user["github_installation_id"]
                try:
                    token_result = get_installation_token(installation_id)
                    
                    # Handle different return types from get_installation_token
                    if isinstance(token_result, dict) and "token" in token_result:
                        github_token = token_result["token"]
                    else:
                        github_token = token_result
                    
                    # Ensure token is a string
                    if not isinstance(github_token, str):
                        logging.warning(f"GitHub token is not a string, converting: {type(github_token)}")
                        github_token = str(github_token)
                except Exception as token_error:
                    logging.error(f"Error getting GitHub token: {token_error}")
                    github_token = None
                    
                logging.info(f"Got GitHub token for user {user_id}")
            else:
                logging.warning(f"No GitHub installation found for user {user_id} - proceeding without token")
                # Continue without token for public repos
        except Exception as e:
            logging.warning(f"Failed to get GitHub token: {e}")
            # Continue without token for public repos
        
        # Get repository size from GitHub API
        try:
            # Extract repo name from URL
            repo_url = proj["repoUrl"]
            repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
            
            # Get repository size from GitHub API
            headers = {}
            if github_token:
                headers["Authorization"] = f"token {github_token}"
                
            async with httpx.AsyncClient() as client:
                repo_resp = await client.get(f"https://api.github.com/repos/{repo_name}", headers=headers)
                
                if repo_resp.status_code == 200:
                    repo_data = repo_resp.json()
                    # GitHub returns size in KB, convert to MB
                    repo_size_mb = repo_data.get("size", 0) / 1024
                    
                    # Validate repository size against user's subscription tier
                    project_store = ProjectStore()
                    # Wrap potentially problematic function in a try block with better error handling
                    try:
                        await project_store.validate_repository_size(user_id, repo_size_mb)
                    except Exception as validation_error:
                        logging.error(f"Repository size validation error: {validation_error}")
                        # Continue anyway - this isn't critical for private repos
                    
                    logging.info(f"Repository size validation passed for {repo_name}: {repo_size_mb:.1f}MB")
                else:
                    logging.warning(f"Failed to get repository size from GitHub API: {repo_resp.status_code}")
                    # For 404 errors, we'll proceed anyway as the user might be using a private repo
                    if repo_resp.status_code == 404:
                        logging.info(f"Repository not found (404) - assuming private repo and continuing")
                        # Continue with indexing for private repos - we can't validate size
                    else:
                        # Don't continue if we can't validate the repository size
                        raise HTTPException(
                            status_code=400,
                            detail="Unable to validate repository size due to GitHub API error. Please try again later."
                        )
        except HTTPException as he:
            # Re-raise HTTP exceptions (like 402 Payment Required)
            raise he
        except Exception as e:
            logging.error(f"Error checking repository size: {e}")
            # Don't continue with indexing if size check fails
            raise HTTPException(
                status_code=400,
                detail="Unable to validate repository size. Please ensure the repository exists and try again later."
            )

        # Start background indexing task
        background_tasks.add_task(
            _background_index_project,
            project_id,
            user_id,
            proj["repoUrl"],
            branchOrCommit,
            github_token
        )

        return {"status": "indexing", "message": "Started indexing process"}
    except HTTPException as he:
        # Pass through HTTP exceptions with their status codes
        raise he
    except Exception as e:
        logging.error(f"Error starting indexing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/status")
async def get_project_status(project_id: str, user_id: str):
    """Get the current indexing status of a project."""
    try:
        # Add retries for getting project status during indexing
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            # Get project from MongoDB
            proj = get_project(project_id, user_id)
            if not proj:
                if retry_count < max_retries - 1:
                    retry_count += 1
                    await asyncio.sleep(1)  # Wait 1 second before retry
                    continue
                raise HTTPException(status_code=404, detail="Project not found")
            
            # Format the response using the project details from MongoDB
            response = {
                "status": proj.get("status", "unknown"),
                "is_indexed": proj.get("is_indexed", False),
                "progress": 0,  # Default to 0 for progress
                "error": proj.get("error"),
                "last_indexed": proj.get("last_indexed"),
                "chat_id": proj.get("current_chat_id")
            }
            
            # Get details from project for additional status information
            details = proj.get("details", {})
            if details:
                # Make sure all values are JSON serializable
                safe_details = {}
                for k, v in details.items():
                    if isinstance(v, (str, int, float, bool, dict, list, type(None))):
                        safe_details[k] = v
                    else:
                        # Convert non-serializable objects to strings
                        safe_details[k] = str(v)
                
                # Add workflow_run_id if available
                if "workflow_run_id" in safe_details:
                    response["workflow_run_id"] = safe_details.get("workflow_run_id")
                
                # Handle progress
                if "progress" in safe_details:
                    response["progress"] = safe_details.get("progress")
                
                # Add message if available
                if "message" in safe_details:
                    response["message"] = safe_details.get("message")
                
                # Add stage information if available
                if "stage" in safe_details:
                    response["stage"] = safe_details.get("stage")
            
            # Check for the special 'indexing_progress' field that might have been set
            if "indexing_progress" in proj and proj["indexing_progress"] is not None:
                response["progress"] = proj["indexing_progress"]
            
            # Handle errors - make sure to provide useful error messages
            if response["status"] == "error" and not response.get("message"):
                response["message"] = proj.get("error") or "Unknown error occurred during indexing"
                
            # Additional check: If there's an error field but status isn't error, something's wrong
            elif proj.get("error") and response["status"] != "error":
                # This is likely an error that occurred during startup but status wasn't properly updated
                logging.warning(f"Project has error field but status isn't 'error': {proj.get('error')}")
                response["status"] = "error"
                response["progress"] = -1
                response["message"] = proj.get("error") or "Error during startup"
            
            # Ensure response doesn't contain any non-serializable objects
            for key, value in list(response.items()):
                if not isinstance(value, (str, int, float, bool, dict, list, type(None))):
                    response[key] = str(value)
            
            return response
            
        # If we get here, project was not found after retries
        raise HTTPException(status_code=404, detail="Project not found")
            
    except Exception as e:
        logging.error(f"Error getting project status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/cancel")
def cancel_project_indexing(project_id: str, user_id: str = Body(...)):
    """Cancel an in-progress indexing job."""
    from hatchet_sdk import Hatchet
    
    project = get_project(project_id, user_id)
    if not project:
        raise HTTPException(status_code=404, detail="No such project")
    
    if project.get("status") != "indexing":
        raise HTTPException(status_code=400, detail="Project is not currently being indexed")
    
    try:
        # Get the workflow run ID from project details
        details = project.get("details", {})
        workflow_run_id = details.get("workflow_run_id")
        
        if not workflow_run_id:
            logging.warning(f"No workflow run ID found for project {project_id}")
            # Update project status directly in MongoDB
            update_project(
                project_id=project_id,
                user_id=user_id,
                status="cancelled",
                details={
                    "stage": "cancelled",
                    "message": "Indexing cancelled by user",
                    "progress": -1,
                    "cancelled_at": datetime.now(timezone.utc).isoformat()
                }
            )
            return {"success": True, "message": "Cancellation requested (direct update)"}
        
        # Initialize Hatchet client
        hatchet = Hatchet()
        
        # Cancel the workflow
        hatchet.client.admin.cancel_workflow_run(workflow_run_id)
        logging.info(f"Cancelled Hatchet workflow for project {project_id}: {workflow_run_id}")
        
        # Update the project status
        update_project(
            project_id=project_id,
            user_id=user_id,
            status="cancelled",
            details={
                "stage": "cancelled",
                "message": "Indexing cancelled by user",
                "progress": -1,
                "cancelled_at": datetime.now(timezone.utc).isoformat(),
                "workflow_run_id": workflow_run_id
            }
        )
        
        return {"success": True, "message": "Cancellation requested"}
    except Exception as e:
        logging.error(f"Error cancelling workflow: {e}")
        # No fallback available
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to cancel indexing: {str(e)}"
        )

# ------------------
# PROJECT CHAT
# ------------------
@router.post("/{project_id}/chat")
async def chat_with_project(
    project_id: str,
    request: Request,
    user_id: str = Form(...),
    prompt: str = Form(...),
    chat_id: str = Form(...),
    messages: str = Form(...),  # JSON string
    max_tokens: int = Form(4096),
    temperature: float = Form(0.2),
    stream: bool = Form(True),
    additional_project_ids: str = Form("[]"),  # JSON string
    use_nuanced: bool = Form(False),
    include_external_sources: bool = Form(True),
    include_sources: bool = Form(True),
    use_graph_rag: bool = Form(False),
    graph_query_mode: str = Form("auto")
):
    """
    Chat with a vector store containing a code repository.
    Supports multimodal inputs (images) according to provider requirements.
    
    Args:
        project_id: The ID of the project to query
        user_id: The ID of the user querying
        prompt: The user query
        chat_id: The chat session ID for message threading
        messages: List of messages in conversation (for chat history/context)
        max_tokens: Max number of tokens in the response
        temperature: Model temperature for controlling randomness
        stream: Whether to stream the response or not
        additional_project_ids: Optional list of additional project IDs to include
        use_nuanced: Whether to use Nuanced call graph data for context
        include_external_sources: Whether to include external data sources in retrieval
        include_sources: Whether to include source information in response 
        use_graph_rag: Whether to use GraphRAG for enhanced code structure understanding
        graph_query_mode: GraphRAG query mode ('auto', 'global', 'local', or 'drift')
        
    Returns:
        StreamingResponse with the chat results
    """
    try:
        # Parse form data and extract images
        form_data = await request.form()
        image_files = []
        
        # Extract image files
        for key, value in form_data.items():
            if key.startswith("images") and hasattr(value, "filename"):
                image_files.append(value)
        
        # Log image information
        logging.info(f"Received {len(image_files)} images with prompt: {prompt[:50]}...")
        
        # Parse JSON strings
        messages_data = json.loads(messages)
        additional_project_ids_list = json.loads(additional_project_ids)
        
        # Verify user has access to primary project
        proj = get_project(project_id, user_id)
        if not proj:
            raise HTTPException(
                status_code=403, 
                detail=f"User {user_id} does not have access to project {project_id}"
            )
            
        # Process and encode image files
        processed_images = []
        image_urls = []
        if image_files:
            for img_file in image_files:
                content = await img_file.read()
                encoded_image = base64.b64encode(content).decode("utf-8")
                mime_type = img_file.content_type or "image/jpeg"  # Default to jpeg if not specified
                processed_images.append({
                    "data": encoded_image,
                    "mime_type": mime_type,
                    "filename": img_file.filename
                })
                
                # Create a data URL for storing the image with the user message
                img_url = f"data:{mime_type};base64,{encoded_image}"
                image_urls.append(img_url)
        
        # Record message in chat log with any images
        from chat_store import add_chat_message
        add_chat_message(
            project_id,
            chat_id, 
            "user",
            prompt,
            user_id,
            images=image_urls if image_urls else None
        )
            
        # Log what project(s) we're processing
        logging.info(f"Chat request - Primary project: {project_id}")
        logging.info(f"Additional projects: {additional_project_ids_list}")
        logging.info(f"Include external sources: {include_external_sources}")
            
        # Expand to include any additional projects
        projects_to_process = [project_id]
        if additional_project_ids_list:
            projects_to_process.extend(additional_project_ids_list)
                
        logging.info(f"Processing query across projects: {projects_to_process}")
            
        project_configs = []
        
        # Process each project (primary and additional)
        for idx, pid in enumerate(projects_to_process):
            # Get project details - allow community access
            current_proj = get_project(pid, user_id, allow_community_access=True)
            if not current_proj:
                logging.warning(f"Project not found: {pid}")
                continue
                
            if not current_proj.get("is_indexed"):
                logging.warning(f"Project not indexed: {pid}")
                continue
                
            # Determine correct user ID and index for this project
            is_community = current_proj.get("is_community", False)
            admin_user_id = os.getenv("ADMIN_USER_ID")
            
            # Fix for community projects - ensure admin_user_id is set
            if is_community and not admin_user_id:
                logging.error(f"ADMIN_USER_ID environment variable not set but required for community repo {pid}")
                admin_user_id = "admin" # Fallback value
                
            retrieval_user_id = admin_user_id if is_community else user_id
            index_name = os.getenv("COMMUNITY_INDEX_NAME", "community-repos") if is_community else "nia-app"
            
            # Add Nuanced path for each project to ensure local file lookup works
            repo_path = f"/tmp/my_local_repo_{pid}"
            
            # Additional logging for community projects
            if is_community:
                logging.info(f"Community project: {pid}, using admin user: {retrieval_user_id}, index: {index_name}")
                
                # For community repos, check if the repository exists locally
                if os.path.exists(repo_path):
                    logging.info(f"Found local repository for community project at: {repo_path}")
                else:
                    logging.warning(f"No local repository found for community project at: {repo_path}")
                    
                    # Try alternate paths
                    alternate_paths = [
                        f"/tmp/nuanced_debug_{pid}", 
                        f"/tmp/nia_repo_{pid}"
                    ]
                    
                    for alt_path in alternate_paths:
                        if os.path.exists(alt_path):
                            repo_path = alt_path
                            logging.info(f"Found alternative repository path: {repo_path}")
                            break
            
            project_configs.append({
                "project_id": pid,
                "user_id": retrieval_user_id,
                "index_name": index_name,
                "is_community": is_community,
                "repo_path": repo_path  # Add repo path to config
            })
            
            logging.info(f"Validated project: {pid} ({idx+1})")

        # If no valid projects, return 404
        if not project_configs:
            raise HTTPException(status_code=404, detail="No indexed projects found")
            
        # Process model preferences from project
        provider = proj.get("llm_provider", "anthropic")  # Get the provider from project settings
        model = proj.get("llm_model", None)  # Get the model from project settings
        
        # Set default models based on provider
        if provider == "anthropic":
            model = model or "claude-3-7-sonnet-20250219"
            use_advanced = True  # Claude models support advanced retrievers
        elif provider == "openai":
            model = model or "gpt-4.1-2025-04-14"
            use_advanced = False  # Don't use advanced retrievers with OpenAI models
        elif provider == "gemini":
            model = model or "gemini-2.5-pro"
            use_advanced = True  # Gemini supports advanced retrievers
        else:
            # Default to Anthropic
            provider = "anthropic"
            model = "claude-3-7-sonnet-20250219"
            use_advanced = True
            
        # Detect graph-oriented queries
        if not use_graph_rag:
            try:
                # Try to determine if query is appropriate for GraphRAG
                from routes.openai_compat import is_graph_appropriate_query
                if is_graph_appropriate_query(prompt):
                    logging.info(f"GraphRAG automatically enabled based on query content")
                    use_graph_rag = True
            except Exception as e:
                logging.warning(f"Error checking for GraphRAG-appropriate query: {e}")
                
        # Detect function call relationship queries
        if not use_nuanced and not use_graph_rag:
            try:
                from utils.retriever_utils import is_call_relationship_query
                if is_call_relationship_query(prompt):
                    logging.info(f"Nuanced automatically enabled for call relationship query")
                    use_nuanced = True
            except Exception as e:
                logging.warning(f"Error checking for call relationship query: {e}")
                
        # If both Nuanced and GraphRAG would be enabled, prioritize GraphRAG
        if use_nuanced and use_graph_rag:
            logging.info(f"Both Nuanced and GraphRAG requested, prioritizing GraphRAG")
            use_nuanced = False

        # Generate multi-queries first to stream them early
        from utils.retriever_utils import generate_multi_queries
        multi_queries = await generate_multi_queries(prompt)
        
        # Store multi-queries for streaming
        generated_multi_queries = multi_queries
        
        # Get retrieval results using fallback_pinecone_retrieval
        # The validation agent is automatically applied within the function
        docs, contexts, sources = await fallback_pinecone_retrieval(
            prompt, 
            project_configs,
            use_nuanced=use_nuanced,
            include_external_sources=include_external_sources,
            user_id=user_id,
            use_graph_rag=use_graph_rag,
            graph_query_mode=graph_query_mode
        )

        # Build a system prompt with top retrieved docs
        system_prompt = (
            f"You are an expert AI coding assistant called Nia designed by Nozomio engineering team: a world class AI company based in San Francisco."
            "Follow these guidelines for responses:\n"
            "1. Prioritize accuracy and practical insights\n"
            "2. Include relevant code examples when explaining functionality\n"
            "3. Do not lie or make up facts\n"
            "4. Reference specific files and line numbers when relevant\n"
            "5. If you do not have any relevant code, pinpoint to the specific files where that code is located\n"
            "6. Do not assume about the codebase in any case and do not make any assumptions about the codebase\n"
            "\nHere are relevant code from the repository:\n\n" +
            format_context(sources, contexts)
        )

        # Format conversation for model
        formatted_messages = []
        for m in messages_data[-10:]:
            if m["role"] == "user":
                formatted_messages.append({"role": "user", "content": m["content"]})
            elif m["role"] == "assistant":
                formatted_messages.append({"role": "assistant", "content": m["content"]})

        # Streaming response generator
        async def generate():
            full_response = ""
            start_time = perf_counter()
            
            try:
                # First, send a thinking message to indicate we're starting to process queries
                thinking_data = {
                    "type": "thinking",
                    "stage": "queries",
                    "message": "Expanding search..."
                }
                yield f"data: {safe_json_dumps(thinking_data)}\n\n"
                await asyncio.sleep(0.3)  # Delay to show thinking state
                
                # Then stream each query one by one for a more dynamic feel
                if generated_multi_queries:
                    # First send an empty multi-queries array to initialize the state
                    empty_queries = {
                        "multi_queries": [],
                        "type": "multi_query"
                    }
                    yield f"data: {safe_json_dumps(empty_queries)}\n\n"
                    await asyncio.sleep(0.5)  # Delay before starting to stream queries
                    
                    # Now stream each query one by one with delays
                    for i, query in enumerate(generated_multi_queries):
                        # Send the current set of queries
                        partial_queries = {
                            "multi_queries": generated_multi_queries[:i+1],
                            "type": "multi_query"
                        }
                        yield f"data: {safe_json_dumps(partial_queries)}\n\n"
                        
                        # Add a delay between each query (shorter for the last one)
                        if i < len(generated_multi_queries) - 1:
                            await asyncio.sleep(0.6)  # Longer delay between queries
                        else:
                            await asyncio.sleep(0.3)  # Shorter delay after last query
                
                # Send source info AFTER multi-queries but BEFORE validation
                # This ensures correct ordering of information
                yield f"data: {safe_json_dumps({'sources': sources})}\n\n"
                
                # Send any validation agent reasoning if available
                # The validation agent attaches its reasoning to the last document
                if docs and hasattr(docs[-1], "metadata") and docs[-1].metadata.get("validation_reasoning"):
                    validation_data = {
                        "validation": {
                            "reasoning": docs[-1].metadata.get("validation_reasoning", ""),
                            "score": docs[-1].metadata.get("validation_score", 0.0),
                            "sufficient": docs[-1].metadata.get("validation_sufficient", True),
                            "missing_info": docs[-1].metadata.get("validation_missing_info", [])
                        },
                        "type": "validation"
                    }
                    yield f"data: {safe_json_dumps(validation_data)}\n\n"
                    await asyncio.sleep(0.1)  # Small delay for client to process
                
                if provider == "anthropic":
                    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
                    if not anthropic_api_key:
                        raise HTTPException(status_code=401, detail="ANTHROPIC_API_KEY missing")
                    
                    from anthropic import Anthropic
                    anthropic_client = Anthropic(api_key=anthropic_api_key)

                    # Format images for Anthropic
                    user_message_content = []
                    
                    # Add images if present
                    for img in processed_images:
                        user_message_content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": img["mime_type"],
                                "data": img["data"]
                            }
                        })
                    
                    # Add text prompt
                    user_message_content.append({
                        "type": "text",
                        "text": prompt
                    })
                    
                    # Format all messages for Claude
                    claude_messages = []
                    for msg in formatted_messages:
                        if isinstance(msg["content"], str):
                            claude_messages.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })
                        else:
                            # Handle existing multimodal content if present
                            claude_messages.append(msg)
                    
                    # Add the current message with images
                    claude_messages.append({
                        "role": "user",
                        "content": user_message_content
                    })

                    # Make request to Claude
                    stream_resp = anthropic_client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        system=system_prompt,
                        messages=claude_messages,
                        stream=True
                    )
                    
                    for chunk in stream_resp:
                        if chunk.type == 'content_block_delta' and chunk.delta.text:
                            content = chunk.delta.text
                            full_response += content
                            processed_content = process_code_blocks(content) if "```" in full_response else content
                            yield f"data: {safe_json_dumps({'content': processed_content})}\n\n"
                            await asyncio.sleep(0)
                
                elif provider == "openai":
                    openai_api_key = os.getenv("OPENAI_API_KEY")
                    if not openai_api_key:
                        raise HTTPException(status_code=401, detail="OPENAI_API_KEY missing")
                    
                    from openai import OpenAI
                    openai_client = OpenAI(api_key=openai_api_key)

                    # Format images for OpenAI
                    message_content = []
                    
                    # Add text first
                    message_content.append({
                        "type": "text",
                        "text": prompt
                    })
                    
                    # Add images if present
                    for img in processed_images:
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{img['mime_type']};base64,{img['data']}",
                                "detail": "high"  # Use high detail for code images
                            }
                        })
                    
                    # Format all messages for OpenAI
                    # First add system message
                    openai_messages = [
                        {"role": "system", "content": system_prompt}
                    ]
                    
                    # Add prior conversation messages
                    for msg in formatted_messages:
                        if isinstance(msg["content"], str):
                            openai_messages.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })
                        else:
                            # Handle existing multimodal content if present
                            openai_messages.append(msg)
                    
                    # Add current message with images
                    openai_messages.append({
                        "role": "user", 
                        "content": message_content
                    })

                    # Make request to OpenAI
                    stream_resp = openai_client.chat.completions.create(
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        messages=openai_messages,
                        stream=True
                    )
                    
                    for chunk in stream_resp:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            processed_content = process_code_blocks(content) if "```" in full_response else content
                            yield f"data: {safe_json_dumps({'content': processed_content})}\n\n"
                            await asyncio.sleep(0)
                
                elif provider == "gemini":
                    gemini_api_key = os.getenv("GEMINI_API_KEY")
                    if not gemini_api_key:
                        raise HTTPException(status_code=401, detail="GEMINI_API_KEY missing")
                    
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_api_key)
                    
                    # Format messages for Gemini
                    gemini_content = []
                    
                    # Add prior conversation messages
                    for msg in formatted_messages:
                        if msg["role"] == "user":
                            gemini_content.append({
                                "role": "user",
                                "parts": [{"text": msg["content"]}]
                            })
                        elif msg["role"] == "assistant":
                            gemini_content.append({
                                "role": "model",
                                "parts": [{"text": msg["content"]}]
                            })
                    
                    # Create parts array for current message
                    current_parts = []
                    
                    # Add images if present
                    for img in processed_images:
                        current_parts.append({
                            "inline_data": {
                                "mime_type": img["mime_type"],
                                "data": img["data"]
                            }
                        })
                    
                    # Add text
                    current_parts.append({"text": prompt})
                    
                    # Add system prompt as a prefix to the user's message
                    prefixed_prompt = f"{system_prompt}\n\nNow answer this question: {prompt}"
                    current_parts = [{"text": prefixed_prompt}] + current_parts[1:] if current_parts else [{"text": prefixed_prompt}]
                    
                    # Add current message
                    gemini_content.append({
                        "role": "user",
                        "parts": current_parts
                    })
                    
                    # Create the Gemini model
                    model_obj = genai.GenerativeModel(model)
                    
                    # Start the chat session
                    chat = model_obj.start_chat(history=gemini_content[:-1])
                    
                    # Send the message and stream the response
                    stream_resp = chat.send_message(
                        gemini_content[-1]["parts"],
                        stream=True
                    )
                    
                    for chunk in stream_resp:
                        if chunk.text:
                            content = chunk.text
                            full_response += content
                            processed_content = process_code_blocks(content) if "```" in full_response else content
                            yield f"data: {safe_json_dumps({'content': processed_content})}\n\n"
                            await asyncio.sleep(0)
                
                # End of stream
                yield f"data: {safe_json_dumps({'content': '[DONE]'})}\n\n"
                
                # Save the assistant's response to chat store
                if full_response:
                    # Generate image URLs for storage and display
                    image_urls = []
                    for img in processed_images:
                        # Create a unique ID for each image
                        img_id = str(uuid4())
                        # Store in a format that can be retrieved later
                        img_url = f"data:{img['mime_type']};base64,{img['data']}"
                        image_urls.append(img_url)
                    
                    # Add the message with image URLs
                    add_chat_message(
                        project_id, 
                        chat_id, 
                        "assistant", 
                        full_response, 
                        user_id, 
                        sources=sources,
                        images=image_urls if image_urls else None
                    )
                    
            except Exception as e:
                logging.error(f"Streaming error: {str(e)}")
                yield f"data: {safe_json_dumps({'error': str(e), 'content': full_response})}\n\n"
                if full_response:
                    add_chat_message(project_id, chat_id, "assistant", full_response, user_id, sources=sources, images=None)

        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        logging.error(f"Error in chat_with_project: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/chat-history")
def get_project_chat_history(project_id: str, user_id: str):
    """Get chat history for a project."""
    # First verify project access
    proj = get_project(project_id, user_id, allow_community_access=True)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    return get_chat_messages(project_id, user_id)

@router.post("/{project_id}/chat/reset")
def reset_project_chat(project_id: str, user_id: str):
    """Reset chat history for a project."""
    # First verify project access
    proj = get_project(project_id, user_id, allow_community_access=True)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    reset_chat(project_id)
    return {"success": True}

@router.get("/{project_id}/chats")
def get_project_chats_endpoint(project_id: str, user_id: str = Query(...)):
    """Get all chats for a project."""
    try:
        # First verify project access
        proj = get_project(project_id, user_id, allow_community_access=True)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found or access denied")
        chats = get_project_chats(project_id, user_id)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/chats/{chat_id}")
def get_chat_messages_endpoint(project_id: str, chat_id: str, user_id: str = Query(...)):
    """Get messages for a specific chat."""
    try:
        # First verify project access
        proj = get_project(project_id, user_id, allow_community_access=True)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found or access denied")
        messages = get_chat_messages(project_id, chat_id, user_id)
        if messages is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return {"chat_id": chat_id, "messages": messages}
    except Exception as e:
        logging.error(f"Failed to get chat messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/chats")
def create_chat_endpoint(project_id: str, user_id: str = Query(...), title: str = Query(None)):
    """Create a new chat for a project."""
    try:
        # First verify project access
        proj = get_project(project_id, user_id, allow_community_access=True)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found or access denied")
        
        logging.info(f"Creating new chat for project {project_id} with user {user_id} and title {title}")
        chat_id = create_new_chat(project_id, user_id, title or "New Chat")
        logging.info(f"Created new chat with ID: {chat_id}")
        return {
            "chat_id": chat_id,
            "chat": {
                "id": chat_id,
                "project_id": project_id,
                "user_id": user_id,
                "title": title or "New Chat",
                "messages": [],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    except Exception as e:
        logging.error(f"Failed to create chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{project_id}/chats/{chat_id}")
def update_chat_endpoint(project_id: str, chat_id: str, user_id: str = Query(...), title: str = Body(...)):
    """Update a chat's title."""
    try:
        # First verify project access
        proj = get_project(project_id, user_id, allow_community_access=True)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found or access denied")
        success = update_chat_title(project_id, chat_id, user_id, title)
        if not success:
            raise HTTPException(status_code=404, detail="Chat not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}/chats/{chat_id}")
def delete_chat_endpoint(project_id: str, chat_id: str, user_id: str = Query(...)):
    """Delete a chat."""
    try:
        # First verify project access
        proj = get_project(project_id, user_id, allow_community_access=True)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found or access denied")
        success = delete_chat(project_id, chat_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chat not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------
# PROJECT MODEL
# ------------------
class ModelUpdateRequest(BaseModel):
    user_id: str
    provider: str
    model: str
    
@api_router.patch("/{project_id}/model")
async def update_project_model(project_id: str, request: ModelUpdateRequest):
    """Update the LLM model for a project."""
    available_models = get_available_models()
    if request.provider not in available_models or request.model not in available_models[request.provider]:
        raise HTTPException(status_code=400, detail="Invalid provider or model")
    try:
        # Get project first to check if it's a community repo
        proj = get_project(project_id, request.user_id, allow_community_access=True)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found")
            
        # For community repos, we need to use the admin's user ID for updates
        update_user_id = os.getenv("ADMIN_USER_ID") if proj.get("is_community") else request.user_id
        
        project = update_project(
            project_id=project_id,
            user_id=update_user_id,  # Use the correct user ID based on project type
            llm_provider=request.provider,
            llm_model=request.model
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"id": project_id, **project}
    except Exception as e:
        logging.error(f"Error updating model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
