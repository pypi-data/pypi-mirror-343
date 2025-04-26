"""
Helper functions for database operations needed for Hatchet integration.

These functions provide async-compatible interfaces for working with
MongoDB in Hatchet workflows.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pymongo.errors import PyMongoError

from db import MongoDB
from project_store import update_project as sync_update_project

logger = logging.getLogger(__name__)

# Initialize MongoDB client
db = MongoDB()

# Import wrapped sync functions - using lazy import to avoid circular imports
def get_wrapped_functions():
    """Import and return wrapped functions to avoid circular imports"""
    try:
        from workflows.utils import update_project_async as update_project_wrapped
        from workflows.utils import get_project_async as get_project_wrapped
        return {
            "update_project_async": update_project_wrapped,
            "get_project_async": get_project_wrapped
        }
    except ImportError as e:
        # Fallback to synchronous versions if utils module is not available
        logger.warning(f"Could not import wrapped functions, using sync versions: {e}")
        from project_store import update_project, get_project
        return {
            "update_project_async": update_project,
            "get_project_async": get_project
        }

# Use the sync version directly for non-async contexts
from project_store import update_project as update_project_sync
from project_store import get_project as get_project_sync

async def update_project_async(project_id: str, user_id: str, **kwargs) -> Dict[str, Any]:
    """
    Async-compatible version of update_project for use in Hatchet workflows.
    
    This function properly handles progress updates and status tracking.
    """
    try:
        # Import here to avoid circular imports
        from workflows.utils import update_project_async as update_func
        
        # Call the wrapped function directly
        return await update_func(project_id, user_id, **kwargs)
    except Exception as e:
        logger.error(f"Error updating project {project_id} asynchronously: {e}")
        # Call the synchronous version directly as a fallback
        try:
            return sync_update_project(project_id, user_id, **kwargs)
        except Exception as inner_e:
            logger.error(f"Fallback update also failed: {inner_e}")
            # Return a formatted error response instead of raising
            return {
                "success": False, 
                "error": str(e), 
                "project_id": project_id,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

def sync_to_async_project_update(project_id: str, user_id: str, **kwargs) -> Dict[str, Any]:
    """
    Non-async version of project update for use in synchronous Hatchet steps.
    
    This is important when we need to update project status from a synchronous
    workflow step.
    """
    try:
        return update_project_sync(project_id, user_id, **kwargs)
    except Exception as e:
        logger.error(f"Error in sync project update for {project_id}: {e}")
        return {
            "success": False, 
            "error": str(e), 
            "project_id": project_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

def find_stale_projects(status: str, updated_before: datetime) -> List[Dict[str, Any]]:
    """Find projects that have been stuck in a specific status for too long"""
    try:
        cursor = db.db.projects.find({
            "status": status,
            "updated_at": {"$lt": updated_before}
        })
        
        projects = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            projects.append(doc)
        
        return projects
    except Exception as e:
        logger.error(f"Error finding stale projects: {e}")
        return []

def find_stale_data_sources(db, status: str, updated_before: datetime) -> List[Dict[str, Any]]:
    """
    Find data sources that have been stuck in a given status for too long
    
    Args:
        db: MongoDB instance
        status: Status to filter by (e.g., "processing")
        updated_before: Datetime threshold for last update
        
    Returns:
        List of stale data source documents
    """
    try:
        # Use client.nozomio.data_sources instead of get_collection
        query = {
            "status": status,
            "updated_at": {"$lt": updated_before.isoformat()}
        }
        
        # Using sync cursor methods
        cursor = db.client.nozomio.data_sources.find(query)
        result = []
        for doc in cursor:
            result.append(doc)
        return result
    except Exception as e:
        logger.error(f"Error finding stale data sources: {e}")
        return []

def perform_health_check(db) -> Dict[str, Any]:
    """
    Perform a health check on the database
    
    Args:
        db: MongoDB instance
        
    Returns:
        Health check result dictionary
    """
    try:
        # Run serverStatus command to check DB health
        status = db.client.admin.command("serverStatus")
        return {
            "status": "healthy",
            "connections": status.get("connections", {}).get("current", 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }