from typing import List, Optional
from datetime import datetime, timezone
from uuid import uuid4

from db import db as get_db
from models import FileTag, FileTagCreate, FileTagResponse

def create_file_tag(tag_data: FileTagCreate) -> FileTagResponse:
    """Create a new file tag"""
    db_conn = get_db()
    tag_id = str(uuid4())
    
    tag = FileTag(
        id=tag_id,
        file_path=tag_data.file_path,
        tag_name=tag_data.tag_name,
        description=tag_data.description,
        created_at=datetime.now(timezone.utc),
        user_id=tag_data.user_id,
        project_id=tag_data.project_id
    )
    
    db_conn.file_tags.insert_one(tag.model_dump())
    
    return FileTagResponse(**tag.model_dump())

def get_file_tags(project_id: str, user_id: str, file_path: Optional[str] = None) -> List[FileTagResponse]:
    """Get all file tags for a project, optionally filtered by file path"""
    db_conn = get_db()
    query = {"project_id": project_id, "user_id": user_id}
    
    if file_path:
        query["file_path"] = file_path
        
    tags = list(db_conn.file_tags.find(query))
    return [FileTagResponse(**tag) for tag in tags]

def delete_file_tag(tag_id: str, user_id: str) -> bool:
    """Delete a file tag"""
    db_conn = get_db()
    result = db_conn.file_tags.delete_one({"id": tag_id, "user_id": user_id})
    return result.deleted_count > 0

def get_files_by_tag(project_id: str, user_id: str, tag_name: str) -> List[str]:
    """Get all file paths that have a specific tag"""
    db_conn = get_db()
    query = {
        "project_id": project_id,
        "user_id": user_id,
        "tag_name": tag_name
    }
    
    tags = db_conn.file_tags.find(query)
    return list(set(tag["file_path"] for tag in tags))

def get_all_tags_for_project(project_id: str, user_id: str) -> List[str]:
    """Get all unique tag names used in a project"""
    db_conn = get_db()
    query = {"project_id": project_id, "user_id": user_id}
    
    tags = db_conn.file_tags.find(query)
    return list(set(tag["tag_name"] for tag in tags)) 