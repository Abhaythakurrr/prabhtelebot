"""
Real Razorpay Payment Integration
"""

import logging
import razorpay
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from src.core.config import get_config

logger = logging.getLogger(__name__)

class RazorpayPaymentHandler:
    """Handle real Razorpay payments"""
    
    def __init__(self):
        self.config = get_config()
        
        # Initialize Razorpay client
        if self.config.razorpay.key_id and self.config.razorpay.key_secret:
            self.client = razorpay.Client(auth=(
                self.config.razorpay.key_id,
                self.config.razorpay.key_secret
            ))
            logger.info("✅ Razorpay client initialized")
        else:
            self.client = None
            logger.warning("⚠️ Razorpay credentials not configured")
    
    def create_subscription_order(self, user_id: str, plan_id: str, amount: int) -> Dict[str, Any]:
        """Create a real Razorpay order for subscription"""
        try:
            if not self.client:
                return {"success": False, "error": "Payment gateway not configured"}
            
            # Create order
            order_data = {
                "amount": amount * 100,  # Convert to paise
                "currency": "INR",
                "receipt": f"sub_{user_id}_{plan_id}_{int(datetime.now().timestamp())}",
                "notes": {
                    "user_id": user_id,
                    "plan_id": plan_id,
                    "type": "subscription"
                }
            }
            
            order = self.client.order.create(data=order_data)
            
            logger.info(f"✅ Created Razorpay order: {order['id']} for user {user_id}")
            
            return {
                "success": True,
                "order_id": order["id"],
                "amount": amount,
                "currency": "INR",
                "key_id": self.config.razorpay.key_id
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating Razorpay order: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_payment(self, payment_id: str, order_id: str, signature: str) -> Dict[str, Any]:
        """Verify Razorpay payment signature"""
        try:
            if not self.client:
                return {"success": False, "error": "Payment gateway not configured"}
            
            # Verify signature
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }
            
            self.client.utility.verify_payment_signature(params_dict)
            
            logger.info(f"✅ Payment verified: {payment_id}")
            
            return {
                "success": True,
                "payment_id": payment_id,
                "order_id": order_id,
                "verified": True
            }
            
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f"❌ Payment verification failed: {e}")
            return {"success": False, "error": "Invalid payment signature"}
        except Exception as e:
            logger.error(f"❌ Error verifying payment: {e}")
            return {"success": False, "error": str(e)}
    
    def activate_subscription(self, user_id: str, plan_id: str, payment_id: str) -> Dict[str, Any]:
        """Activate user subscription after successful payment"""
        try:
            # Calculate subscription period
            plan_durations = {
                "basic": 30,
                "pro": 30,
                "prime": 30,
                "super": 30,
                "lifetime": 36500  # 100 years
            }
            
            duration_days = plan_durations.get(plan_id, 30)
            expiry_date = datetime.now() + timedelta(days=duration_days)
            
            # Store subscription (in production, save to database)
            subscription_data = {
                "user_id": user_id,
                "plan_id": plan_id,
                "payment_id": payment_id,
                "activated_at": datetime.now().isoformat(),
                "expires_at": expiry_date.isoformat(),
                "status": "active"
            }
            
            logger.info(f"✅ Activated {plan_id} subscription for user {user_id}")
            
            return {
                "success": True,
                "subscription": subscription_data,
                "message": f"Welcome to {plan_id.upper()} plan! Your subscription is now active."
            }
            
        except Exception as e:
            logger.error(f"❌ Error activating subscription: {e}")
            return {"success": False, "error": str(e)}
    
    def check_subscription_status(self, user_id: str) -> Dict[str, Any]:
        """Check user's subscription status"""
        try:
            # In production, fetch from database
            # For now, return free tier
            return {
                "user_id": user_id,
                "plan_id": "free",
                "status": "active",
                "expires_at": None,
                "features": {
                    "messages_per_day": 10,
                    "image_generation": 1,
                    "video_generation": 0,
                    "nsfw_content": False,
                    "voice_cloning": False
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error checking subscription: {e}")
            return {"error": str(e)}
    
    def handle_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """Handle Razorpay webhook events"""
        try:
            if not self.client:
                return {"success": False, "error": "Payment gateway not configured"}
            
            # Verify webhook signature
            self.client.utility.verify_webhook_signature(
                payload,
                signature,
                self.config.razorpay.webhook_secret
            )
            
            event = payload.get("event")
            
            if event == "payment.captured":
                # Handle successful payment
                payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
                order_id = payment_entity.get("order_id")
                payment_id = payment_entity.get("id")
                
                logger.info(f"✅ Payment captured: {payment_id} for order {order_id}")
                
                return {
                    "success": True,
                    "event": "payment_captured",
                    "payment_id": payment_id,
                    "order_id": order_id
                }
            
            elif event == "payment.failed":
                # Handle failed payment
                payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
                payment_id = payment_entity.get("id")
                
                logger.warning(f"⚠️ Payment failed: {payment_id}")
                
                return {
                    "success": True,
                    "event": "payment_failed",
                    "payment_id": payment_id
                }
            
            return {"success": True, "event": event}
            
        except Exception as e:
            logger.error(f"❌ Error handling webhook: {e}")
            return {"success": False, "error": str(e)}
    
    def get_plan_details(self, plan_id: str) -> Dict[str, Any]:
        """Get plan pricing and features"""
        plans = {
            "free": {
                "name": "Free",
                "price": 0,
                "currency": "INR",
                "duration": "forever",
                "features": ["10 messages/day", "1 image/month", "Basic AI"]
            },
            "basic": {
                "name": "Basic",
                "price": 299,
                "currency": "INR",
                "duration": "monthly",
                "features": ["Unlimited messages", "50 images/month", "Voice cloning", "5 videos/month"]
            },
            "pro": {
                "name": "Pro",
                "price": 599,
                "currency": "INR",
                "duration": "monthly",
                "features": ["Unlimited messages", "200 images/month", "Voice cloning", "20 videos/month", "Better AI"]
            },
            "prime": {
                "name": "Prime",
                "price": 899,
                "currency": "INR",
                "duration": "monthly",
                "features": ["Unlimited messages", "500 images/month", "Voice cloning", "50 videos/month", "Limited NSFW", "Proactive messaging"]
            },
            "super": {
                "name": "Super",
                "price": 1299,
                "currency": "INR",
                "duration": "monthly",
                "features": ["Unlimited everything", "Full NSFW access", "Best AI models", "Priority queue", "Proactive messaging"]
            },
            "lifetime": {
                "name": "Lifetime",
                "price": 2999,
                "currency": "INR",
                "duration": "lifetime",
                "features": ["Unlimited everything forever", "Full NSFW access", "Best AI models", "Instant priority", "All future features"]
            }
        }
        
        return plans.get(plan_id, plans["free"])


# Global instance
payment_handler = RazorpayPaymentHandler()


def get_payment_handler() -> RazorpayPaymentHandler:
    """Get the global payment handler instance"""
    return payment_handler
