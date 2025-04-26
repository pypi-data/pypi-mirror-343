from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging
from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, wait_exponential
from db import db
from models import Chat, Message

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_project_chats(project_id: str, user_id: str) -> Dict[str, Any]:
    """Get all chats for a project."""
    try:
        chats = {}
        cursor = db.chats.find({"project_id": project_id, "user_id": user_id})
        for doc in cursor:
            chat_id = doc["id"]
            doc.pop("_id")  # Remove MongoDB's internal ID
            chats[chat_id] = doc
        return chats
    except PyMongoError as e:
        logger.error(f"Failed to get project chats: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_chat_messages(project_id: str, chat_id: str, user_id: str) -> List[Dict[str, Any]]:
    """Get messages for a specific chat."""
    try:
        doc = db.chats.find_one({"project_id": project_id, "id": chat_id, "user_id": user_id})
        if doc:
            return doc.get("messages", [])
        return []
    except PyMongoError as e:
        logger.error(f"Failed to get chat messages: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def create_new_chat(project_id: str, user_id: str, title: str = "New Chat") -> str:
    """Create a new chat and return its ID."""
    try:
        chat_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        
        chat = Chat(
            id=chat_id,
            project_id=project_id,
            user_id=user_id,
            title=title
        )
        
        db.chats.insert_one(chat.model_dump())
        logger.info(f"Created new chat {chat_id} for project {project_id}")
        return chat_id
    except PyMongoError as e:
        logger.error(f"Failed to create new chat: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def update_chat_title(project_id: str, chat_id: str, user_id: str, title: str) -> bool:
    """Update a chat's title."""
    try:
        result = db.chats.update_one(
            {"project_id": project_id, "id": chat_id, "user_id": user_id},
            {
                "$set": {
                    "title": title,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        success = result.modified_count > 0
        if success:
            logger.info(f"Updated title for chat {chat_id}")
        return success
    except PyMongoError as e:
        logger.error(f"Failed to update chat title: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def add_chat_message(
    project_id: str,
    chat_id: str,
    role: str,
    content: str,
    user_id: str,
    sources: Optional[List[str]] = None,
    images: Optional[List[str]] = None
):
    """Add a message to a specific chat."""
    try:
        message = Message(role=role, content=content, sources=sources, images=images)
        
        # Get current chat to check title
        chat = db.chats.find_one({"project_id": project_id, "id": chat_id, "user_id": user_id})
        
        update_data = {
            "$push": {"messages": message.model_dump()},
            "$set": {"updated_at": datetime.now(timezone.utc)}
        }
        
        # Update title if it's the first user message and title is "New Chat"
        if (role == "user" and 
            chat and 
            chat.get("title") == "New Chat" and 
            len(chat.get("messages", [])) == 0):
            title = content[:50] + ("..." if len(content) > 50 else "")
            update_data["$set"]["title"] = title
        
        result = db.chats.update_one(
            {"project_id": project_id, "id": chat_id, "user_id": user_id},
            update_data
        )
        
        if result.modified_count > 0:
            logger.info(f"Added message to chat {chat_id}")
        else:
            logger.warning(f"Failed to add message to chat {chat_id}")
    except PyMongoError as e:
        logger.error(f"Failed to add chat message: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def delete_chat(project_id: str, chat_id: str, user_id: str) -> bool:
    """Delete a specific chat."""
    try:
        result = db.chats.delete_one({
            "project_id": project_id,
            "id": chat_id,
            "user_id": user_id
        })
        success = result.deleted_count > 0
        if success:
            logger.info(f"Deleted chat {chat_id}")
        return success
    except PyMongoError as e:
        logger.error(f"Failed to delete chat: {e}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def reset_chat(project_id: str, chat_id: str, user_id: str):
    """Clear messages from a specific chat."""
    try:
        result = db.chats.update_one(
            {"project_id": project_id, "id": chat_id, "user_id": user_id},
            {
                "$set": {
                    "messages": [],
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        if result.modified_count > 0:
            logger.info(f"Reset messages for chat {chat_id}")
        else:
            logger.warning(f"Failed to reset chat {chat_id}")
    except PyMongoError as e:
        logger.error(f"Failed to reset chat: {e}")
        raise
