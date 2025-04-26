from typing import Dict, Optional, Any
from datetime import datetime, timezone
import logging
from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, wait_exponential
from db import db
from models import Project
from user_store import get_or_create_user
from fastapi import HTTPException
from subscription_store import SubscriptionStore

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def list_projects(user_id: str) -> Dict[str, Dict[str, Any]]:
    """List all projects for a user, sorted by creation date (newest first)."""
    try:
        projects = {}
        cursor = db.projects.find({"user_id": user_id}).sort("created_at", -1)
        for doc in cursor:
            project_id = str(doc.pop("_id"))
            projects[project_id] = doc
        return projects
    except PyMongoError as e:
        logger.error(f"Failed to list projects: {e}")
        raise

def create_project(
    project_id: str,
    name: str,
    repoUrl: str,
    user_id: str,
    status: str = "new",
    api_project: bool = False,
    api_key_id: str = None,
    is_community: bool = False,
    community_repo_id: Optional[str] = None,
    branch_or_commit: Optional[str] = None
) -> dict:
    """Create a new project in MongoDB."""
    project = {
        "id": project_id,
        "name": name,
        "repoUrl": repoUrl,
        "user_id": user_id,
        "status": status,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "is_indexed": False,
        "last_indexed": None,
        "api_project": api_project,
        "api_key_id": api_key_id,
        "is_community": is_community,
        "community_repo_id": community_repo_id,
        "branch_or_commit": branch_or_commit
    }
    
    db.projects.insert_one(project)
    return project

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_project(project_id: str, user_id: str, allow_community_access: bool = False) -> Optional[Dict[str, Any]]:
    """Return a project from MongoDB, or None if not found.
    
    Args:
        project_id: The ID of the project to retrieve
        user_id: The ID of the requesting user
        allow_community_access: If True, allows access to community projects even if user_id doesn't match
    """
    try:
        # First try to find the project with exact user_id match
        doc = db.projects.find_one({"id": project_id, "user_id": user_id})
        
        # If not found and community access is allowed, check if it's a community project
        if not doc and allow_community_access:
            doc = db.projects.find_one({"id": project_id, "is_community": True})
            
        if doc:
            doc.pop("_id")  # Remove MongoDB's internal ID
            return doc
        return None
    except PyMongoError as e:
        logger.error(f"Failed to get project: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def update_project(project_id: str, user_id: str, **kwargs):
    """Update project fields in MongoDB."""
    try:
        # Make a copy of kwargs to avoid modifying the original
        updates = kwargs.copy()
        
        # Ensure all data is JSON serializable
        # Handle details dictionary specially for nested values
        if "details" in updates and isinstance(updates["details"], dict):
            for key, value in list(updates["details"].items()):
                if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    updates["details"][key] = str(value)
        
        update_data = {
            "$set": {
                **updates,
                "updated_at": datetime.now(timezone.utc)
            }
        }
        
        if kwargs.get("is_indexed") is True:
            update_data["$set"]["last_indexed"] = datetime.now(timezone.utc)
        
        # Handle progress updates
        if "progress" in kwargs:
            # Ensure progress is set directly in the update data and is JSON serializable
            progress_value = kwargs["progress"]
            
            # Convert any non-serializable objects to strings
            if isinstance(progress_value, dict):
                for key, value in list(progress_value.items()):
                    if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                        progress_value[key] = str(value)
            
            update_data["$set"]["indexing_progress"] = progress_value
            logger.info(f"Updating indexing progress for project {project_id}")
            # Remove progress from kwargs to avoid duplicate in update
            kwargs.pop("progress")
        
        result = db.projects.update_one(
            {"id": project_id, "user_id": user_id},
            update_data
        )
        
        if result.modified_count > 0:
            logger.info(f"Updated project {project_id}")
            return get_project(project_id, user_id)
        logger.warning(f"No changes made to project {project_id}")
        return None
    except PyMongoError as e:
        logger.error(f"Failed to update project: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def delete_project(project_id: str, user_id: str) -> bool:
    """Delete a project from MongoDB."""
    try:
        result = db.projects.delete_one({"id": project_id, "user_id": user_id})
        success = result.deleted_count > 0
        if success:
            logger.info(f"Deleted project {project_id}")
        return success
    except PyMongoError as e:
        logger.error(f"Failed to delete project: {e}")
        raise

class ProjectStore:
    def __init__(self):
        self.db = db
        self.subscription_store = SubscriptionStore()

    async def validate_repository_size(self, user_id: str, size_mb: float) -> None:
        """Validate repository size against user's subscription tier limits."""
        try:
            # Log the repository size for debugging
            logger.info(f"Validating repository size for user {user_id}: {size_mb:.1f}MB")
            
            # Get the user's subscription
            subscription = await self.subscription_store.get_subscription(user_id)
            
            # Check if subscription features exist and extract max repo size
            if not subscription or "features" not in subscription:
                logger.error(f"Invalid subscription object for user {user_id}")
                # Default to free tier limit
                max_size = 100
            else:
                max_size = subscription["features"]["maxRepoSize"]
            
            # Log the max size for the user's plan
            logger.info(f"User {user_id} max repo size: {max_size}MB (Plan: {subscription.get('tier', 'free')})")
            
            if size_mb > max_size:
                logger.warning(f"Repository size ({size_mb:.1f}MB) exceeds plan limit of {max_size}MB for user {user_id}")
                raise HTTPException(
                    status_code=402,  # Use 402 to indicate payment required
                    detail={
                        "error": "Repository size exceeds plan limit",
                        "current_size": round(size_mb, 1),
                        "size_limit": max_size,
                        "upgrade_message": f"Repository size ({size_mb:.1f}MB) exceeds your plan limit of {max_size}MB. Please upgrade to Pro for repositories up to 1GB."
                    }
                )
            logger.info(f"Repository size validation passed for user {user_id}: {size_mb:.1f}MB <= {max_size}MB")
        except Exception as e:
            logger.error(f"Error validating repository size: {e}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail="Failed to validate repository size")

    async def create_project(self, user_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project with size validation."""
        try:
            # Validate repository size
            repo_size = project_data.get("size_mb", 0)
            await self.validate_repository_size(user_id, repo_size)
            
            # Continue with existing create_project logic
            project_doc = {
                "user_id": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                **project_data
            }
            
            result = self.db.projects.insert_one(project_doc)
            project_doc["_id"] = str(result.inserted_id)
            return project_doc
            
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail="Failed to create project")
