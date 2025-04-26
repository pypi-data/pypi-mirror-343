from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

def utc_now():
    """Helper function to get current UTC time."""
    return datetime.now().astimezone()

class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"

class UserFeatures(BaseModel):
    max_repo_size_mb: int = Field(default=20, description="Maximum repository size in MB")
    private_repos: bool = Field(default=False, description="Access to private repositories")
    multi_repo_querying: bool = Field(default=False, description="Ability to query multiple repositories")
    unlimited_chat: bool = Field(default=False, description="Unlimited codebase chat")
    credits_limit: int = Field(default=100, description="Monthly credits limit")
    integrations: List[str] = Field(default_factory=list, description="Enabled integrations")

    @classmethod
    def get_free_tier(cls) -> 'UserFeatures':
        """Get features for free tier."""
        return cls(
            max_repo_size_mb=20,
            private_repos=False,
            multi_repo_querying=False,
            unlimited_chat=False,
            credits_limit=100,
            integrations=[]
        )

    @classmethod
    def get_pro_tier(cls) -> 'UserFeatures':
        """Get features for pro tier."""
        return cls(
            max_repo_size_mb=2048,  # 2GB
            private_repos=True,
            multi_repo_querying=True,
            unlimited_chat=True,
            credits_limit=-1,  # Unlimited
            integrations=["slack", "github", "cursor"]
        )

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    
    # GitHub integration
    github_installation_id: Optional[int] = None
    
    # Stripe and subscription fields
    stripe_customer_id: Optional[str] = None
    subscription_tier: SubscriptionTier = Field(default=SubscriptionTier.FREE)
    subscription_status: SubscriptionStatus = Field(default=SubscriptionStatus.ACTIVE)
    subscription_id: Optional[str] = None
    subscription_updated_at: datetime = Field(default_factory=utc_now)
    subscription_period_end: Optional[datetime] = None
    
    # Usage tracking
    credits_remaining: int = Field(default=100, description="Monthly credits for codebase chat")
    credits_reset_date: datetime = Field(default_factory=utc_now)
    api_request_count: int = Field(default=0, description="Number of API requests made")
    last_api_request: Optional[datetime] = None
    
    # Feature configuration
    features: UserFeatures = Field(default_factory=UserFeatures.get_free_tier)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a specific feature is enabled for the user."""
        if self.subscription_tier == SubscriptionTier.PRO:
            return True
        return getattr(self.features, feature_name, False)
    
    def can_access_private_repos(self) -> bool:
        """Check if user can access private repositories."""
        return self.features.private_repos
    
    def can_use_multi_repo(self) -> bool:
        """Check if user can query multiple repositories."""
        return self.features.multi_repo_querying
    
    def has_credits_remaining(self) -> bool:
        """Check if user has credits remaining for codebase chat."""
        if self.features.unlimited_chat:
            return True
        return self.credits_remaining > 0
    
    def can_use_integration(self, integration: str) -> bool:
        """Check if user can use a specific integration."""
        return integration in self.features.integrations
    
    def can_handle_repo_size(self, size_mb: float) -> bool:
        """Check if user can handle a repository of given size."""
        return size_mb <= self.features.max_repo_size_mb

class NiaUser(BaseModel):
    user_id: str
    github_installation_id: Optional[str] = None
    
