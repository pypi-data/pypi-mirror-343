from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timezone, timedelta
from api_store import validate_api_key, get_api_key_usage
from uuid import uuid4
try:
    from utils.posthog import capture as posthog_capture
except ImportError:
    # Mock function if PostHog is not available
    def posthog_capture(*args, **kwargs):
        pass

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for API rate limiting and usage tracking."""
    
    def __init__(self, app):
        super().__init__(app)
        self.public_api_paths = {
            "/v2/repositories",
            "/v2/query",
            "/v2/repositories/{repository_id}"
        }
    
    def _ensure_datetime(self, value: Any, default_now: bool = False) -> datetime:
        """Convert various datetime formats to a proper timezone-aware datetime."""
        if value is None:
            return datetime.now(timezone.utc) if default_now else None
            
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value)
            except (ValueError, TypeError):
                dt = datetime.now(timezone.utc) if default_now else None
        elif isinstance(value, dict) and "$date" in value:
            # Handle MongoDB extended JSON format
            ts = value["$date"]
            if isinstance(ts, (int, float)):
                dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
            else:
                dt = datetime.now(timezone.utc) if default_now else None
        else:
            dt = datetime.now(timezone.utc) if default_now else None
            
        # Ensure timezone awareness
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        return dt or datetime.now(timezone.utc)

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip middleware for non-API routes
        if not any(request.url.path.startswith(path.split("{")[0]) for path in self.public_api_paths):
            return await call_next(request)
        
        api_key_doc = None
        try:
            # Extract and validate API key
            api_key_doc = self._get_api_key(request)
            if not api_key_doc:
                raise HTTPException(status_code=401, detail="Invalid or missing API key")
            
            # Process the request
            response = await call_next(request)
            
            # Add rate limit headers
            self._add_rate_limit_headers(response, api_key_doc)
            
            return response
            
        except HTTPException as e:
            if e.status_code == 429:  # Rate limit exceeded
                from fastapi.responses import JSONResponse
                response = JSONResponse(
                    content={"detail": str(e.detail)},
                    status_code=429
                )
                if api_key_doc:
                    self._add_rate_limit_headers(response, api_key_doc)
                return response
            raise e
    
    def _get_api_key(self, request: Request) -> Optional[dict]:
        """Extract and validate API key from request headers."""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        key = auth_header.replace("Bearer ", "")
        return validate_api_key(key)
    
    def _add_rate_limit_headers(self, response: Response, api_key_doc: Dict[str, Any]):
        """Add rate limit headers to response."""
        try:
            now = datetime.now(timezone.utc)
            
            # Safely get values with defaults
            usage = api_key_doc.get("usage", {})
            limits = api_key_doc.get("limits", {})
            
            monthly_requests = usage.get("monthly_requests", 0)
            monthly_limit = limits.get("monthly_request_limit", 10000)
            current_minute_requests = usage.get("current_minute_requests", 0)
            rate_limit = limits.get("rate_limit_requests", 60)
            
            # Calculate remaining requests
            remaining_monthly = max(0, monthly_limit - monthly_requests)
            remaining_minute = max(0, rate_limit - current_minute_requests)
            
            # Get and parse datetime fields
            current_minute_start = self._ensure_datetime(
                usage.get("current_minute_start"),
                default_now=True
            )
            last_reset = self._ensure_datetime(
                usage.get("last_reset"),
                default_now=True
            )
            
            # Calculate reset times
            minute_reset = (current_minute_start + timedelta(seconds=60)).timestamp()
            
            # Calculate next monthly reset
            if last_reset.month == 12:
                next_reset = datetime(last_reset.year + 1, 1, 1, tzinfo=timezone.utc)
            else:
                next_reset = datetime(last_reset.year, last_reset.month + 1, 1, tzinfo=timezone.utc)
            
            # Add headers
            response.headers.update({
                "X-RateLimit-Limit": str(rate_limit),
                "X-RateLimit-Remaining": str(remaining_minute),
                "X-RateLimit-Reset": str(int(minute_reset)),
                "X-Monthly-Limit": str(monthly_limit),
                "X-Monthly-Remaining": str(remaining_monthly),
                "X-Monthly-Reset": next_reset.isoformat(),
                "X-Billing-Rate": str(api_key_doc.get("billing_rate", 0.11))
            })
        except Exception as e:
            logger.error(f"Error adding rate limit headers: {e}")
            # Don't fail the request if we can't add headers 

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all API requests with correlation IDs."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
        start_time = datetime.now(timezone.utc)
        
        # Prepare request logging
        request_id = str(uuid4())
        client_host = request.client.host if request.client else "unknown"
        
        # Get user ID for tracking
        user_id = None
        api_key_doc = None
        
        # Try to extract user ID from auth header or API key
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            api_key = auth_header.replace("Bearer ", "")
            api_key_doc = validate_api_key(api_key)
            if api_key_doc and "user_id" in api_key_doc:
                user_id = str(api_key_doc["user_id"])
        
        # Use client IP + user agent as anonymous ID if no user ID
        anonymous_id = f"{client_host}_{request.headers.get('user-agent', 'unknown')}"
        distinct_id = user_id or anonymous_id
        
        # Log request
        logger.info(
            f"Request started",
            extra={
                "correlation_id": correlation_id,
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_host": client_host,
                "user_agent": request.headers.get("user-agent"),
            }
        )
        
        # Track request in PostHog
        event_properties = {
            "correlation_id": correlation_id,
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_host": client_host,
            "user_agent": request.headers.get("user-agent"),
        }
        
        posthog_capture(
            distinct_id=distinct_id,
            event="api_request",
            properties=event_properties
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Add correlation headers
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Request-ID"] = request_id
            
            # Calculate duration
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            # Log response
            logger.info(
                f"Request completed",
                extra={
                    "correlation_id": correlation_id,
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration": duration,
                }
            )
            
            # Track response in PostHog
            response_properties = {
                "correlation_id": correlation_id,
                "request_id": request_id,
                "status_code": response.status_code,
                "duration": duration,
                "method": request.method,
                "path": request.url.path,
            }
            
            posthog_capture(
                distinct_id=distinct_id,
                event="api_response",
                properties=response_properties
            )
            
            return response
            
        except Exception as e:
            # Calculate duration even for errors
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            # Log error
            logger.error(
                f"Request failed",
                extra={
                    "correlation_id": correlation_id,
                    "request_id": request_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration": duration,
                }
            )
            
            # Track error in PostHog
            error_properties = {
                "correlation_id": correlation_id,
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__,
                "method": request.method,
                "path": request.url.path,
                "duration": duration,
            }
            
            posthog_capture(
                distinct_id=distinct_id,
                event="api_error",
                properties=error_properties
            )
            
            raise

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response 

class FeatureAccessMiddleware(BaseHTTPMiddleware):
    """Middleware for checking feature access based on subscription tier."""
    
    def __init__(self, app):
        super().__init__(app)
        self.protected_paths = {
            # Integration endpoints
            "/api/github/": {"required_feature": "private_repos"},
            "/api/slack/": {"required_feature": "integrations"},
            # Multi-repo querying
            "/api/query/multi": {"required_feature": "multi_repo_querying"},
            # Chat endpoints (for credit tracking)
            "/api/chat/": {"required_feature": "chat_credits"},
        }
    
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        
        # Skip middleware for non-protected paths
        if not any(path.startswith(protected) for protected in self.protected_paths.keys()):
            return await call_next(request)
            
        try:
            # Get user from request state (set by auth middleware)
            user_id = request.state.user_id
            if not user_id:
                raise HTTPException(status_code=401, detail="Unauthorized")
                
            # Get user subscription details
            from subscription_store import SubscriptionStore
            subscription_store = SubscriptionStore()
            subscription = await subscription_store.get_subscription(user_id)
            
            # Check feature access
            for protected_path, requirements in self.protected_paths.items():
                if path.startswith(protected_path):
                    required_feature = requirements["required_feature"]
                    
                    # Special handling for chat credits
                    if required_feature == "chat_credits":
                        if subscription["creditsRemaining"] <= 0 and subscription["tier"] != "pro":
                            raise HTTPException(
                                status_code=403,
                                detail="No chat credits remaining. Please upgrade to Pro for unlimited chat."
                            )
                    # Check other feature access
                    elif not subscription["features"].get(required_feature, False):
                        raise HTTPException(
                            status_code=403,
                            detail=f"This feature requires a Pro subscription"
                        )
            
            # Store subscription in request state for later use
            request.state.subscription = subscription
            response = await call_next(request)
            
            # Deduct credit for chat endpoints if not Pro
            if path.startswith("/api/chat/") and subscription["tier"] != "pro":
                await subscription_store.deduct_credit(user_id)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in feature access middleware: {e}")
            raise HTTPException(status_code=500, detail="Internal server error") 