from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

import api_store
from subscription_store import SubscriptionStore, STRIPE_PRODUCTS
from modelsdb.user import User, SubscriptionTier, SubscriptionStatus
import stripe
import os
import logging

router = APIRouter(prefix="/api/billing", tags=["billing"])
subscription_store = SubscriptionStore()
logger = logging.getLogger(__name__)

class CheckoutSessionRequest(BaseModel):
    user_id: str
    price_id: str
    user_email: str
    user_name: Optional[str] = None
    promotion_code: Optional[str] = None

class CheckoutSessionResponse(BaseModel):
    url: str

class PortalSessionRequest(BaseModel):
    user_id: str
    user_email: Optional[str] = None
    user_name: Optional[str] = None

class PortalSessionResponse(BaseModel):
    url: str

class SubscriptionFeatures(BaseModel):
    maxRepoSize: int = Field(alias="max_repo_size")
    privateRepos: bool = Field(alias="private_repos")
    multiRepoQuerying: bool = Field(alias="multi_repo_querying")
    unlimitedChat: bool = Field(alias="unlimited_chat")
    integrations: list[str]

    class Config:
        populate_by_name = True

class SubscriptionResponse(BaseModel):
    tier: SubscriptionTier
    status: str
    current_period_end: str = Field(alias="currentPeriodEnd")
    features: SubscriptionFeatures

    class Config:
        populate_by_name = True

class AddPaymentMethodRequest(BaseModel):
    user_id: str
    return_url: str

class AddPaymentMethodResponse(BaseModel):
    url: str

