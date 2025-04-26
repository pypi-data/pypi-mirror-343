from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import logging
from uuid import uuid4
from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, wait_exponential

from db import db
from models import CommunityRepo, CommunityRepoCreate

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def create_community_repo(repo_data: CommunityRepoCreate) -> CommunityRepo:
    """Create a new community repository."""
    repo_id = str(uuid4())
    repo_dict = repo_data.model_dump()
    repo_dict.update({
        "id": repo_id,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "status": "new",
        "is_indexed": False,
        "branch": repo_dict.get("default_branch")  # Set branch to default_branch initially
    })
    
    db.community_repos.insert_one(repo_dict)
    logger.info(f"Created new community repo: {repo_id}")
    return CommunityRepo(**repo_dict)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_community_repo(repo_id: str) -> Optional[CommunityRepo]:
    """Get a community repository by ID."""
    try:
        doc = db.community_repos.find_one({"id": repo_id})
        if doc:
            doc.pop("_id", None)
            return CommunityRepo(**doc)
        return None
    except PyMongoError as e:
        logger.error(f"Failed to get community repo: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def list_community_repos() -> List[CommunityRepo]:
    """List all indexed community repositories."""
    try:
        repos = []
        # Only fetch indexed repos
        cursor = db.community_repos.find({
            "is_indexed": True,
            "status": "indexed",
            "project_id": {"$exists": True, "$ne": None}
        })
        for doc in cursor:
            doc.pop("_id", None)
            repos.append(CommunityRepo(**doc))
        return repos
    except PyMongoError as e:
        logger.error(f"Failed to list community repos: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def update_community_repo(repo_id: str, update_data: Dict[str, Any]) -> bool:
    """Update a community repository."""
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # If we're updating the branch, make sure it's stored
    if "branch" not in update_data and "default_branch" in update_data:
        update_data["branch"] = update_data["default_branch"]
    
    result = db.community_repos.update_one(
        {"id": repo_id},
        {"$set": update_data}
    )
    return result.modified_count > 0

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def delete_community_repo(repo_id: str) -> bool:
    """Delete a community repository."""
    try:
        result = db.community_repos.delete_one({"id": repo_id})
        success = result.deleted_count > 0
        if success:
            logger.info(f"Deleted community repo: {repo_id}")
        return success
    except PyMongoError as e:
        logger.error(f"Failed to delete community repo: {e}")
        raise 