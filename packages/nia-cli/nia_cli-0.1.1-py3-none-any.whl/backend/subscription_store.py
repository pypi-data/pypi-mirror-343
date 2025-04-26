import os
from dotenv import load_dotenv
import stripe
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

from fastapi import HTTPException
from pydantic import BaseModel

from db import MongoDB
from modelsdb.user import User, SubscriptionTier, SubscriptionStatus, UserFeatures

logger = logging.getLogger(__name__)
load_dotenv()
# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Stripe product configuration
STRIPE_PRODUCTS = {
    "pro_monthly": {
        "price_id": os.getenv("STRIPE_PRO_MONTHLY_PRICE_ID"),
        "amount": 1499,  # $14.99
        "currency": "usd",
        "interval": "month",
        "features": UserFeatures.get_pro_tier()
    },
    "api_usage": {
        "price_id": os.getenv("STRIPE_USAGE_PRICE_ID"),
        "amount": 10,  # $0.10
        "currency": "usd",
        "usage_type": "metered",
        "aggregation": "sum"
    }
}

class SubscriptionStore:
    """Manages user subscriptions and Stripe integration."""
    
    def __init__(self):
        """Initialize the subscription store."""
        self.db = MongoDB()
        self.stripe = stripe
        self.stripe.api_key = os.getenv("STRIPE_API_KEY")
        self.logger = logging.getLogger(__name__)
        
    def safe_get_user(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Safely retrieve user information without requiring full User model validation.
        
        Args:
            query: MongoDB query to find the user
            
        Returns:
            User document as a dictionary, or None if not found
        """
        user_doc = self.db.users.find_one(query)
        if not user_doc:
            return None
            
        # Remove MongoDB-specific fields
        if "_id" in user_doc:
            del user_doc["_id"]
            
        return user_doc
        
    async def get_or_create_customer(self, user: User) -> str:
        """Get or create a Stripe customer for the user."""
        if user.stripe_customer_id:
            try:
                # Try to retrieve existing customer
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
                if not getattr(customer, 'deleted', False):
                    return user.stripe_customer_id
                else:
                    logger.info(f"Found deleted customer {user.stripe_customer_id}, will recreate")
            except stripe.error.InvalidRequestError as e:
                if 'No such customer' in str(e):
                    logger.info(f"Customer {user.stripe_customer_id} not found, will recreate")
                else:
                    raise
            except stripe.error.StripeError as e:
                logger.error(f"Error retrieving Stripe customer: {e}")
                raise
        
        try:
            # Create new customer
            customer = stripe.Customer.create(
                email=user.email,
                name=user.name,
                metadata={
                    "user_id": user.id
                }
            )
            
            # Update user record with new customer ID
            self.db.users.update_one(
                {"id": user.id},
                {"$set": {"stripe_customer_id": customer.id}}
            )
            
            logger.info(f"Created new customer {customer.id} for user {user.id}")
            return customer.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe customer: {e}")
            raise

    async def create_checkout_session(self, user: User, price_id: str, idempotency_key: Optional[str] = None, promotion_code: Optional[str] = None) -> Dict[str, Any]:
        """Create a Stripe Checkout Session for subscription."""
        try:
            customer_id = await self.get_or_create_customer(user)
            
            # Set up idempotency parameters
            idempotency_params = {}
            if idempotency_key:
                idempotency_params = {"idempotency_key": idempotency_key}
                
            # Set up the session parameters
            session_params = {
                "customer": customer_id,
                "payment_method_types": ["card"],
                "line_items": [
                    {
                        "price": price_id,
                        "quantity": 1
                    }
                ],
                "mode": "subscription",
                "success_url": f"{os.getenv('FRONTEND_URL')}/billing?success=true",
                "cancel_url": f"{os.getenv('FRONTEND_URL')}/billing?canceled=true",
                "metadata": {
                    "user_id": user.id,
                    "user_email": user.email
                },
                "subscription_data": {
                    "metadata": {
                        "user_id": user.id,
                        "user_email": user.email
                    },
                    "description": f"Subscription for {user.email}",
                    "trial_settings": {
                        "end_behavior": {
                            "missing_payment_method": "cancel"
                        }
                    }
                },
                **idempotency_params
            }
            
            # Add promotion code if provided
            if promotion_code and promotion_code.strip():
                try:
                    # Validate the promotion code exists before using it
                    promo_codes = stripe.PromotionCode.list(
                        code=promotion_code,
                        active=True,
                        limit=1
                    )
                    
                    if promo_codes.data:
                        # Valid promotion code found - apply it directly with discounts parameter
                        session_params["discounts"] = [{"promotion_code": promo_codes.data[0].id}]
                        logger.info(f"Applied promotion code {promotion_code} to checkout session for user {user.id}")
                    else:
                        # If no valid code found, let the user enter a code during checkout
                        session_params["allow_promotion_codes"] = True
                        logger.warning(f"Promotion code {promotion_code} not found or inactive")
                except stripe.error.StripeError as e:
                    # If there's an error validating the code, allow code entry during checkout
                    session_params["allow_promotion_codes"] = True
                    logger.warning(f"Error validating promotion code {promotion_code}: {e}")
            else:
                # No code provided, allow entry during checkout
                session_params["allow_promotion_codes"] = True
            
            # Create the checkout session
            session = stripe.checkout.Session.create(**session_params)
            
            return {"url": session.url, "session_id": session.id}
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create checkout session: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    async def handle_subscription_updated(self, subscription: Dict[str, Any]) -> None:
        """Handle subscription update events from Stripe."""
        try:
            customer_id = subscription.get("customer")
            subscription_id = subscription.get("id")
            status = subscription.get("status")
            
            logger.info(f"Processing subscription update: id={subscription_id}, status={status}, customer={customer_id}")
            
            # Get user by Stripe customer ID using safe method
            user_doc = self.safe_get_user({"stripe_customer_id": customer_id})
            if not user_doc:
                logger.warning(f"No user found for Stripe customer {customer_id}")
                return
                
            user_id = user_doc.get("id")
            if not user_id:
                logger.warning(f"Invalid user document for Stripe customer {customer_id}")
                return
                
            # Map subscription status to our enum
            subscription_status = SubscriptionStatus.CANCELED
            if status in ["active", "trialing"]:
                subscription_status = SubscriptionStatus.ACTIVE
            elif status in ["past_due", "unpaid"]:
                subscription_status = SubscriptionStatus.PAST_DUE
            elif status == "incomplete":
                subscription_status = SubscriptionStatus.INCOMPLETE
                
            # Determine subscription tier based on product IDs in subscription
            subscription_items = subscription.get("items", {}).get("data", [])
            subscription_tier = None
            
            for item in subscription_items:
                price = item.get("price", {})
                product_id = price.get("product")
                
                # Get product details
                product = stripe.Product.retrieve(product_id)
                product_name = product.get("name", "").lower()
                
                if "pro" in product_name:
                    subscription_tier = SubscriptionTier.PRO
                
            # Default to free tier if no matching tier found
            if not subscription_tier:
                subscription_tier = SubscriptionTier.FREE
                
            # Get the current period end
            current_period_end = datetime.fromtimestamp(subscription.get("current_period_end", 0))
            current_period_end_str = current_period_end.isoformat()
            
            # Update user with subscription info
            update_data = {
                "subscription_id": subscription_id,
                "subscription_tier": subscription_tier.value,
                "subscription_status": subscription_status.value,
                "subscription_current_period_end": current_period_end_str,
                "updated_at": datetime.now().astimezone()
            }
            
            logger.info(f"Updating user {user_id} with: tier={subscription_tier.value}, status={subscription_status.value}")
            
            self.db.users.update_one(
                {"id": user_id},
                {"$set": update_data}
            )
            
            logger.info(f"Updated user {user_id} with subscription {subscription_id} (tier: {subscription_tier.value}, status: {subscription_status.value})")
            
            # For Pro subscriptions, ensure API usage item is included
            if subscription_tier == SubscriptionTier.PRO and subscription_status == SubscriptionStatus.ACTIVE:
                # Get API usage price ID
                api_usage_price_id = os.getenv("STRIPE_USAGE_PRICE_ID")
                if not api_usage_price_id:
                    logger.error("STRIPE_USAGE_PRICE_ID not set in environment")
                    return
                
                # Check if subscription already has API usage price
                has_api_usage = False
                for item in subscription_items:
                    if item.get("price", {}).get("id") == api_usage_price_id:
                        has_api_usage = True
                        break
                
                # If not, add it
                if not has_api_usage:
                    try:
                        # Try to find existing subscription item for this price first
                        existing_items = stripe.SubscriptionItem.list(
                            subscription=subscription_id
                        )
                        
                        existing_item_id = None
                        for item in existing_items.data:
                            if item.price.id == api_usage_price_id:
                                existing_item_id = item.id
                                break
                        
                        # If existing item found, update it instead of creating a new one
                        if existing_item_id:
                            logger.info(f"Found existing subscription item {existing_item_id} for API usage price")
                        else:
                            # Add API usage price to subscription
                            stripe.SubscriptionItem.create(
                                subscription=subscription_id,
                                price=api_usage_price_id,
                                idempotency_key=f"add_api_{subscription_id}"
                            )
                            logger.info(f"Added API usage item to subscription {subscription_id}")
                    except stripe.error.InvalidRequestError as e:
                        # Handle the specific error about existing subscription items
                        if "existing Subscription Item" in str(e) and "is already using that Price" in str(e):
                            logger.warning(f"API usage item already exists on subscription {subscription_id}: {e}")
                        else:
                            logger.error(f"Error adding API usage to subscription: {e}")
                    except stripe.error.StripeError as e:
                        logger.error(f"Error adding API usage to subscription: {e}")
            
        except Exception as e:
            logger.error(f"Error processing subscription update: {e}")

    async def handle_subscription_deleted(self, subscription: Dict[str, Any]) -> None:
        """Handle subscription deleted webhook event."""
        try:
            # Try to get user ID from subscription metadata
            user_id = subscription.get("metadata", {}).get("user_id")
            
            # If not in metadata, try to find by customer ID
            if not user_id:
                customer_id = subscription.get("customer")
                if customer_id:
                    user_doc = self.safe_get_user({"stripe_customer_id": customer_id})
                    if user_doc:
                        user_id = user_doc.get("id")
            
            if not user_id:
                logger.error(f"No user_id found for subscription: {subscription.get('id')}")
                return
                
            logger.info(f"Processing subscription deletion for user: {user_id}")
            
            # Reset user to free tier with default features
            update_data = {
                "subscription_tier": SubscriptionTier.FREE.value,
                "subscription_status": SubscriptionStatus.CANCELED.value,
                "subscription_id": None,
                "features": UserFeatures.get_free_tier().dict(),
                "updated_at": datetime.now().astimezone()
            }
            
            result = self.db.users.update_one(
                {"id": user_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Reset user {user_id} to free tier after subscription cancellation")
            else:
                logger.warning(f"No changes made to subscription for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error processing subscription deletion: {e}", exc_info=True)

    async def handle_invoice_payment_succeeded(self, invoice: Dict[str, Any]) -> None:
        """Handle invoice.payment_succeeded webhook event."""
        try:
            # Get customer and subscription information
            customer_id = invoice.get("customer")
            subscription_id = invoice.get("subscription")
            invoice_id = invoice.get("id")
            
            logger.info(f"Processing invoice payment success: id={invoice_id}, customer={customer_id}, subscription={subscription_id}")
            
            if not customer_id:
                logger.error(f"No customer ID in invoice: {invoice_id}")
                return
                
            # Find user by Stripe customer ID
            user_doc = self.safe_get_user({"stripe_customer_id": customer_id})
            if not user_doc:
                logger.error(f"No user found for Stripe customer: {customer_id}")
                return
                
            user_id = user_doc.get("id")
            logger.info(f"Processing invoice payment success for user: {user_id}")
            
            # If this is for a subscription, update the subscription status
            if subscription_id:
                # Fetch the latest subscription details
                try:
                    subscription = stripe.Subscription.retrieve(subscription_id)
                    await self.handle_subscription_updated(subscription)
                except stripe.error.StripeError as e:
                    logger.error(f"Failed to retrieve subscription {subscription_id}: {e}")
            
            # Update payment history
            payment_data = {
                "invoice_id": invoice_id,
                "amount_paid": invoice.get("amount_paid", 0) / 100,  # Convert cents to dollars
                "status": "succeeded",
                "currency": invoice.get("currency", "usd"),
                "created_at": datetime.fromtimestamp(invoice.get("created", datetime.now().timestamp())),
                "billing_reason": invoice.get("billing_reason"),
                "hosted_invoice_url": invoice.get("hosted_invoice_url")
            }
            
            # Add payment record to user's payment history and update status
            self.db.users.update_one(
                {"id": user_id},
                {
                    "$push": {
                        "payment_history": payment_data
                    },
                    "$set": {
                        "last_payment_status": "succeeded",
                        "last_payment_date": datetime.now().astimezone(),
                        "updated_at": datetime.now().astimezone()
                    }
                }
            )
            
            logger.info(f"Successfully processed invoice payment for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error processing invoice payment: {e}", exc_info=True)

    async def handle_invoice_payment_failed(self, invoice: Dict[str, Any]) -> None:
        """Handle invoice.payment_failed webhook event."""
        try:
            # Get customer and subscription information
            customer_id = invoice.get("customer")
            subscription_id = invoice.get("subscription")
            
            if not customer_id:
                logger.error(f"No customer ID in invoice: {invoice.get('id')}")
                return
                
            # Find user by Stripe customer ID
            user_doc = self.safe_get_user({"stripe_customer_id": customer_id})
            if not user_doc:
                logger.error(f"No user found for Stripe customer: {customer_id}")
                return
                
            user_id = user_doc.get("id")
            logger.info(f"Processing invoice payment failure for user: {user_id}")
            
            # If this is for a subscription, update the subscription status
            if subscription_id:
                # Fetch the latest subscription details
                try:
                    subscription = stripe.Subscription.retrieve(subscription_id)
                    # The subscription status should be updated automatically by Stripe to past_due
                    await self.handle_subscription_updated(subscription)
                except stripe.error.StripeError as e:
                    logger.error(f"Failed to retrieve subscription {subscription_id}: {e}")
            
            # Update payment history
            payment_data = {
                "invoice_id": invoice.get("id"),
                "amount_due": invoice.get("amount_due", 0) / 100,  # Convert cents to dollars
                "status": "failed",
                "currency": invoice.get("currency", "usd"),
                "created_at": datetime.fromtimestamp(invoice.get("created", datetime.now().timestamp())),
                "billing_reason": invoice.get("billing_reason"),
                "attempt_count": invoice.get("attempt_count", 1),
                "next_payment_attempt": invoice.get("next_payment_attempt")
            }
            
            # Add payment record to user's payment history and update status
            self.db.users.update_one(
                {"id": user_id},
                {
                    "$push": {
                        "payment_history": payment_data
                    },
                    "$set": {
                        "last_payment_status": "failed",
                        "last_payment_date": datetime.now().astimezone(),
                        "updated_at": datetime.now().astimezone()
                    }
                }
            )
            
            logger.info(f"Recorded failed payment for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error processing invoice payment failure: {e}", exc_info=True)

    async def handle_payment_intent_succeeded(self, payment_intent: Dict[str, Any]) -> None:
        """Handle payment_intent.succeeded webhook event."""
        try:
            # Get customer information
            customer_id = payment_intent.get("customer")
            
            if not customer_id:
                logger.error(f"No customer ID in payment intent: {payment_intent.get('id')}")
                return
                
            # Find user by Stripe customer ID
            user = self.db.users.find_one({"stripe_customer_id": customer_id})
            if not user:
                logger.error(f"No user found for Stripe customer: {customer_id}")
                return
                
            user_id = user.get("id")
            logger.info(f"Processing payment intent success for user: {user_id}")
            
            # This could be a setup intent for adding a payment method
            # Update user's payment method information
            self.db.users.update_one(
                {"id": user_id},
                {
                    "$set": {
                        "has_payment_method": True,
                        "last_payment_method_update": datetime.now().astimezone(),
                        "updated_at": datetime.now().astimezone()
                    }
                }
            )
            
            logger.info(f"Successfully processed payment intent success for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error processing payment intent success: {e}", exc_info=True)

    async def handle_payment_intent_failed(self, payment_intent: Dict[str, Any]) -> None:
        """Handle payment_intent.failed webhook event."""
        try:
            # Get customer information
            customer_id = payment_intent.get("customer")
            
            if not customer_id:
                logger.error(f"No customer ID in payment intent: {payment_intent.get('id')}")
                return
                
            # Find user by Stripe customer ID
            user = self.db.users.find_one({"stripe_customer_id": customer_id})
            if not user:
                logger.error(f"No user found for Stripe customer: {customer_id}")
                return
                
            user_id = user.get("id")
            logger.info(f"Processing payment intent failure for user: {user_id}")
            
            # Get the error information
            error = payment_intent.get("last_payment_error", {})
            error_message = error.get("message", "Unknown error")
            error_code = error.get("code", "unknown")
            
            # Update user record with payment failure information
            self.db.users.update_one(
                {"id": user_id},
                {
                    "$set": {
                        "last_payment_error": {
                            "message": error_message,
                            "code": error_code,
                            "date": datetime.now().astimezone()
                        },
                        "updated_at": datetime.now().astimezone()
                    }
                }
            )
            
            logger.info(f"Successfully processed payment intent failure for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error processing payment intent failure: {e}", exc_info=True)

    async def cancel_subscription(self, user: User) -> None:
        """Cancel user's subscription."""
        if not user.subscription_id:
            raise HTTPException(status_code=400, detail="No active subscription")
            
        try:
            subscription = stripe.Subscription.modify(
                user.subscription_id,
                cancel_at_period_end=True
            )
            
            # Update user's subscription status
            self.db.users.update_one(
                {"id": user.id},
                {
                    "$set": {
                        "subscription_status": SubscriptionStatus.CANCELED,
                        "subscription_updated_at": datetime.now().astimezone()
                    }
                }
            )
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription: {e}")
            raise HTTPException(status_code=400, detail="Failed to cancel subscription")

    async def create_portal_session(self, user: User, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """Create a Stripe Customer Portal session."""
        if not user.stripe_customer_id:
            raise HTTPException(status_code=400, detail="No Stripe customer found")
            
        try:
            # Set up idempotency parameters
            idempotency_params = {}
            if idempotency_key:
                idempotency_params = {"idempotency_key": idempotency_key}
                
            session = stripe.billing_portal.Session.create(
                customer=user.stripe_customer_id,
                return_url=f"{os.getenv('FRONTEND_URL')}/billing",
                **idempotency_params
            )
            return {"url": session.url}
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create portal session: {e}")
            raise HTTPException(status_code=400, detail="Failed to create portal session")

    async def report_api_usage(self, user: User, request_count: int = 1) -> None:
        """Report API usage to Stripe for metered billing."""
        if not user.subscription_id:
            return
            
        try:
            # Get subscription items
            subscription = stripe.Subscription.retrieve(user.subscription_id)
            
            # Safely access items, handling both object.data and direct iterable cases
            items = subscription.items.data if hasattr(subscription.items, 'data') else subscription.items
            
            usage_item = next(
                (item for item in items if item.price.recurring.usage_type == "metered"),
                None
            )
            
            if usage_item:
                # Report usage
                stripe.SubscriptionItem.create_usage_record(
                    usage_item.id,
                    quantity=request_count,
                    timestamp=int(datetime.now().timestamp()),
                    action="increment"
                )
        except stripe.error.StripeError as e:
            logger.error(f"Failed to report API usage: {e}")
            # Don't raise exception, just log error
            # We don't want to block the API call if usage reporting fails 

    async def get_subscription(self, user_id: str) -> Dict[str, Any]:
        """Get user's subscription details."""
        try:
            # Get user from database
            user_doc = self.db.users.find_one({"id": user_id})
            if not user_doc:
                # Return free tier defaults if user not found
                logger.info(f"No user found for {user_id}, returning free tier defaults")
                return {
                    "tier": "free",
                    "status": "active",
                    "currentPeriodEnd": datetime.now().astimezone() + timedelta(days=30),
                    "features": UserFeatures.get_free_tier().dict()
                }

            # If user has Stripe subscription, get latest details
            # Only check with Stripe if the last check was more than 30 minutes ago
            # to reduce API calls to Stripe and improve performance
            last_stripe_check = user_doc.get("last_stripe_check")
            should_check_stripe = True
            
            if last_stripe_check:
                try:
                    # Parse datetime from string or datetime object
                    last_check_time = self._ensure_datetime(last_stripe_check)
                    now = datetime.now().astimezone()
                    # Only check Stripe if it's been more than 30 minutes since last check
                    if (now - last_check_time).total_seconds() < 1800:  # 30 minutes
                        should_check_stripe = False
                        logger.info(f"Skipping Stripe check for user {user_id} - last check was recent")
                except Exception as e:
                    logger.error(f"Error parsing last_stripe_check time: {e}")
            
            if user_doc.get("subscription_id") and should_check_stripe:
                try:
                    # Create a RequestsClient with timeout and use it directly
                    client = stripe.http_client.RequestsClient(timeout=3.0)
                    # Temporarily set as the client for this call
                    old_client = stripe.default_http_client
                    stripe.default_http_client = client
                    
                    try:
                        subscription = stripe.Subscription.retrieve(user_doc["subscription_id"])
                        # Update subscription status if needed
                        if subscription.status != user_doc.get("subscription_status"):
                            # Call handle_subscription_updated asynchronously
                            await self.handle_subscription_updated(subscription)
                            user_doc = self.db.users.find_one({"id": user_id})
                    finally:
                        # Restore the original client
                        stripe.default_http_client = old_client
                    
                    # Update last stripe check time
                    self.db.users.update_one(
                        {"id": user_id},
                        {"$set": {"last_stripe_check": datetime.now().astimezone()}}
                    )
                except stripe.error.StripeError as e:
                    logger.error(f"Failed to fetch Stripe subscription: {e}")
                    # Don't fail the request, continue with database data
                except Exception as e:
                    logger.error(f"Unexpected error fetching Stripe subscription: {e}")

            # Get features based on subscription tier
            features = (
                UserFeatures.get_pro_tier() if user_doc.get("subscription_tier") == "pro"
                else UserFeatures.get_free_tier()
            )
            
            # Return subscription data in camelCase format
            return {
                "tier": user_doc.get("subscription_tier", "free"),
                "status": user_doc.get("subscription_status", "active"),
                "currentPeriodEnd": user_doc.get("subscription_period_end", datetime.now().astimezone() + timedelta(days=30)),
                "features": {
                    "maxRepoSize": features.max_repo_size_mb,
                    "privateRepos": features.private_repos,
                    "multiRepoQuerying": features.multi_repo_querying,
                    "unlimitedChat": features.unlimited_chat,
                    "integrations": features.integrations
                }
            }
        except Exception as e:
            logger.error(f"Error fetching subscription: {e}")
            # Return a fallback free plan in case of errors
            return {
                "tier": "free",
                "status": "active",
                "currentPeriodEnd": datetime.now().astimezone() + timedelta(days=30),
                "features": UserFeatures.get_free_tier().dict()
            }

    def _ensure_datetime(self, value: Any) -> datetime:
        """Convert various datetime formats to timezone-aware datetime."""
        if value is None:
            return datetime.now(timezone.utc)
            
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value)
            except ValueError:
                dt = datetime.now(timezone.utc)
        elif isinstance(value, dict) and "$date" in value:
            ts = value["$date"]
            if isinstance(ts, (int, float)):
                dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
            else:
                dt = datetime.now(timezone.utc)
        else:
            dt = datetime.now(timezone.utc)
            
        # Ensure timezone awareness
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        return dt 

# Simple function to get a user's subscription tier
def get_subscription_tier(user_id: str) -> str:
    """Get a user's subscription tier (pro or free)."""
    try:
        db_instance = MongoDB()
        user_doc = db_instance.users.find_one({"id": user_id})
        if not user_doc:
            return "free"
            
        return user_doc.get("subscription_tier", "free")
    except Exception as e:
        logging.error(f"Failed to get subscription tier: {e}")
        return "free" 