class BillingPeriod(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None

class ApiUsageDetailsResponse(BaseModel):
    has_payment_method: bool = Field(description="Whether the user has a payment method on file")
    api_keys_count: int = Field(description="Number of API keys the user has")
    total_requests: int = Field(description="Total number of API requests made this month")
    upcoming_charges: float = Field(description="Upcoming charges in dollars")
    current_usage: int = Field(description="Current usage count")
    billing_period: BillingPeriod = Field(description="Start and end dates of the current billing period")

    class Config:
        schema_extra = {
            "example": {
                "has_payment_method": True,
                "api_keys_count": 3,
                "total_requests": 150,
                "upcoming_charges": 15.0,
                "current_usage": 150,
                "billing_period": {
                    "start": "2023-06-01T00:00:00Z",
                    "end": "2023-06-30T23:59:59Z"
                }
            }
        }

@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(request: CheckoutSessionRequest):
    """Create a checkout session for Stripe."""
    try:
        # Get user from database
        user_doc = subscription_store.db.users.find_one({"id": request.user_id})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Convert to User model
        if "_id" in user_doc:
            del user_doc["_id"]
            
        # Add email from the request to ensure User model validation passes
        user_doc["email"] = request.user_email
        
        user = User(**user_doc)
        
        # Check if customer exists and is valid in Stripe
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        customer_valid = False
        
        if user.stripe_customer_id:
            try:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
                if not getattr(customer, 'deleted', False):
                    customer_valid = True
                else:
                    logger.info(f"Found deleted customer {user.stripe_customer_id}, will recreate")
            except stripe.error.InvalidRequestError as e:
                if 'No such customer' in str(e):
                    logger.info(f"Customer {user.stripe_customer_id} not found, will recreate")
                else:
                    raise
        
        # If customer is deleted or invalid, create a new one
        if not customer_valid:
            try:
                # Create new customer
                customer = stripe.Customer.create(
                    email=request.user_email,
                    name=request.user_name,
                    metadata={
                        "user_id": request.user_id
                    }
                )
                
                # Update user record with new customer ID
                user.stripe_customer_id = customer.id
                subscription_store.db.users.update_one(
                    {"id": user.id},
                    {"$set": {"stripe_customer_id": customer.id}}
                )
                
                logger.info(f"Created new customer {customer.id} for user {user.id}")
            except stripe.error.StripeError as e:
                logger.error(f"Error creating new customer: {e}")
                raise HTTPException(status_code=400, detail=str(e))
        
        # Generate idempotency key
        idempotency_key = f"checkout_{request.user_id}_{request.price_id}_{int(datetime.now().timestamp())}"
        
        # Create checkout session
        result = await subscription_store.create_checkout_session(
            user=user,
            price_id=request.price_id,
            idempotency_key=idempotency_key,
            promotion_code=request.promotion_code
        )
        
        return CheckoutSessionResponse(url=result["url"])
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating checkout session: {e}")
        raise HTTPException(
            status_code=400,
            detail={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )

@router.post("/create-portal-session", response_model=PortalSessionResponse)
async def create_portal_session(request: PortalSessionRequest):
    """Create a portal session for managing billing."""
    try:
        # Get user from database
        user_doc = subscription_store.db.users.find_one({"id": request.user_id})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Convert to User model
        if "_id" in user_doc:
            del user_doc["_id"]
        
        # Add email from request if available
        if request.user_email:
            user_doc["email"] = request.user_email
            
        user = User(**user_doc)
        
        if not user.stripe_customer_id:
            raise HTTPException(status_code=400, detail="No Stripe customer found")
            
        # Check if the customer is valid in Stripe
        try:
            stripe.api_key = os.getenv("STRIPE_API_KEY")
            customer = stripe.Customer.retrieve(user.stripe_customer_id)
            if getattr(customer, 'deleted', False):
                logger.warning(f"Customer {user.stripe_customer_id} is deleted in Stripe")
                raise HTTPException(status_code=400, detail="Customer record is invalid. Please contact support.")
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving customer {user.stripe_customer_id}: {e}")
            raise HTTPException(status_code=400, detail="Error accessing customer record. Please try again later.")
        
        # Generate an idempotency key to prevent duplicate portal sessions
        idempotency_key = f"portal_{request.user_id}_{int(datetime.now().timestamp())}"
            
        result = await subscription_store.create_portal_session(user, idempotency_key=idempotency_key)
        return PortalSessionResponse(url=result["url"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating portal session: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    try:
        body = await request.body()
        sig_header = request.headers.get("stripe-signature")
        
        if not sig_header:
            logger.error("Missing stripe-signature header")
            raise HTTPException(status_code=400, detail={"error": "Missing stripe-signature header"})
            
        try:
            event = stripe.Webhook.construct_event(
                body,
                sig_header,
                os.getenv("STRIPE_WEBHOOK_SECRET")
            )
            logger.info(f"Received Stripe webhook event: {event.type}")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {e}")
            raise HTTPException(status_code=400, detail={"error": "Invalid webhook signature"})
        except Exception as e:
            logger.error(f"Error constructing webhook event: {e}")
            raise HTTPException(status_code=400, detail={"error": "Invalid webhook payload"})

        # Handle the event
        event_handlers = {
            "customer.subscription.created": subscription_store.handle_subscription_updated,
            "customer.subscription.updated": subscription_store.handle_subscription_updated,
            "customer.subscription.deleted": subscription_store.handle_subscription_deleted,
            "customer.subscription.trial_will_end": subscription_store.handle_subscription_updated,
            "invoice.payment_succeeded": subscription_store.handle_invoice_payment_succeeded,
            "invoice.payment_failed": subscription_store.handle_invoice_payment_failed,
            "payment_intent.succeeded": subscription_store.handle_payment_intent_succeeded,
            "payment_intent.failed": subscription_store.handle_payment_intent_failed,
        }

        handler = event_handlers.get(event.type)
        if handler:
            logger.info(f"Processing event {event.type} with handler")
            await handler(event.data.object)
            logger.info(f"Successfully processed {event.type} webhook")
        else:
            logger.info(f"No handler for webhook type: {event.type}")
            
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to process webhook"}
        )

@router.get("/subscription/{user_id}", response_model=SubscriptionResponse)
async def get_subscription(user_id: str):
    """Get current subscription details."""
    try:
        subscription = await subscription_store.get_subscription(user_id)
        
        # Convert the response to match the expected format
        return SubscriptionResponse(
            tier=subscription["tier"],
            status=subscription["status"],
            currentPeriodEnd=subscription["currentPeriodEnd"].isoformat() if isinstance(subscription["currentPeriodEnd"], datetime) else subscription["currentPeriodEnd"],
            features=SubscriptionFeatures(
                maxRepoSize=subscription["features"]["maxRepoSize"],
                privateRepos=subscription["features"]["privateRepos"],
                multiRepoQuerying=subscription["features"]["multiRepoQuerying"],
                unlimitedChat=subscription["features"]["unlimitedChat"],
                integrations=subscription["features"]["integrations"]
            )
        )
    except Exception as e:
        logger.error(f"Error in get_subscription route: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )

@router.post("/cancel")
async def cancel_subscription(user: User):
    """Cancel current subscription."""
    try:
        await subscription_store.cancel_subscription(user)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api-usage")
async def get_api_usage(user_id: str):
    """Get API usage statistics for a user."""
    now = datetime.now().astimezone()
    try:
        # Get all API keys for the user
        api_keys = list(subscription_store.db.api_keys.find({"user_id": user_id}))
        
        if not api_keys:
            return {
                "apiKeysCount": 0,
                "totalRequestsThisMonth": 0,
                "totalTokensThisMonth": 0,
                "billingRate": 0.1,
                "estimatedCost": 0,
                "limit": 10000
            }
        
        # Calculate total usage from our database
        total_requests = sum(key.get("usage", {}).get("monthly_requests", 0) for key in api_keys)
        total_tokens = sum(key.get("usage", {}).get("monthly_tokens", 0) for key in api_keys)
        
        # Get user's subscription tier to determine limits
        user = subscription_store.db.users.find_one({"id": user_id})
        tier = user.get("subscription_tier", "free") if user else "free"
        stripe_customer_id = user.get("stripe_customer_id") if user else None
        
        # Set limits based on tier
        request_limit = 100000 if tier == "pro" else 10000
        
        # Get average billing rate (in case there are different rates)
        billing_rates = [key.get("billing_rate", 0.1) for key in api_keys]
        avg_billing_rate = sum(billing_rates) / len(billing_rates) if billing_rates else 0.1
        
        # Try to get recent usage data from Stripe for more accurate billing
        stripe_requests = 0
        if stripe_customer_id:
            try:
                # Configure Stripe API
                stripe.api_key = os.getenv("STRIPE_API_KEY")
                
                # Log that we're skipping Stripe meter events due to API issues
    
                
                # Just use the database counts instead
                stripe_requests = 0
                    
            except Exception as e:
                logger.error(f"Error with Stripe API: {str(e)}")
                # Continue with database counts if Stripe API fails
        
        # Calculate estimated cost
        estimated_cost = total_requests * avg_billing_rate
        
        # Simplified response with only the essential information
        return {
            "apiKeysCount": len(api_keys),
            "totalRequestsThisMonth": total_requests,
            "billingRate": avg_billing_rate,
            "estimatedCost": estimated_cost,
            "limit": request_limit
        }
    except Exception as e:
        logger.error(f"Error fetching API usage: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )

async def has_payment_method_internal(stripe_customer_id: str) -> bool:
    """
    Check if a Stripe customer has a payment method added.
    
    Args:
        stripe_customer_id: The Stripe customer ID to check
        
    Returns:
        bool: True if the customer has a payment method, False otherwise
    """
    try:
        # Configure Stripe
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        
        # List payment methods for customer
        payment_methods = stripe.PaymentMethod.list(
            customer=stripe_customer_id,
            type="card"
        )
        
        # Check if customer has any payment methods
        if hasattr(payment_methods, 'data'):
            return len(payment_methods.data) > 0
        else:
            # Handle case where payment_methods might be an iterable directly
            return len(list(payment_methods)) > 0
            
    except Exception as e:
        logger.error(f"Error checking payment method for customer {stripe_customer_id}: {e}")
        return False

@router.get("/has-payment-method")
async def has_payment_method(user_id: str):
    """Check if a user has a payment method added."""
    try:
        user_doc = subscription_store.safe_get_user({"id": user_id})
        if not user_doc:
            return {"hasPaymentMethod": False}
            
        stripe_customer_id = user_doc.get("stripe_customer_id")
        if not stripe_customer_id:
            return {"hasPaymentMethod": False}
            
        has_method = await has_payment_method_internal(stripe_customer_id)
        return {"hasPaymentMethod": has_method}
    except Exception as e:
        logger.error(f"Error checking payment method: {e}")
        return {"hasPaymentMethod": False}

@router.post("/add-payment-method", response_model=AddPaymentMethodResponse)
async def add_payment_method(request: AddPaymentMethodRequest):
    """Create a Stripe setup session for adding a payment method."""
    try:
        # Get user from database
        user_doc = subscription_store.db.users.find_one({"id": request.user_id})
        
        # Create user if not exists
        if not user_doc:
            logger.info(f"User not found, creating new user with id: {request.user_id}")
            user_doc = {
                "id": request.user_id,
                "created_at": datetime.now().astimezone(),
                "updated_at": datetime.now().astimezone(),
                "subscription_tier": SubscriptionTier.FREE,
                "subscription_status": SubscriptionStatus.ACTIVE
            }
            subscription_store.db.users.insert_one(user_doc)
        
        # Get or create Stripe customer
        stripe_customer_id = user_doc.get("stripe_customer_id")
        if not stripe_customer_id:
            # Create new Stripe customer
            customer = stripe.Customer.create(
                metadata={"user_id": request.user_id}
            )
            stripe_customer_id = customer.id
            
            # Update user with Stripe customer ID
            subscription_store.db.users.update_one(
                {"id": request.user_id},
                {
                    "$set": {
                        "stripe_customer_id": stripe_customer_id,
                        "updated_at": datetime.now().astimezone()
                    }
                }
            )
            logger.info(f"Created new Stripe customer: {stripe_customer_id}")
        
        # Create a setup session
        setup_session = stripe.checkout.Session.create(
            customer=stripe_customer_id,
            payment_method_types=["card"],
            mode="setup",
            success_url=f"{request.return_url}?setup=success",
            cancel_url=f"{request.return_url}?setup=canceled",
        )
        
        return AddPaymentMethodResponse(url=setup_session.url)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in add_payment_method: {e}")
        raise HTTPException(
            status_code=400,
            detail={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Error in add_payment_method: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )

@router.get("/api-usage-details", response_model=ApiUsageDetailsResponse)
async def get_api_usage_details(user_id: str):
    """
    Get detailed usage information including upcoming charges for API usage.
    
    Args:
        user_id: The ID of the user to get API usage details for
        
    Returns:
        ApiUsageDetailsResponse: Detailed API usage information
        
    Raises:
        HTTPException: If user is not found or an error occurs
    """
    try:
        logger.info(f"Getting API usage details for user {user_id}")
        
        # Get user from database using safe method
        user_doc = subscription_store.safe_get_user({"id": user_id})
        if not user_doc:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
            
        # Get stripe customer ID directly instead of using User model
        stripe_customer_id = user_doc.get("stripe_customer_id")
        logger.info(f"Stripe customer ID for user {user_id}: {stripe_customer_id}")
        
        if not stripe_customer_id:
            logger.info(f"No Stripe customer ID for user {user_id}, returning zeros")
            return ApiUsageDetailsResponse(
                has_payment_method=False,
                api_keys_count=0,
                total_requests=0,
                upcoming_charges=0,
                current_usage=0,
                billing_period=BillingPeriod(start=None, end=None)
            )
        
        # Configure Stripe
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        
        # Get API keys for user
        api_keys = api_store.get_user_api_keys(user_id)
        logger.info(f"Found {len(api_keys)} API keys for user {user_id}")
        
        # Calculate total requests
        total_requests = sum(key.get("usage", {}).get("monthly_requests", 0) for key in api_keys)
        logger.info(f"Total API requests for user {user_id}: {total_requests}")
        
        # Get upcoming invoice to check metered usage
        try:
            logger.info(f"Retrieving upcoming invoice for customer {stripe_customer_id}")
            upcoming_invoice = stripe.Invoice.upcoming(customer=stripe_customer_id)
            
            # Get metered line items
            metered_usage_amount = 0
            current_usage = 0
            billing_period = BillingPeriod(start=None, end=None)
            
            for line in upcoming_invoice.get("lines", {}).get("data", []):
                if line.get("price", {}).get("recurring", {}).get("usage_type") == "metered":
                    # Convert cents to dollars
                    line_amount = line.get("amount", 0) / 100
                    metered_usage_amount += line_amount
                    
                    # Get usage quantity
                    line_quantity = line.get("quantity", 0)
                    current_usage += line_quantity
                    
                    logger.info(f"Found metered line item: amount=${line_amount}, quantity={line_quantity}")
                    
                    # Get billing period
                    period = line.get("period", {})
                    if period:
                        start = datetime.fromtimestamp(period.get("start", 0))
                        end = datetime.fromtimestamp(period.get("end", 0))
                        billing_period = BillingPeriod(
                            start=start.isoformat(),
                            end=end.isoformat()
                        )
                        logger.info(f"Billing period: {start.isoformat()} to {end.isoformat()}")
        except stripe.error.StripeError as e:
            logger.warning(f"Could not retrieve upcoming invoice: {e}")
            metered_usage_amount = 0
            current_usage = total_requests
            billing_period = BillingPeriod(start=None, end=None)
            
        # Get payment method status
        logger.info(f"Checking payment method for customer {stripe_customer_id}")
        has_payment_method = await has_payment_method_internal(stripe_customer_id)
        logger.info(f"Customer {stripe_customer_id} has payment method: {has_payment_method}")
            
        response = ApiUsageDetailsResponse(
            has_payment_method=has_payment_method,
            api_keys_count=len(api_keys),
            total_requests=total_requests,
            upcoming_charges=metered_usage_amount,
            current_usage=current_usage,
            billing_period=billing_period
        )
        logger.info(f"API usage details response for user {user_id}: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error getting API usage details: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        ) 