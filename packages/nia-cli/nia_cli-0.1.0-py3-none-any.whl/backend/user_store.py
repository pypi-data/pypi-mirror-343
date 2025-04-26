import logging
from typing import Optional, Dict, Any
from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, wait_exponential
from db import db
from datetime import datetime, timezone
from bson import ObjectId
import httpx
import os

logger = logging.getLogger(__name__)

def sanitize_user_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Remove MongoDB-specific fields and ensure proper date formatting."""
    if not doc:
        return None
    
    # Remove MongoDB's _id
    doc.pop("_id", None)
    
    # Ensure dates are ISO format strings
    for field in ["created_at", "updated_at"]:
        if field in doc and isinstance(doc[field], datetime):
            doc[field] = doc[field].isoformat()
            
    return doc

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Return a user from MongoDB, or None if not found."""
    try:
        # First try by id (new format)
        doc = db.users.find_one({"id": user_id})
        if not doc:
            # Try legacy format
            doc = db.users.find_one({"user_id": user_id})
            if doc:
                # Migrate to new format
                doc["id"] = doc.pop("user_id")
                db.users.update_one(
                    {"_id": doc["_id"]}, 
                    {
                        "$set": {"id": doc["id"]}, 
                        "$unset": {"user_id": ""}
                    }
                )
        
        return sanitize_user_doc(doc)
    except PyMongoError as e:
        logger.error(f"Failed to get user: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def create_user(user_id: str) -> Dict[str, Any]:
    """Create a new user in MongoDB."""
    try:
        now = datetime.now(timezone.utc)
        user = {
            "id": user_id,
            "github_installation_id": None,
            "slack_user_ids": [],  # List of associated Slack user IDs
            "created_at": now,
            "updated_at": now
        }
        
        # Check if user already exists first
        existing = get_user(user_id)
        if existing:
            logger.warning(f"User {user_id} already exists")
            return existing
            
        result = db.users.insert_one(user)
        if not result.inserted_id:
            raise PyMongoError("Failed to insert user document")
            
        logger.info(f"Created new user {user_id}")
        return sanitize_user_doc(user)
    except PyMongoError as e:
        logger.error(f"Failed to create user: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_clerk_id_by_slack_id(slack_user_id: str) -> Optional[str]:
    """Get Clerk user ID associated with a Slack user ID."""
    try:
        logger.info(f"Looking up Clerk ID for Slack user {slack_user_id}")
        doc = db.users.find_one({"slack_user_ids": slack_user_id})
        if doc:
            clerk_id = doc.get("id")
            logger.info(f"Found Clerk ID {clerk_id} for Slack user {slack_user_id}")
            return clerk_id
        logger.warning(f"No Clerk ID found for Slack user {slack_user_id}")
        return None
    except PyMongoError as e:
        logger.error(f"Failed to get Clerk ID for Slack user: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def add_slack_user_id(clerk_user_id: str, slack_user_id: str) -> bool:
    """Associate a Slack user ID with a Clerk user."""
    try:
        logger.info(f"Adding Slack user ID {slack_user_id} to Clerk user {clerk_user_id}")
        
        # First check if this Slack ID is already associated with any user
        existing_user = db.users.find_one({"slack_user_ids": slack_user_id})
        if existing_user and existing_user.get("id") != clerk_user_id:
            logger.warning(f"Slack user {slack_user_id} is already associated with another user")
            return False

        # Ensure the user exists - use sync version to avoid recursion
        user = get_or_create_user_sync(clerk_user_id)
        if not user:
            logger.error(f"Could not find or create user {clerk_user_id}")
            return False

        # Add the Slack user ID to the user's slack_user_ids array if not already present
        result = db.users.update_one(
            {"id": clerk_user_id},
            {
                "$addToSet": {"slack_user_ids": slack_user_id},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )
        
        success = result.modified_count > 0 or result.matched_count > 0
        if success:
            logger.info(f"Successfully associated Slack user {slack_user_id} with Clerk user {clerk_user_id}")
        else:
            logger.warning(f"No changes made when adding Slack user {slack_user_id} to Clerk user {clerk_user_id}")
        return success
    except PyMongoError as e:
        logger.error(f"Failed to add Slack user ID: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_or_create_user_sync(user_id: str) -> Dict[str, Any]:
    """Get a user from MongoDB, creating them if they don't exist."""
    try:
        user = get_user(user_id)
        if not user:
            user = create_user(user_id)
        return sanitize_user_doc(user)
    except PyMongoError as e:
        logger.error(f"Failed to get or create user: {e}")
        raise

async def get_or_create_user(user_id: str) -> Dict[str, Any]:
    """Async version of get_or_create_user for use in async contexts."""
    # Correctly handle the async/sync distinction to avoid recursion
    try:
        # Call the synchronous function directly
        result = get_or_create_user_sync(user_id)
        return result
    except Exception as e:
        logger.error(f"Error in async get_or_create_user: {e}")
        # Return a minimal user object to avoid further errors
        return {"id": user_id}

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def update_user(user_id: str, updates: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[Dict[str, Any]]:
    """Update user fields in MongoDB."""
    try:
        # Combine updates from dict and kwargs
        update_data = {}
        if updates:
            update_data.update(updates)
        if kwargs:
            update_data.update(kwargs)
            
        if not update_data:
            logger.warning(f"No updates provided for user {user_id}")
            return get_user(user_id)

        # Ensure we're updating the correct user
        result = db.users.update_one(
            {"id": user_id},
            {
                "$set": {
                    **update_data,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
        if result.matched_count == 0:
            logger.warning(f"No user found with id {user_id}")
            return None
            
        if result.modified_count > 0:
            logger.info(f"Updated user {user_id}")
        else:
            logger.info(f"No changes needed for user {user_id}")
            
        return get_user(user_id)
    except PyMongoError as e:
        logger.error(f"Failed to update user: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
async def remove_slack_team_users(team_id: str):
    """Remove all Slack user IDs associated with a team when the app is uninstalled."""
    try:
        # First get all users with Slack IDs from this team
        async with httpx.AsyncClient() as client:
            # Get all users from the team using Slack's API
            response = await client.get(
                "https://slack.com/api/users.list",
                headers={
                    "Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"
                }
            )
            
            if not response.is_success:
                logger.error(f"Failed to get users from Slack team: {response.text}")
                return
            
            data = response.json()
            if not data.get("ok"):
                logger.error(f"Slack API error: {data.get('error')}")
                return
            
            # Get all user IDs from the team
            team_user_ids = [member["id"] for member in data["members"]]
            
            # Update all users who have these Slack IDs
            result = db.users.update_many(
                {"slack_user_ids": {"$in": team_user_ids}},
                {
                    "$pull": {"slack_user_ids": {"$in": team_user_ids}},
                    "$set": {"updated_at": datetime.now(timezone.utc)}
                }
            )
            
            logger.info(f"Removed Slack IDs for {result.modified_count} users from team {team_id}")
    except Exception as e:
        logger.error(f"Failed to remove Slack team users: {e}")
        raise
