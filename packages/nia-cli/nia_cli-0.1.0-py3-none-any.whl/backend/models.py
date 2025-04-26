from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from uuid import UUID

def utc_now():
    """Helper function to get current UTC time."""
    return datetime.now(timezone.utc)

class Message(BaseModel):
    role: str
    content: str
    sources: Optional[List[str]] = None
    images: Optional[List[str]] = None

class Chat(BaseModel):
    id: str
    project_id: str
    user_id: str
    title: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

class IndexingProgress(BaseModel):
    stage: str
    message: str
    progress: int

class Project(BaseModel):
    id: str
    user_id: str
    name: str
    repoUrl: str
    status: str = "new"
    is_indexed: bool = False
    is_community: bool = False
    community_repo_id: Optional[str] = None
    last_indexed: Optional[datetime] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    llm_provider: str = "anthropic"
    llm_model: str = "claude-3-7-sonnet-20250219"
    branch_or_commit: Optional[str] = None
    indexing_progress: IndexingProgress = IndexingProgress(
        stage="initializing",
        message="Not started",
        progress=0
    )

class ApiUsageLimits(BaseModel):
    monthly_request_limit: int = 10000  # Standard tier limit
    rate_limit_requests: int = 60  # Per minute
    rate_limit_window: int = 60  # Window in seconds

class ApiUsageStats(BaseModel):
    monthly_requests: int = 0
    monthly_tokens: int = 0
    last_reset: datetime = Field(default_factory=utc_now)
    current_minute_requests: int = 0
    current_minute_start: datetime = Field(default_factory=utc_now)

class ApiKey(BaseModel):
    id: str
    key: str
    label: str
    user_id: str
    created_at: datetime = Field(default_factory=utc_now)
    last_used: Optional[datetime] = None
    usage: ApiUsageStats
    limits: ApiUsageLimits = Field(default_factory=ApiUsageLimits)
    is_active: bool = True
    billing_rate: float = 0.11  # $0.11 per request

# Public API Models
class ApiError(BaseModel):
    """Standard error response for the API."""
    code: str
    message: str
    details: Optional[Dict] = None

class ApiResponse(BaseModel):
    """Standard success response wrapper for the API."""
    success: bool = True
    data: Optional[Dict] = None
    error: Optional[ApiError] = None

class RepositoryRequest(BaseModel):
    """Request model for repository indexing."""
    repository: str = Field(..., description="Repository identifier in owner/repo format")
    branch: Optional[str] = Field(None, description="Branch to index, defaults to main")
    reload: bool = Field(True, description="Whether to force reindex if already indexed")

class QueryRequest(BaseModel):
    """Request model for querying repositories."""
    messages: List[Dict[str, str]] = Field(..., description="List of chat messages")
    repositories: List[str] = Field(..., description="List of repository identifiers to query")
    stream: bool = Field(False, description="Whether to stream the response")
    temperature: float = Field(0.2, description="Model temperature for response generation")

class SourceReference(BaseModel):
    """Source reference in query responses."""
    file_path: str
    line_start: int
    line_end: int
    content: str
    relevance_score: float

class QueryResponse(BaseModel):
    """Response model for queries."""
    message: str
    sources: List[SourceReference]
    usage: Dict[str, int]

class FileTag(BaseModel):
    """Model for file tags"""
    id: str
    file_path: str
    tag_name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: str
    project_id: str

class FileSearchResult(BaseModel):
    """Model for file search results"""
    file_path: str
    score: float
    tags: List[str] = []
    description: Optional[str] = None
    metadata: Dict[str, Any] = {}

class FileTagCreate(BaseModel):
    """Model for creating file tags"""
    tag_name: str
    description: Optional[str] = None
    file_path: str
    project_id: str
    user_id: str

class FileTagResponse(BaseModel):
    """Model for file tag response"""
    id: str
    tag_name: str
    description: Optional[str] = None
    file_path: str
    created_at: datetime
    project_id: str
    user_id: str

class CommunityRepo(BaseModel):
    id: str
    name: str
    repo_url: str
    description: Optional[str] = None
    stars: Optional[int] = 0
    language: Optional[str] = None
    indexed_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    status: str = "new"
    is_indexed: bool = False
    project_id: Optional[str] = None
    branch: Optional[str] = None
    indexing_progress: IndexingProgress = Field(
        default_factory=lambda: IndexingProgress(
            stage="initializing",
            message="Not started",
            progress=0
        )
    )
    # GitHub metadata
    github_metadata: Optional[dict] = Field(default_factory=dict, description="GitHub repository metadata")
    github_updated_at: Optional[datetime] = None
    fork_count: Optional[int] = 0
    open_issues_count: Optional[int] = 0
    watchers_count: Optional[int] = 0
    default_branch: Optional[str] = None
    license: Optional[str] = None
    topics: List[str] = Field(default_factory=list)
    owner: Optional[dict] = None

class CommunityRepoCreate(BaseModel):
    name: str
    repo_url: str
    description: Optional[str] = None
    stars: Optional[int] = None
    language: Optional[str] = None

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    github_installation_id: Optional[int] = None
    api_keys: List[ApiKey] = Field(default_factory=list)
    # Pro subscription fields
    is_pro: bool = False
    pro_expires_at: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    pro_features: Dict[str, Any] = Field(
        default_factory=lambda: {
            "max_repo_size_mb": 2048,  # 1GB for pro users (consistent with UserFeatures)
            "max_repos": 100,  # 50 repos for pro users
            "max_api_requests": 100000,  # 100k API requests per month
            "priority_support": True
        }
    ) 