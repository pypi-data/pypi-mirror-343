import asyncio
from asyncio.log import logger
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Tuple
from uuid import uuid4
import secrets
import string
from db import db
import logging
from bson import ObjectId
from fastapi import HTTPException
from models import ApiKey, ApiUsageStats, ApiUsageLimits
from utils.stripe_meter import report_api_usage
import stripe
import os

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize a MongoDB document to a JSON-compatible dictionary."""
    if doc is None:
        return None
    
    result = {}
    for key, value in doc.items():
        if key == '_id':
            # Skip MongoDB's _id field
            continue
        elif isinstance(value, ObjectId):
            # Convert ObjectId to string
            result[key] = str(value)
        elif isinstance(value, datetime):
            # Convert datetime to ISO format string with UTC timezone
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            result[key] = value.isoformat()
        elif isinstance(value, dict):
            if "$date" in value:
                # Handle MongoDB extended JSON format
                ts = value["$date"]
                if isinstance(ts, (int, float)):
                    # Convert milliseconds to datetime
                    dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
                    result[key] = dt.isoformat()
                elif isinstance(ts, str):
                    # Already an ISO string
                    result[key] = ts
                else:
                    # Fallback to current time
                    result[key] = datetime.now(timezone.utc).isoformat()
            else:
                # Recursively serialize nested dictionaries
                result[key] = serialize_doc(value)
        elif isinstance(value, list):
            # Recursively serialize lists
            result[key] = [
                serialize_doc(item) if isinstance(item, dict)
                else item.isoformat() if isinstance(item, datetime)
                else str(item) if isinstance(item, ObjectId)
                else item
                for item in value
            ]
        else:
            result[key] = value
    return result

def generate_api_key(length: int = 32) -> str:
    """Generate a secure random API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

