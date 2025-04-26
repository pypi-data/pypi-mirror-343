"""
Utilities for Hatchet workflows.

This module provides helper functions to make working with Hatchet
workflows more consistent and robust, especially for handling sync/async
operations and error tracking.
"""
import logging
import traceback
import asyncio
from datetime import datetime
from typing import Dict, Any, Callable, Optional
from functools import wraps
from hatchet_sdk import sync_to_async, Context

logger = logging.getLogger(__name__)

def handle_workflow_errors(func):
    """
    Decorator to handle errors in workflow steps consistently.
    Captures errors, logs them, and returns a structured error response.
    """
    @wraps(func)
    async def async_wrapper(self, context: Context, *args, **kwargs):
        try:
            return await func(self, context, *args, **kwargs)
        except Exception as e:
            error_message = str(e)
            logger.exception(f"Error in workflow step {func.__name__}: {error_message}")
            return {
                "status": "error",
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
                "traceback": traceback.format_exc()
            }
    
    @wraps(func)
    def sync_wrapper(self, context: Context, *args, **kwargs):
        try:
            return func(self, context, *args, **kwargs)
        except Exception as e:
            error_message = str(e)
            logger.exception(f"Error in workflow step {func.__name__}: {error_message}")
            return {
                "status": "error",
                "error": error_message,
                "timestamp": datetime.now().isoformat(),
                "traceback": traceback.format_exc()
            }
    
    # Return the appropriate wrapper based on if the decorated function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper

def with_progress_tracking(
    update_func: Callable, 
    project_id: str, 
    user_id: str
):
    """
    Creates a progress tracking callback function for use in workflow steps.
    
    Args:
        update_func: Function to call to update progress (can be sync or async)
        project_id: Project ID to update
        user_id: User ID for the project
        
    Returns:
        A callback function to use for progress tracking
    """
    async def async_progress_callback(stage: str, message: str, progress: float, details: Optional[Dict[str, Any]] = None):
        if details is None:
            details = {}
            
        update_data = {
            "status": "indexing",
            "progress": int(progress),
            "message": message,
            "details": {
                "stage": stage,
                **details,
                "updated_at": datetime.now().isoformat()
            }
        }
        
        try:
            await update_func(project_id=project_id, user_id=user_id, **update_data)
            logger.debug(f"Updated progress for {project_id}: {progress}% - {message}")
        except Exception as e:
            logger.error(f"Error updating progress for {project_id}: {e}")
    
    return async_progress_callback

# Wrap commonly used synchronous functions for async compatibility
def wrap_sync_functions():
    """
    Wrap synchronous functions with Hatchet's sync_to_async decorator for use in async workflows.
    Returns a dictionary of wrapped functions.
    """
    # Import synchronous functions to wrap
    from project_store import update_project, get_project, delete_project
    
    # Return a dictionary of wrapped functions
    return {
        "update_project": sync_to_async(update_project),
        "get_project": sync_to_async(get_project),
        "delete_project": sync_to_async(delete_project)
    }

# Create wrapped versions of synchronous functions
wrapped_funcs = wrap_sync_functions()

# Export the wrapped functions with descriptive names
update_project_async = wrapped_funcs["update_project"]
get_project_async = wrapped_funcs["get_project"]
delete_project_async = wrapped_funcs["delete_project"] 