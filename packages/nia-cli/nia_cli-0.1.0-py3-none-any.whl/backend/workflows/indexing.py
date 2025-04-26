import os
import sys
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from hatchet_sdk import Hatchet, Context, sync_to_async
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger("workflows.indexing")

# Initialize Hatchet client
hatchet = Hatchet()

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import required modules
from index import index_repository as index_repo_func
from index import index_web_source
from db_helpers import sync_to_async_project_update, update_project_async
from db import MongoDB

# Initialize MongoDB
db = MongoDB()

@hatchet.workflow()
class IndexRepositoryWorkflow:
    @hatchet.step(timeout="3h")  # Match current 3-hour time limit
    async def index_repository(self, context: Context):
        """
        Hatchet workflow for indexing a repository.
        Replaces the Celery task 'worker.tasks.index_repository'.
        """
        # Get input data from workflow
        input_data = context.workflow_input()
        project_id = input_data["project_id"]
        user_id = input_data["user_id"]
        repo_url = input_data["repo_url"]
        branch_or_commit = input_data["branch_or_commit"]
        github_token = input_data.get("github_token")
        pinecone_index = input_data.get("pinecone_index", "nia-app")
        namespace = input_data.get("namespace")
        use_nuanced = input_data.get("use_nuanced", True)  # Default to True if not specified
        use_graph_rag = input_data.get("use_graph_rag", True)  # Enable GraphRAG by default
        api_initiated = input_data.get("api_initiated", False)  # Whether this was started via API
        
        workflow_run_id = context.workflow_run_id()
        logger.info(f"Starting indexing task for project {project_id}, run ID: {workflow_run_id}")
        logger.info(f"Setting use_nuanced={use_nuanced} and use_graph_rag={use_graph_rag}")
        
        # Initialize status
        status_data = {
            "status": "indexing",
            "progress": 0,
            "message": "Starting indexing job",
            "details": {
                "started_at": datetime.now().isoformat(),
                "workflow_run_id": workflow_run_id,
                "api_initiated": api_initiated,  # Track whether this came from API
                "nuanced_enabled": use_nuanced,  # Track whether Nuanced is enabled
                "graph_rag_enabled": use_graph_rag  # Track whether GraphRAG is enabled
            }
        }
        
        # Update initial status in database - properly handled for async
        try:
            await update_project_async(project_id=project_id, user_id=user_id, **status_data)
        except Exception as e:
            logger.error(f"Failed to update initial status: {e}")
        
        # Define an async callback function to track progress
        async def progress_callback(stage: str, message: str, progress: float, details: dict = None):
            if details is None:
                details = {}
            
            # Check if workflow has been canceled through Hatchet
            if context.done():
                logger.info(f"Task for project {project_id} was canceled")
                return {"status": "cancelled"}
            
            # Update status with progress information
            update_data = {
                "status": "indexing",
                "progress": int(progress),
                "message": message,
                "details": {
                    "stage": stage,
                    **(details or {}),
                    "workflow_run_id": workflow_run_id,
                    "updated_at": datetime.now().isoformat(),
                    "nuanced_enabled": use_nuanced,
                    "graph_rag_enabled": use_graph_rag  
                }
            }
            
            try:
                # Use the async-compatible version
                await update_project_async(project_id=project_id, user_id=user_id, **update_data)
                logger.debug(f"Updated progress: {progress}% - {message}")
            except Exception as e:
                logger.error(f"Error updating progress: {e}")
        
        try:
            # Create a unique temporary directory for this project
            temp_dir = f"/tmp/nia_repo_{project_id}_{int(time.time())}"
            
            # Run the async indexing function using await
            result = await index_repo_func(
                repo_url=repo_url,
                commit_hash=branch_or_commit,
                local_dir=temp_dir,  # Use the unique temp directory
                pinecone_index=pinecone_index,
                user_id=user_id,
                project_id=project_id,
                progress_callback=progress_callback,
                access_token=github_token,
                namespace=namespace,
                use_nuanced=use_nuanced,    # Pass the use_nuanced flag from workflow input
                use_graph_rag=use_graph_rag  # Pass the use_graph_rag flag from workflow input
            )
            
            # Update final status using async-compatible update function
            await update_project_async(
                project_id=project_id, 
                user_id=user_id,
                status="indexed",
                is_indexed=True,
                progress=100,
                message="Indexing completed successfully",
                last_indexed=datetime.now().isoformat(),
                use_nuanced=use_nuanced,    # Also include in final status
                use_graph_rag=use_graph_rag, # Also include in final status
                details={
                    "finished_at": datetime.now().isoformat(),
                    "result": result,
                    "workflow_run_id": workflow_run_id,
                    "nuanced_enabled": use_nuanced,
                    "graph_rag_enabled": use_graph_rag
                }
            )
            
            logger.info(f"Indexing task {workflow_run_id} completed successfully")
            logger.info(f"GraphRAG is {'enabled' if use_graph_rag else 'disabled'} for project {project_id}")
            return {"status": "completed", "result": result}
            
        except Exception as e:
            error_message = str(e)
            logger.exception(f"Error indexing repository: {error_message}")
            
            # Create more user-friendly error messages for common failures
            user_error_message = error_message
            
            # Check for common error patterns and provide better messages
            if "Failed to validate branch/commit" in error_message:
                if "Branch or commit" in error_message and "not found" in error_message:
                    # Branch/commit not found
                    user_error_message = f"The specified branch or commit '{branch_or_commit}' was not found in the repository. Please check the branch/commit name and try again."
                elif "Authentication required" in error_message:
                    # Authentication error
                    user_error_message = "This appears to be a private repository. Please install the GitHub App to access private repositories."
                elif "Permission denied" in error_message:
                    # Permission error
                    user_error_message = "Permission denied when accessing the repository. Please ensure you have access rights or install the GitHub App."
                elif "rate limit exceeded" in error_message.lower():
                    # Rate limit error
                    user_error_message = "GitHub API rate limit exceeded. You may need to install the GitHub App to increase rate limits."
                else:
                    # Generic validation error
                    user_error_message = f"Failed to validate repository branch/commit. Please check that the repository is accessible and try again. Error: {error_message}"
            
            # Update error status using async-compatible update function
            await update_project_async(
                project_id=project_id,
                user_id=user_id,
                status="error",
                error=user_error_message,  # Use more user-friendly message
                is_indexed=False,
                progress=-1,
                details={
                    "error": user_error_message,
                    "original_error": error_message,  # Keep the original error message for debugging
                    "finished_at": datetime.now().isoformat(),
                    "workflow_run_id": workflow_run_id,
                    "nuanced_enabled": use_nuanced,
                    "graph_rag_enabled": use_graph_rag
                }
            )
            
            # Return error state
            return {"status": "failed", "error": error_message}

@hatchet.workflow()
class WebIndexingWorkflow:
    @hatchet.step(timeout="1h")  # Match current 1-hour limit
    async def index_web_source(self, context: Context):
        """
        Hatchet workflow for indexing a web source.
        Replaces the Celery task 'worker.tasks.index_web_source_task'.
        """
        # Get workflow input
        input_data = context.workflow_input()
        source_id = input_data["source_id"]
        url = input_data["url"]
        user_id = input_data["user_id"]
        url_patterns = input_data.get("url_patterns")
        project_id = input_data.get("project_id")
        
        workflow_run_id = context.workflow_run_id()
        logger.info(f"Starting web indexing task for source {source_id}, run ID: {workflow_run_id}")
        
        # Update initial status
        await db.update_data_source(source_id, {
            "status": "processing",
            "progress": 0,
            "message": "Starting web source indexing",
            "updated_at": datetime.now().isoformat(),
            "details": {
                "workflow_run_id": workflow_run_id
            }
        })
        
        # Define progress callback
        async def progress_callback(progress_data):
            """Update data source status based on progress updates"""
            # Check if workflow has been canceled
            if context.done():
                return
                
            try:
                # Extract progress fields
                stage = progress_data.get("stage", "unknown")
                message = progress_data.get("message", "Processing...")
                progress_value = progress_data.get("progress", 0)
                
                # Create status update
                status_update = {
                    "status": "processing",
                    "message": message,
                    "progress": progress_value,
                    "updated_at": datetime.now().isoformat(),
                    "details": {
                        "stage": stage,
                        "workflow_run_id": workflow_run_id,
                        "updated_at": datetime.now().isoformat()
                    }
                }
                
                # Update data source status
                await db.update_data_source(source_id, status_update)
                logger.debug(f"Updated source {source_id} progress: {progress_value}% - {message}")
            except Exception as e:
                logger.error(f"Error updating progress for source {source_id}: {e}")
        
        try:
            # Get Firecrawl API key from environment
            api_key = os.environ.get("FIRECRAWL_API_KEY") or os.environ.get("FIRECRAWL_KEY") or os.environ.get("SCRAPEGPT_API_KEY")
            
            if not api_key:
                raise ValueError("Firecrawl API key not set in environment")
            
            # Create a dedicated namespace for this source
            namespace = f"web-sources_{user_id}_{source_id}"
            
            # Log parameters
            logger.info(f"Indexing web source: url={url}, source_id={source_id}, namespace={namespace}")
            if url_patterns:
                logger.info(f"Using URL patterns: {url_patterns}")
            
            # Run the async indexing function
            result = await index_web_source(
                url=url,
                allowed_patterns=url_patterns,
                user_id=user_id,
                project_id=project_id,
                progress_callback=progress_callback,
                namespace=namespace,
                api_key=api_key
            )
            
            # Process result
            if result.get("success", False):
                # Update data source status to completed
                await db.update_data_source(source_id, {
                    "status": "completed",
                    "page_count": result.get("document_count", 0),
                    "updated_at": datetime.now().isoformat(),
                    "message": f"Successfully indexed {result.get('document_count', 0)} pages",
                    "details": {
                        "workflow_run_id": workflow_run_id,
                        "finished_at": datetime.now().isoformat()
                    }
                })
                
                logger.info(f"Successfully indexed {result.get('document_count', 0)} pages from {url}")
                return {"success": True, "document_count": result.get("document_count", 0)}
            else:
                # Update data source status to failed
                error_message = result.get("message", "Unknown error during web indexing")
                await db.update_data_source(source_id, {
                    "status": "failed",
                    "error": error_message,
                    "updated_at": datetime.now().isoformat(),
                    "details": {
                        "workflow_run_id": workflow_run_id,
                        "finished_at": datetime.now().isoformat(),
                        "error": error_message
                    }
                })
                
                logger.error(f"Failed to index web source {url}: {error_message}")
                return {"success": False, "error": error_message}
        
        except Exception as e:
            error_message = str(e)
            logger.exception(f"Error indexing web source {url}: {error_message}")
            
            # Update data source status to failed
            await db.update_data_source(source_id, {
                "status": "failed",
                "error": error_message,
                "updated_at": datetime.now().isoformat(),
                "details": {
                    "workflow_run_id": workflow_run_id,
                    "finished_at": datetime.now().isoformat()
                }
            })
            
            return {"success": False, "error": error_message}

