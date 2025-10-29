"""
Razorpay Payment Integration
"""

import logging
import razorpay
from typing import Dict, Any
from datetime import datetime, timedelta
from src.core.config import get_config

logger = logging.getLogger(__name__)


class PaymentHandler:
    """Handle Razorpay payments"""
    
    def __init__(self):
        self.config = get_config()
        
        if self.config.razorpay_key_id and self.config.razorpay_key_secret:
            self.client = razorpay.Client(auth=(
                self.config.razorpay_key_id,
                self.config.razorpay_key_secret
            ))
            logger.info("✅ Razorpay initialized")
        else:
            self.client = None
            logger.warning("⚠️ Razorpay not configured")
    
    def create_order(self, user_id: str, plan_id: str, amount: int) -> Dict[str, Any]:
        """Create payment order"""
        try:
            if not self.client:
                return {"success": False, "error": "Payment not configured"}
            
            order_data = {
                "amount": amount * 100,
                "currency": "INR",
                "receipt": f"sub_{user_id}_{plan_id}_{int(datetime.now().timestamp())}",
                "notes": {
                    "user_id": user_id,
                    "plan_id": plan_id
                }
            }
            
            order = self.client.order.create(data=order_data)
            
            return {
                "success": True,
                "order_id": order["id"],
                "amount": amount,
                "key_id": self.config.razorpay_key_id
            }
            
        except Exception as e:
            logger.error(f"❌ Order creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_payment(self, payment_id: str, order_id: str, signature: str) -> Dict[str, Any]:
        """Verify payment signature"""
        try:
            if not self.client:
                return {"success": False, "error": "Payment not configured"}
            
            params = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }
            
            self.client.utility.verify_payment_signature(params)
            
            return {
                "success": True,
                "payment_id": payment_id,
                "verified": True
            }
            
        except Exception as e:
            logger.error(f"❌ Payment verification failed: {e}")
            return {"success": False, "error": str(e)}


# Global instance
_payment_handler = None


def get_payment_handler() -> PaymentHandler:
    """Get global payment handler"""
    global _payment_handler
    if _payment_handler is None:
        _payment_handler = PaymentHandler()
    return _payment_handler
