from fastapi import APIRouter, HTTPException, Body, Query, Depends
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
import logging

from api_store import create_api_key, get_user_api_keys, delete_api_key, update_api_key
from project_store import list_projects
from subscription_store import get_subscription_tier

# API Key Models
class ApiKeyUsage(BaseModel):
    monthly_requests: int = 0
    monthly_tokens: int = 0
    last_reset: datetime
    current_minute_requests: int = 0
    current_minute_start: datetime

class ApiKeyCreate(BaseModel):
    user_id: str
    label: str

class CursorApiKeyCreate(BaseModel):
    user_id: str
    project_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ApiKeyLimits(BaseModel):
    monthly_request_limit: int = 10000
    rate_limit_requests: int = 60
    rate_limit_window: int = 60  # in seconds

class ApiKeyResponse(BaseModel):
    id: str
    key: str
    label: str
    user_id: str
    created_at: datetime
    last_used: Optional[datetime] = None
    usage: ApiKeyUsage
    limits: Optional[ApiKeyLimits] = None
    is_active: bool = True
    billing_rate: float = 0.1
    metadata: Optional[Dict[str, Any]] = None

class CursorApiKeyUpdate(BaseModel):
    key_id: str
    user_id: str
    project_id: Optional[str] = None

class ProjectInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str = "active"
    indexed_at: Optional[datetime] = None

class ProjectsResponse(BaseModel):
    projects: List[ProjectInfo]

# Create router
router = APIRouter(prefix="/api/keys", tags=["api-keys"])

@router.post("", response_model=ApiKeyResponse)
async def create_new_api_key(request: ApiKeyCreate):
    """Create a new API key for a user."""
    try:
        api_key = await create_api_key(request.user_id, request.label)
        return api_key
    except HTTPException as e:
        # Pass through HTTPExceptions directly to preserve status code and details
        raise e
    except Exception as e:
        logging.error(f"Error creating API key: {e}")
        raise HTTPException(status_code=500, detail="Failed to create API key")

@router.post("/cursor", response_model=ApiKeyResponse)
async def create_cursor_api_key(key_data: CursorApiKeyCreate):
    try:
        # Check if user has a Pro subscription
        user_tier = get_subscription_tier(key_data.user_id)
        
        if user_tier != "pro":
            raise HTTPException(
                status_code=403, 
                detail="Cursor integration is only available for Pro tier subscribers"
            )
        
        # Generate a label for the Cursor API key
        label = "Cursor Integration"
        
        # Create the API key with Cursor-specific metadata
        metadata = key_data.metadata or {}
        metadata["type"] = "cursor_integration"
        # Always include project_id in metadata, even if it's None
        metadata["project_id"] = key_data.project_id
        
        api_key = await create_api_key(
            user_id=key_data.user_id,
            label=label,
            metadata=metadata
        )
        
        return api_key
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating Cursor API key: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create Cursor API key: {str(e)}")

@router.get("", response_model=List[ApiKeyResponse])
async def list_api_keys(user_id: str):
    """List all API keys for a user."""
    try:
        keys = get_user_api_keys(user_id)
        return keys if keys else []
    except Exception as e:
        logging.error(f"Error listing API keys: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch API keys")

@router.delete("/{key_id}")
async def remove_api_key(key_id: str, user_id: str):
    """Delete an API key."""
    success = delete_api_key(user_id, key_id)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"success": True}

@router.put("/cursor/project", response_model=ApiKeyResponse)
async def update_cursor_api_key_project(update_data: CursorApiKeyUpdate):
    try:
        # Get the API key
        api_keys = get_user_api_keys(update_data.user_id)
        api_key = next((k for k in api_keys if k["id"] == update_data.key_id), None)
        
        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found")
        
        # Update the metadata with the new project ID
        if "metadata" not in api_key:
            api_key["metadata"] = {}
        
        # Always set project_id, even if it's None
        api_key["metadata"]["project_id"] = update_data.project_id
        
        # Save the updated API key
        updated_key = update_api_key(api_key)
        
        return updated_key
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating Cursor API key project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update API key project: {str(e)}")

@router.get("/cursor/projects", response_model=ProjectsResponse)
async def list_cursor_projects(user_id: str = Query(...)):
    try:
        # Get the user's projects
        projects_data = {}
        try:
            projects_data = list_projects(user_id)
        except Exception as project_error:
            logging.error(f"Error fetching projects for Cursor integration: {str(project_error)}")
            # Return empty projects rather than failing completely
            return ProjectsResponse(projects=[])
            
        # Convert the dictionary to a list of ProjectInfo objects
        # Check if projects_data is a dictionary with project IDs as keys
        if isinstance(projects_data, dict):
            projects_list = []
            for project_id, project_data in projects_data.items():
                # Ensure project_id is included in the data
                if isinstance(project_data, dict):
                    project_data['id'] = project_data.get('id', project_id)
                    projects_list.append(ProjectInfo(
                        id=project_data.get('id', project_id),
                        name=project_data.get('name', 'Unnamed Project'),
                        description=project_data.get('description'),
                        status=project_data.get('status', 'active'),
                        indexed_at=project_data.get('indexed_at')
                    ))
            
            # Format the response
            return ProjectsResponse(projects=projects_list)
        else:
            # If it's already a list or another format, try to convert each item
            projects_list = [
                ProjectInfo(
                    id=p.get('id') if isinstance(p, dict) else str(i),
                    name=p.get('name', 'Unnamed Project') if isinstance(p, dict) else str(p),
                    description=p.get('description') if isinstance(p, dict) else None,
                    status=p.get('status', 'active') if isinstance(p, dict) else 'active',
                    indexed_at=p.get('indexed_at') if isinstance(p, dict) else None
                )
                for i, p in enumerate(projects_data) if hasattr(projects_data, '__iter__')
            ]
            return ProjectsResponse(projects=projects_list)
    except Exception as e:
        logging.error(f"Error listing projects for Cursor integration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list projects: {str(e)}") 