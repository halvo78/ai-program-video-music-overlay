"""
Stripe Integration for SaaS

Complete payment system:
- Subscription management
- Usage-based billing
- Customer portal
- Webhooks
- Invoice management
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PricingTier:
    """Pricing tier configuration."""
    id: str
    name: str
    price_monthly: int  # cents
    price_yearly: int  # cents
    features: List[str]
    limits: Dict[str, int]
    stripe_price_id_monthly: Optional[str] = None
    stripe_price_id_yearly: Optional[str] = None
    is_popular: bool = False


# Pricing tiers based on competitive analysis
PRICING_TIERS = [
    PricingTier(
        id="free",
        name="Free",
        price_monthly=0,
        price_yearly=0,
        features=[
            "5 videos per month",
            "720p export quality",
            "Basic AI features",
            "Taj Chat watermark",
            "1 social platform",
        ],
        limits={
            "videos_per_month": 5,
            "export_quality": 720,
            "ai_credits": 50,
            "social_platforms": 1,
            "storage_gb": 1,
        },
    ),
    PricingTier(
        id="creator",
        name="Creator",
        price_monthly=1900,  # $19/month
        price_yearly=15900,  # $159/year ($13.25/month)
        features=[
            "30 videos per month",
            "1080p export quality",
            "All AI features",
            "No watermark",
            "3 social platforms",
            "Virality Score",
            "URL to Video",
            "Basic analytics",
        ],
        limits={
            "videos_per_month": 30,
            "export_quality": 1080,
            "ai_credits": 500,
            "social_platforms": 3,
            "storage_gb": 10,
        },
        is_popular=True,
    ),
    PricingTier(
        id="professional",
        name="Professional",
        price_monthly=4900,  # $49/month
        price_yearly=39900,  # $399/year ($33.25/month)
        features=[
            "100 videos per month",
            "4K export quality",
            "All AI features",
            "No watermark",
            "All social platforms",
            "Virality Score",
            "URL to Video",
            "AI B-Roll",
            "Brand Kit",
            "Advanced analytics",
            "Priority support",
        ],
        limits={
            "videos_per_month": 100,
            "export_quality": 2160,
            "ai_credits": 2000,
            "social_platforms": 6,
            "storage_gb": 50,
        },
    ),
    PricingTier(
        id="enterprise",
        name="Enterprise",
        price_monthly=19900,  # $199/month
        price_yearly=159900,  # $1599/year ($133.25/month)
        features=[
            "Unlimited videos",
            "4K export quality",
            "All AI features",
            "White-label option",
            "All social platforms",
            "All advanced features",
            "AI Avatars",
            "Video Translation",
            "Custom integrations",
            "Dedicated support",
            "SLA guarantee",
        ],
        limits={
            "videos_per_month": -1,  # Unlimited
            "export_quality": 2160,
            "ai_credits": -1,  # Unlimited
            "social_platforms": 6,
            "storage_gb": 500,
        },
    ),
]


class StripeIntegration:
    """
    Stripe payment integration for Taj Chat SaaS.
    
    Features:
    - Subscription management
    - Usage-based billing
    - Customer portal
    - Webhooks
    """

    def __init__(self):
        self.secret_key = os.getenv("STRIPE_SECRET_KEY", "")
        self.publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
        
        self.stripe = None
        if self.secret_key:
            try:
                import stripe
                stripe.api_key = self.secret_key
                self.stripe = stripe
                logger.info("Stripe initialized successfully")
            except ImportError:
                logger.warning("Stripe library not installed")

    def get_pricing_tiers(self) -> List[Dict]:
        """Get all pricing tiers."""
        return [
            {
                "id": tier.id,
                "name": tier.name,
                "price_monthly": tier.price_monthly / 100,  # Convert to dollars
                "price_yearly": tier.price_yearly / 100,
                "price_monthly_cents": tier.price_monthly,
                "price_yearly_cents": tier.price_yearly,
                "features": tier.features,
                "limits": tier.limits,
                "is_popular": tier.is_popular,
            }
            for tier in PRICING_TIERS
        ]

    async def create_checkout_session(
        self,
        tier_id: str,
        billing_period: str = "monthly",  # monthly or yearly
        customer_email: Optional[str] = None,
        success_url: str = "http://localhost:3000/success",
        cancel_url: str = "http://localhost:3000/pricing",
    ) -> Dict:
        """Create Stripe checkout session."""
        
        if not self.stripe:
            return {"error": "Stripe not configured"}
        
        # Find tier
        tier = next((t for t in PRICING_TIERS if t.id == tier_id), None)
        if not tier:
            return {"error": f"Invalid tier: {tier_id}"}
        
        if tier.price_monthly == 0:
            return {"error": "Free tier doesn't require payment"}
        
        # Get price ID
        price_id = (
            tier.stripe_price_id_yearly if billing_period == "yearly"
            else tier.stripe_price_id_monthly
        )
        
        # If no Stripe price ID, create one dynamically
        if not price_id:
            price_amount = tier.price_yearly if billing_period == "yearly" else tier.price_monthly
            interval = "year" if billing_period == "yearly" else "month"
            
            try:
                # Create product if not exists
                product = self.stripe.Product.create(
                    name=f"Taj Chat - {tier.name}",
                    description=f"Taj Chat {tier.name} subscription",
                )
                
                # Create price
                price = self.stripe.Price.create(
                    product=product.id,
                    unit_amount=price_amount,
                    currency="usd",
                    recurring={"interval": interval},
                )
                
                price_id = price.id
                
            except Exception as e:
                logger.error(f"Failed to create Stripe price: {e}")
                return {"error": str(e)}
        
        try:
            session_params = {
                "mode": "subscription",
                "line_items": [{"price": price_id, "quantity": 1}],
                "success_url": success_url + "?session_id={CHECKOUT_SESSION_ID}",
                "cancel_url": cancel_url,
                "metadata": {
                    "tier_id": tier_id,
                    "billing_period": billing_period,
                },
            }
            
            if customer_email:
                session_params["customer_email"] = customer_email
            
            session = self.stripe.checkout.Session.create(**session_params)
            
            return {
                "session_id": session.id,
                "url": session.url,
            }
            
        except Exception as e:
            logger.error(f"Failed to create checkout session: {e}")
            return {"error": str(e)}

    async def create_customer_portal_session(
        self,
        customer_id: str,
        return_url: str = "http://localhost:3000/settings",
    ) -> Dict:
        """Create Stripe customer portal session for subscription management."""
        
        if not self.stripe:
            return {"error": "Stripe not configured"}
        
        try:
            session = self.stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            return {
                "url": session.url,
            }
            
        except Exception as e:
            logger.error(f"Failed to create portal session: {e}")
            return {"error": str(e)}

    async def get_subscription(self, subscription_id: str) -> Dict:
        """Get subscription details."""
        
        if not self.stripe:
            return {"error": "Stripe not configured"}
        
        try:
            subscription = self.stripe.Subscription.retrieve(subscription_id)
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "plan": {
                    "id": subscription.plan.id,
                    "amount": subscription.plan.amount,
                    "interval": subscription.plan.interval,
                },
            }
            
        except Exception as e:
            logger.error(f"Failed to get subscription: {e}")
            return {"error": str(e)}

    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True,
    ) -> Dict:
        """Cancel subscription."""
        
        if not self.stripe:
            return {"error": "Stripe not configured"}
        
        try:
            if at_period_end:
                subscription = self.stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True,
                )
            else:
                subscription = self.stripe.Subscription.delete(subscription_id)
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end,
            }
            
        except Exception as e:
            logger.error(f"Failed to cancel subscription: {e}")
            return {"error": str(e)}

    async def handle_webhook(self, payload: bytes, signature: str) -> Dict:
        """Handle Stripe webhook events."""
        
        if not self.stripe:
            return {"error": "Stripe not configured"}
        
        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            
            # Handle different event types
            if event.type == "checkout.session.completed":
                return await self._handle_checkout_completed(event.data.object)
            elif event.type == "customer.subscription.updated":
                return await self._handle_subscription_updated(event.data.object)
            elif event.type == "customer.subscription.deleted":
                return await self._handle_subscription_deleted(event.data.object)
            elif event.type == "invoice.payment_succeeded":
                return await self._handle_payment_succeeded(event.data.object)
            elif event.type == "invoice.payment_failed":
                return await self._handle_payment_failed(event.data.object)
            
            return {"status": "unhandled", "event_type": event.type}
            
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return {"error": str(e)}

    async def _handle_checkout_completed(self, session) -> Dict:
        """Handle successful checkout."""
        
        logger.info(f"Checkout completed: {session.id}")
        
        # Extract metadata
        tier_id = session.metadata.get("tier_id")
        customer_id = session.customer
        subscription_id = session.subscription
        
        # Here you would:
        # 1. Update user's subscription in database
        # 2. Provision access to features
        # 3. Send welcome email
        
        return {
            "status": "success",
            "event": "checkout_completed",
            "tier_id": tier_id,
            "customer_id": customer_id,
            "subscription_id": subscription_id,
        }

    async def _handle_subscription_updated(self, subscription) -> Dict:
        """Handle subscription update."""
        
        logger.info(f"Subscription updated: {subscription.id}")
        
        return {
            "status": "success",
            "event": "subscription_updated",
            "subscription_id": subscription.id,
            "new_status": subscription.status,
        }

    async def _handle_subscription_deleted(self, subscription) -> Dict:
        """Handle subscription cancellation."""
        
        logger.info(f"Subscription deleted: {subscription.id}")
        
        # Here you would:
        # 1. Downgrade user to free tier
        # 2. Send cancellation email
        
        return {
            "status": "success",
            "event": "subscription_deleted",
            "subscription_id": subscription.id,
        }

    async def _handle_payment_succeeded(self, invoice) -> Dict:
        """Handle successful payment."""
        
        logger.info(f"Payment succeeded: {invoice.id}")
        
        return {
            "status": "success",
            "event": "payment_succeeded",
            "invoice_id": invoice.id,
            "amount": invoice.amount_paid,
        }

    async def _handle_payment_failed(self, invoice) -> Dict:
        """Handle failed payment."""
        
        logger.warning(f"Payment failed: {invoice.id}")
        
        # Here you would:
        # 1. Notify user of failed payment
        # 2. Retry payment
        # 3. Eventually downgrade if payment continues to fail
        
        return {
            "status": "warning",
            "event": "payment_failed",
            "invoice_id": invoice.id,
        }

    async def record_usage(
        self,
        subscription_item_id: str,
        quantity: int,
        action: str = "increment",
    ) -> Dict:
        """Record usage for metered billing."""
        
        if not self.stripe:
            return {"error": "Stripe not configured"}
        
        try:
            usage_record = self.stripe.SubscriptionItem.create_usage_record(
                subscription_item_id,
                quantity=quantity,
                action=action,
                timestamp=int(datetime.now().timestamp()),
            )
            
            return {
                "id": usage_record.id,
                "quantity": usage_record.quantity,
            }
            
        except Exception as e:
            logger.error(f"Failed to record usage: {e}")
            return {"error": str(e)}


# Singleton instance
stripe_integration = StripeIntegration()