async def create_api_key(user_id: str, label: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a new API key for a user."""
    # Check if user has a payment method (Stripe customer)
    user = db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user has a Stripe customer ID (indicating they've added a payment method)
    if not user.get("stripe_customer_id"):
        raise HTTPException(status_code=403, detail="Please add a payment method in the billing section before creating an API key")
    
    # Check if user is on an active paid subscription
    subscription_tier = user.get("subscription_tier", "free")
    subscription_status = user.get("subscription_status", "inactive")
    
    # Allow API key creation based on subscription
    now = datetime.now(timezone.utc)
    key = generate_api_key()
    
    api_key_doc = ApiKey(
        id=str(uuid4()),
        key=key,
        label=label,
        user_id=user_id,
        created_at=now,
        usage=ApiUsageStats(
            monthly_requests=0,
            monthly_tokens=0,
            last_reset=now,
            current_minute_requests=0,
            current_minute_start=now
        ),
        limits=ApiUsageLimits(
            monthly_request_limit=10000,
            rate_limit_requests=60,
            rate_limit_window=60
        ),
        is_active=True,
        billing_rate=0.1  # $0.1 per request
    ).model_dump()
    
    # Add metadata if provided
    if metadata:
        api_key_doc["metadata"] = metadata
    
    result = db.api_keys.insert_one(api_key_doc)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create API key in database")
    
    return serialize_doc(api_key_doc)

def get_user_api_keys(user_id: str) -> List[Dict[str, Any]]:
    """Get all API keys for a user."""
    api_keys = list(db.api_keys.find({"user_id": user_id}))
    return [serialize_doc(key) for key in api_keys]

def update_api_key(api_key: Dict[str, Any]) -> Dict[str, Any]:
    """Update an API key in the database."""
    # Extract the ID for the query
    key_id = api_key.get("id")
    if not key_id:
        raise ValueError("API key must have an ID")
    
    # Perform the update
    result = db.api_keys.update_one(
        {"id": key_id},
        {"$set": {"metadata": api_key.get("metadata", {})}}
    )
    
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to update API key in database")
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Return the updated key document
    updated_key = db.api_keys.find_one({"id": key_id})
    return serialize_doc(updated_key)

async def delete_api_key(key_id: str, user_id: str) -> bool:
    """Delete an API key."""
    result = db.api_keys.delete_one({"id": key_id, "user_id": user_id})
    return result.deleted_count > 0

def simple_validate_api_key(key: str) -> bool:
    """
    A lightweight API key validation function that only checks if the key exists.
    This is used for fast API key verification during first connection attempts.
    Does not check rate limits or usage, just ensures the key is valid.
    """
    api_key = db.api_keys.find_one({"key": key}, {"_id": 1, "is_active": 1})
    return api_key is not None and api_key.get("is_active", True)

def validate_api_key(key: str) -> Optional[Dict[str, Any]]:
    """Validate API key and check rate limits."""
    api_key = db.api_keys.find_one({"key": key})
    if not api_key:
        return None
    
    if not api_key.get("is_active", True):
        raise HTTPException(status_code=403, detail="API key is inactive")
    
    now = datetime.now(timezone.utc)
    
    # Check monthly limits
    usage = api_key.get("usage", {})
    limits = api_key.get("limits", {})
    
    monthly_requests = usage.get("monthly_requests", 0)
    monthly_limit = limits.get("monthly_request_limit", 10000)
    if monthly_requests >= monthly_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Monthly request limit of {monthly_limit} exceeded"
        )
    
    # Check rate limits (requests per minute)
    current_minute_start = usage.get("current_minute_start", now)
    if isinstance(current_minute_start, str):
        try:
            current_minute_start = datetime.fromisoformat(current_minute_start)
        except ValueError:
            current_minute_start = now
    elif isinstance(current_minute_start, dict) and "$date" in current_minute_start:
        ts = current_minute_start["$date"]
        if isinstance(ts, (int, float)):
            current_minute_start = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
        else:
            current_minute_start = now
    
    # Ensure timezone awareness
    if current_minute_start.tzinfo is None:
        current_minute_start = current_minute_start.replace(tzinfo=timezone.utc)
        
    current_minute_requests = usage.get("current_minute_requests", 0)
    rate_limit = limits.get("rate_limit_requests", 60)
    
    # Reset minute counter if window has passed
    if (now - current_minute_start).total_seconds() >= 60:
        current_minute_requests = 0
        current_minute_start = now
    
    if current_minute_requests >= rate_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit of {rate_limit} requests per minute exceeded"
        )
    
    # Update last used timestamp and rate limit counters
    db.api_keys.update_one(
        {"key": key},
        {
            "$set": {
                "last_used": now,
                "usage.current_minute_start": current_minute_start,
                "usage.current_minute_requests": current_minute_requests + 1
            }
        }
    )
    
    return serialize_doc(api_key)

async def increment_api_usage(key: str, requests: int = 1, tokens: int = 0, idempotency_key: Optional[str] = None) -> Tuple[float, Dict[str, Any]]:
    """Increment usage counters and return the billing amount."""
    now = datetime.now(timezone.utc)
    
    # Get current API key doc
    api_key = db.api_keys.find_one({"key": key})
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Get user information for Stripe
    user_id = api_key.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="API key not associated with a user")
    
    user = db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user has a payment method
    stripe_customer_id = user.get("stripe_customer_id")
    if not stripe_customer_id:
        raise HTTPException(
            status_code=403, 
            detail="No payment method added. Please add a payment method in the billing section."
        )
    
    # Check if this is a Cursor integration key
    metadata = api_key.get("metadata", {})
    is_cursor_key = metadata.get("type") == "cursor_integration"
    subscription_tier = user.get("subscription_tier", "free")
    
    # If this is a Cursor key and user has Pro subscription, don't charge per request
    should_charge = True
    if is_cursor_key and subscription_tier == "pro":
        should_charge = False
    
    # Get the last reset time with proper handling of different formats
    usage = api_key.get("usage", {})
    last_reset_value = usage.get("last_reset")
    
    # Parse last_reset with proper format handling
    if isinstance(last_reset_value, datetime):
        last_reset = last_reset_value
    elif isinstance(last_reset_value, str):
        try:
            last_reset = datetime.fromisoformat(last_reset_value)
        except ValueError:
            last_reset = now
    elif isinstance(last_reset_value, dict) and "$date" in last_reset_value:
        ts = last_reset_value["$date"]
        if isinstance(ts, (int, float)):
            last_reset = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
        else:
            last_reset = now
    else:
        last_reset = now
    
    # Ensure timezone awareness
    if last_reset.tzinfo is None:
        last_reset = last_reset.replace(tzinfo=timezone.utc)
    
    # Reset monthly counters if needed
    if last_reset.month != now.month or last_reset.year != now.year:
        db.api_keys.update_one(
            {"key": key},
            {
                "$set": {
                    "usage.monthly_requests": 0,
                    "usage.monthly_tokens": 0,
                    "usage.last_reset": now
                }
            }
        )
        api_key["usage"]["monthly_requests"] = 0
        api_key["usage"]["monthly_tokens"] = 0
    
    # Calculate billing amount
    billing_rate = api_key.get("billing_rate", 0.1)  # Default to $0.1 per request
    billing_amount = requests * billing_rate
    
    # Increment counters
    db.api_keys.update_one(
        {"key": key},
        {
            "$inc": {
                "usage.monthly_requests": requests,
                "usage.monthly_tokens": tokens
            },
            "$set": {
                "usage.last_request": now
            }
        }
    )
    
    # Create a unique identifier for this usage record to prevent duplicates
    identifier = idempotency_key or f"{api_key.get('id')}_{now.strftime('%Y%m%d%H%M%S%f')}"
    
    # Get user subscription information
    subscription_id = user.get("subscription_id")
    subscription_status = user.get("subscription_status", "inactive")
    
    # Track whether any usage reporting method succeeded
    usage_reported = False
    error_messages = []
    
    # Skip Stripe usage reporting for Pro users with Cursor integration
    if not should_charge:
        logging.info(f"Skipping Stripe usage reporting for Pro user with Cursor integration (API key: {api_key.get('id')})")
        return billing_amount, api_key
    
    # Configure Stripe with the API key
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    
    # First try to report usage through subscription item if available and appropriate
    if subscription_id and subscription_status == "active" and subscription_tier == "pro":
        try:
            # Get subscription details
            subscription = stripe.Subscription.retrieve(subscription_id)
            usage_item = None
            
            # Find metered usage item in subscription
            for item in subscription.items.data:
                if hasattr(item.price, 'recurring') and item.price.recurring.usage_type == "metered":
                    usage_item = item
                    break
            
            # Report usage to subscription item if available
            if usage_item:
                stripe.SubscriptionItem.create_usage_record(
                    usage_item.id,
                    quantity=requests,
                    timestamp=int(now.timestamp()),
                    action="increment"
                )
                logging.info(f"Reported {requests} API requests to subscription item {usage_item.id}")
                usage_reported = True
        except Exception as e:
            error_message = f"Error reporting subscription usage: {e}"
            logging.error(error_message)
            error_messages.append(error_message)
            # Continue to meter event reporting if subscription reporting fails
    
    # If no active subscription with metered billing or subscription reporting failed, use meter events
    if not usage_reported:
        # Try to ensure user has a subscription with API usage product
        usage_reported = await ensure_customer_has_api_subscription(user, stripe_customer_id)
        
        # Report usage to Stripe using meter events API with retries
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries and not usage_reported:
            try:
                # Get the event name from env (default to "api_request")
                event_name = os.getenv("STRIPE_METER_EVENT_NAME", "api_request")
                
                # Create the meter event with idempotency key to prevent duplicate reporting
                response = stripe.billing.MeterEvent.create(
                    event_name=event_name,
                    payload={
                        "stripe_customer_id": stripe_customer_id,
                        "value": requests
                    },
                    timestamp=int(now.timestamp()),
                    identifier=identifier  # This serves as the idempotency key for meter events
                )
                
                logging.info(f"Successfully reported {requests} API requests to Stripe for customer {stripe_customer_id}")
                usage_reported = True
                
            except stripe.error.RateLimitError as e:
                # Handle rate limiting with exponential backoff
                retry_count += 1
                wait_time = 2 ** retry_count
                error_message = f"Rate limit hit, retrying in {wait_time} seconds"
                logging.warning(error_message)
                error_messages.append(error_message)
                await asyncio.sleep(wait_time)
            except stripe.error.APIConnectionError as e:
                # Handle network errors with retries
                retry_count += 1
                wait_time = 2 ** retry_count
                error_message = f"API connection error, retrying in {wait_time} seconds"
                logging.warning(error_message)
                error_messages.append(error_message)
                await asyncio.sleep(wait_time)
            except Exception as e:
                error_message = f"Error reporting API usage to Stripe: {e}"
                logging.error(error_message)
                error_messages.append(error_message)
                break
    
    # Update API key usage information
    updated_api_key = db.api_keys.find_one({"key": key})
    if updated_api_key and "_id" in updated_api_key:
        del updated_api_key["_id"]
        
    result = {
        "success": True,
        "api_key": updated_api_key,
        "billing_amount": billing_amount,
        "usage_reported": usage_reported,
        "subscription_found": bool(subscription_id),
        "subscription_id": subscription_id,
        "errors": error_messages
    }
    
    if not usage_reported:
        logging.warning(f"Failed to report API usage. Errors: {'; '.join(error_messages)}")
    
    # Return billing amount and updated API key info
    return billing_amount, result

async def ensure_customer_has_api_subscription(user: dict, stripe_customer_id: str) -> bool:
    """
    Ensure the customer has an active subscription with the API usage product.
    
    Args:
        user: User document as a dictionary
        stripe_customer_id: Stripe customer ID
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        
        # Check if customer already has an active subscription
        subscriptions = stripe.Subscription.list(
            customer=stripe_customer_id,
            status="active",
            limit=10
        )
        
        # Get the API usage price ID from environment
        api_usage_price_id = os.getenv("STRIPE_USAGE_PRICE_ID")
        if not api_usage_price_id:
            logging.error("STRIPE_USAGE_PRICE_ID not set in environment")
            return False
            
        # Check if any subscription has the API usage price
        has_api_usage = False
        # Ensure we're checking subscriptions.data - the iterable of subscription objects
        if hasattr(subscriptions, 'data'):
            subscription_list = subscriptions.data
        else:
            subscription_list = subscriptions  # Fallback if .data doesn't exist
            
        for subscription in subscription_list:
            # Ensure we're checking subscription.items.data correctly
            items_data = subscription.items.data if hasattr(subscription.items, 'data') else subscription.items
            for item in items_data:
                if item.price.id == api_usage_price_id:
                    has_api_usage = True
                    # Store this subscription ID for future reference
                    if not user.get("api_subscription_id"):
                        db.users.update_one(
                            {"id": user["id"]},
                            {"$set": {"api_subscription_id": subscription.id}}
                        )
                    return True
            
        # If no subscription with API usage, create one
        if not has_api_usage:
            # Generate idempotency key based on customer ID
            idempotency_key = f"api_sub_{stripe_customer_id}"
            
            # Create subscription with API usage product
            subscription = stripe.Subscription.create(
                customer=stripe_customer_id,
                items=[
                    {"price": api_usage_price_id}
                ],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                metadata={"user_id": user["id"], "subscription_type": "api_only"},
                idempotency_key=idempotency_key
            )
            
            # Update user record with subscription info
            update_data = {
                "api_subscription_id": subscription.id
            }
            
            # Only update main subscription if they don't already have one
            if not user.get("subscription_id"):
                update_data.update({
                    "subscription_id": subscription.id,
                    "subscription_status": "active"
                })
                
            db.users.update_one(
                {"id": user["id"]},
                {"$set": update_data}
            )
            
            logging.info(f"Created API usage subscription {subscription.id} for customer {stripe_customer_id}")
            return True
            
        return False
            
    except Exception as e:
        logging.error(f"Error ensuring API subscription: {e}")
        return False
        # Don't raise exception, just log the error

def get_api_key_usage(key: str) -> Dict[str, Any]:
    """Get detailed usage statistics for an API key."""
    api_key = db.api_keys.find_one({"key": key})
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    usage = api_key["usage"]
    limits = api_key["limits"]
    
    return {
        "usage": {
            "monthly_requests": usage["monthly_requests"],
            "monthly_tokens": usage["monthly_tokens"],
            "current_minute_requests": usage["current_minute_requests"],
            "last_reset": usage["last_reset"],
            "last_used": api_key.get("last_used")
        },
        "limits": {
            "monthly_request_limit": limits["monthly_request_limit"],
            "rate_limit_requests": limits["rate_limit_requests"],
            "rate_limit_window": limits["rate_limit_window"]
        },
        "billing_rate": api_key.get("billing_rate", 0.11)
    } 