import os
import stripe
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Configure Stripe API key
stripe.api_key = os.getenv("STRIPE_API_KEY")

# Set up logger
logger = logging.getLogger(__name__)

METER_EVENT_NAME = os.getenv("STRIPE_METER_EVENT_NAME", "api_usage")

async def report_subscription_usage(
    subscription_item_id: str, 
    quantity: int = 1, 
    timestamp: Optional[datetime] = None,
    idempotency_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Report API usage to Stripe via the SubscriptionItem.create_usage_record method.
    
    Args:
        subscription_item_id: The Stripe subscription item ID to bill
        quantity: Number of API requests to report (default: 1)
        timestamp: Optional timestamp for the event (default: current time)
        idempotency_key: Optional idempotency key for preventing duplicate reports
        
    Returns:
        The Stripe UsageRecord object
    """
    try:
        if not timestamp:
            timestamp = datetime.now()
            
        # Report to Stripe using the SubscriptionItem API
        idempotency_params = {}
        if idempotency_key:
            idempotency_params = {"idempotency_key": idempotency_key}
            
        usage_record = stripe.SubscriptionItem.create_usage_record(
            subscription_item_id,
            quantity=quantity,
            timestamp=int(timestamp.timestamp()),
            action="increment",
            **idempotency_params
        )
        
        logger.info(f"Reported {quantity} API requests for subscription item {subscription_item_id}")
        return usage_record
    except Exception as e:
        logger.error(f"Error reporting subscription usage to Stripe: {e}")
        # Don't raise - we don't want to block API calls if billing reporting fails
        return {"error": str(e)}

async def report_meter_event(
    stripe_customer_id: str, 
    quantity: int = 1, 
    timestamp: Optional[datetime] = None,
    idempotency_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Report API usage to Stripe via the billing.meter_event method.
    
    Args:
        stripe_customer_id: The Stripe customer ID to bill
        quantity: Number of API requests to report (default: 1)
        timestamp: Optional timestamp for the event (default: current time)
        idempotency_key: Optional idempotency key for preventing duplicate reports
        
    Returns:
        The Stripe Meter Event object
    """
    try:
        if not timestamp:
            timestamp = datetime.now(timezone.utc)
        
        # Generate idempotency key if not provided
        if not idempotency_key:
            # Create a unique key based on customer, quantity, and timestamp to prevent duplicates
            idempotency_key = f"meter_{stripe_customer_id}_{quantity}_{int(timestamp.timestamp())}"
            
        # Implement retry logic for network issues
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                # Report to Stripe Meter using the billing.MeterEvent.create API
                meter_event = stripe.billing.MeterEvent.create(
                    event_name=METER_EVENT_NAME,
                    payload={
                        "stripe_customer_id": stripe_customer_id,
                        "value": quantity
                    },
                    timestamp=int(timestamp.timestamp()),
                    identifier=idempotency_key  # This serves as the idempotency key
                )
                
                logger.info(f"Successfully reported {quantity} API requests as meter event for customer {stripe_customer_id}")
                return meter_event
            except stripe.error.RateLimitError:
                # Handle rate limiting with exponential backoff
                retry_count += 1
                wait_time = 2 ** retry_count
                logger.warning(f"Rate limit encountered, retrying in {wait_time}s")
                import asyncio
                await asyncio.sleep(wait_time)
            except stripe.error.APIConnectionError:
                # Network error, retry
                retry_count += 1
                wait_time = 2 ** retry_count
                logger.warning(f"API connection error, retrying in {wait_time}s")
                import asyncio
                await asyncio.sleep(wait_time)
            except Exception as e:
                last_error = e
                logger.error(f"Error reporting meter event to Stripe: {e}")
                break
        
        if last_error:
            logger.error(f"Failed to report meter event after retries: {last_error}")
        else:
            logger.error("Failed to report meter event after retries: Maximum retries reached")
            
        # Don't raise - we don't want to block API calls if billing reporting fails
        return {"error": str(last_error) if last_error else "Maximum retries reached"}
    except Exception as e:
        logger.error(f"Error reporting meter event to Stripe: {e}")
        # Don't raise - we don't want to block API calls if billing reporting fails
        return {"error": str(e)}

# Maintain backward compatibility and update the default implementation
report_api_usage = report_meter_event