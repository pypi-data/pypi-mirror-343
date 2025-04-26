from fastapi import APIRouter, HTTPException, Body, Query
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timezone

from user_store import get_user, get_or_create_user, update_user
from api_store import get_user_api_keys
try:
    from utils.posthog import capture, identify
except ImportError:
    # Mock functions if PostHog is not available
    def capture(*args, **kwargs):
        pass
    def identify(*args, **kwargs):
        pass

router = APIRouter(prefix="/user", tags=["users"])
api_router = APIRouter(prefix="/api", tags=["api"])
usage_router = APIRouter(tags=["usage"])

# ------------------
# USER DATA ENDPOINTS
# ------------------
@router.get("/{user_id}")
async def get_user_data(user_id: str):
    """Get user data including GitHub installation status."""
    try:
        # Use await with the async function for proper async/sync handling
        user_doc = await get_or_create_user(user_id)
        
        # Track user data fetch with PostHog
        capture(
            distinct_id=user_id,
            event="user_data_fetched",
            properties={
                "has_github_installation": bool(user_doc.get("github_installation_id")),
                "user_id": user_id
            }
        )
        
        # Identify the user in PostHog
        identify(
            distinct_id=user_id,
            properties={
                "github_installation_id": user_doc.get("github_installation_id"),
                "created_at": user_doc.get("created_at")
            }
        )
        
        return user_doc
    except Exception as e:
        logging.error(f"Error fetching user data: {e}")
        # Track error with PostHog
        capture(
            distinct_id=user_id,
            event="user_data_fetch_error",
            properties={
                "error": str(e),
                "user_id": user_id
            }
        )
        return {
            "id": user_id,
            "github_installation_id": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

# ------------------
# USAGE ENDPOINTS
# ------------------
@usage_router.get("/usage")
async def get_user_usage(user_id: str = Query(...)):
    """Get API usage statistics for a user."""
    logging.info(f"Fetching usage data for user: {user_id}")

    try:
        # Get all API keys for the user
        api_keys = get_user_api_keys(user_id)
        
        response_data = {
            "user_id": user_id,
            "summary": {
                "total_requests": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "monthly_limit": 0
            },
            "keys": []
        }

        if not api_keys:
            # Return empty structure if no keys
            logging.info(f"No API keys found for user {user_id}")
            # Track empty usage data with PostHog
            capture(
                distinct_id=user_id,
                event="user_usage_checked",
                properties={
                    "has_api_keys": False,
                    "user_id": user_id
                }
            )
            return response_data

        # Accumulate stats
        for key_doc in api_keys:
            usage = key_doc.get("usage", {})
            limits = key_doc.get("limits", {})
            rate = key_doc.get("billing_rate", 0.11)

            monthly_requests = usage.get("monthly_requests", 0)
            monthly_tokens = usage.get("monthly_tokens", 0)
            monthly_limit = limits.get("monthly_request_limit", 10000)
            cost = monthly_requests * rate  # Calculate cost based on requests and rate

            # Update summaries
            response_data["summary"]["total_requests"] += monthly_requests
            response_data["summary"]["total_tokens"] += monthly_tokens
            response_data["summary"]["total_cost"] += cost
            response_data["summary"]["monthly_limit"] += monthly_limit

            # Calculate usage percentage
            usage_pct = 0.0
            if monthly_limit > 0:
                usage_pct = (monthly_requests / monthly_limit) * 100

            # Add key info to response
            response_data["keys"].append({
                "id": key_doc.get("id"),
                "label": key_doc.get("label"),
                "monthly_requests": monthly_requests,
                "monthly_tokens": monthly_tokens,
                "monthly_limit": monthly_limit,
                "cost": round(cost, 2),
                "usage_percentage": round(usage_pct, 2),
                "last_used": key_doc.get("last_used")
            })

        # Round summary totals
        response_data["summary"]["total_cost"] = round(response_data["summary"]["total_cost"], 2)
        
        # Track usage data with PostHog
        capture(
            distinct_id=user_id,
            event="user_usage_checked",
            properties={
                "has_api_keys": True,
                "total_requests": response_data["summary"]["total_requests"],
                "total_cost": response_data["summary"]["total_cost"],
                "key_count": len(response_data["keys"]),
                "user_id": user_id
            }
        )
        
        return response_data

    except Exception as e:
        logging.error(f"Error fetching usage data: {e}")
        # Track error with PostHog
        capture(
            distinct_id=user_id,
            event="user_usage_check_error",
            properties={
                "error": str(e),
                "user_id": user_id
            }
        )
        raise HTTPException(status_code=500, detail=str(e))

# Export all routers to be included in main.py
routers = [router, api_router, usage_router] 