@hatchet.workflow()
class CancellableWorkflow:
    # For long-running steps, implement a synchronous version
    # that demonstrates proper cancellation handling
    @hatchet.step(timeout="3h")
    def long_running_job(self, context: Context):
        """Example of a synchronous long-running job with proper cancellation support"""
        # Get input data from workflow
        input_data = context.workflow_input()
        project_id = input_data["project_id"]
        user_id = input_data["user_id"]
        
        # Update initial status using synchronous method
        sync_to_async_project_update(
            project_id=project_id, 
            user_id=user_id,
            status="processing", 
            progress=0
        )
        
        total_steps = 100
        for i in range(total_steps):
            # Check if the workflow has been canceled
            if context.done():
                # Update status to cancelled
                sync_to_async_project_update(
                    project_id=project_id,
                    user_id=user_id,
                    status="cancelled",
                    progress=i,
                    message="Operation cancelled by user"
                )
                # Return early
                return {"status": "cancelled", "progress": i}
            
            # Simulate work
            context.sleep(1)  # Use context.sleep instead of time.sleep
            
            # Update progress (every 5%)
            if i % 5 == 0:
                progress = int((i / total_steps) * 100)
                sync_to_async_project_update(
                    project_id=project_id,
                    user_id=user_id,
                    status="processing",
                    progress=progress,
                    message=f"Processing step {i} of {total_steps}"
                )
        
        # Update final status
        sync_to_async_project_update(
            project_id=project_id,
            user_id=user_id,
            status="completed",
            progress=100,
            message="Processing completed successfully",
            is_indexed=True
        )
        
        return {"status": "completed", "progress": 100}