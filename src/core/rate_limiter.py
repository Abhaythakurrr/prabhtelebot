"""
Advanced Rate Limiting System
Token Bucket Algorithm with Per-User, Per-Model Tracking
"""

import time
import logging
from typing import Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket for rate limiting"""
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def refill(self):
        """Refill tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens
        Returns True if successful, False if rate limited
        """
        self.refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def get_wait_time(self, tokens: int = 1) -> float:
        """Get time to wait until tokens available"""
        self.refill()
        if self.tokens >= tokens:
            return 0.0
        tokens_needed = tokens - self.tokens
        return tokens_needed / self.refill_rate


class RateLimiter:
    """
    Advanced rate limiter with per-user, per-model tracking
    """
    
    # Rate limits per model type (requests per minute)
    MODEL_LIMITS = {
        # Image generation
        "text-to-image": 10,
        "image-analysis": 20,
        
        # Video generation
        "text-to-video": 5,
        "video-analysis": 10,
        
        # Audio generation
        "text-to-speech": 10,
        "text-to-audio": 10,
        "audio-analysis": 15,
        
        # Text models
        "text-generation": 30,
        "text-classification": 40,
        "text-embedding": 50,
        "translation": 20,
        "summarization": 15,
        "question-answering": 25,
        
        # Visual QA
        "visual-qa": 15,
        "document-qa": 15,
    }
    
    # Tier multipliers
    TIER_MULTIPLIERS = {
        "free": 1.0,
        "basic": 2.0,
        "pro": 3.0,
        "prime": 5.0,
        "super": 10.0,
        "lifetime": float('inf')  # Unlimited
    }
    
    def __init__(self):
        # user_id -> model_type -> TokenBucket
        self.buckets: Dict[str, Dict[str, TokenBucket]] = defaultdict(dict)
        
        # Track usage statistics
        self.usage_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        # Track rate limit hits
        self.rate_limit_hits: Dict[str, int] = defaultdict(int)
    
    def check_limit(
        self,
        user_id: str,
        model_type: str,
        user_tier: str = "free",
        tokens: int = 1
    ) -> tuple[bool, Optional[float]]:
        """
        Check if user can make request
        
        Returns:
            (allowed: bool, wait_time: Optional[float])
        """
        # Lifetime tier has no limits
        if user_tier == "lifetime":
            self._track_usage(user_id, model_type)
            return True, None
        
        # Get base limit for model type
        base_limit = self.MODEL_LIMITS.get(model_type, 10)
        
        # Apply tier multiplier
        multiplier = self.TIER_MULTIPLIERS.get(user_tier, 1.0)
        effective_limit = int(base_limit * multiplier)
        
        # Get or create bucket for this user/model
        if model_type not in self.buckets[user_id]:
            # Convert per-minute to per-second rate
            refill_rate = effective_limit / 60.0
            self.buckets[user_id][model_type] = TokenBucket(
                capacity=effective_limit,
                refill_rate=refill_rate
            )
        
        bucket = self.buckets[user_id][model_type]
        
        # Try to consume tokens
        if bucket.consume(tokens):
            self._track_usage(user_id, model_type)
            logger.info(f"✅ Rate limit OK: {user_id} - {model_type} ({user_tier})")
            return True, None
        else:
            # Rate limited
            wait_time = bucket.get_wait_time(tokens)
            self.rate_limit_hits[user_id] += 1
            logger.warning(
                f"⚠️ Rate limited: {user_id} - {model_type} "
                f"(wait {wait_time:.1f}s, tier: {user_tier})"
            )
            return False, wait_time
    
    def _track_usage(self, user_id: str, model_type: str):
        """Track usage statistics"""
        self.usage_stats[user_id][model_type] += 1
        self.usage_stats[user_id]["total"] += 1
    
    def get_usage_stats(self, user_id: str) -> Dict[str, int]:
        """Get usage statistics for user"""
        return dict(self.usage_stats[user_id])
    
    def get_remaining_quota(
        self,
        user_id: str,
        model_type: str,
        user_tier: str = "free"
    ) -> int:
        """Get remaining quota for user/model"""
        if user_tier == "lifetime":
            return float('inf')
        
        if model_type not in self.buckets[user_id]:
            base_limit = self.MODEL_LIMITS.get(model_type, 10)
            multiplier = self.TIER_MULTIPLIERS.get(user_tier, 1.0)
            return int(base_limit * multiplier)
        
        bucket = self.buckets[user_id][model_type]
        bucket.refill()
        return int(bucket.tokens)
    
    def reset_user_limits(self, user_id: str):
        """Reset all limits for a user"""
        if user_id in self.buckets:
            del self.buckets[user_id]
        logger.info(f"🔄 Reset rate limits for user: {user_id}")
    
    def get_rate_limit_message(
        self,
        model_type: str,
        wait_time: float,
        user_tier: str
    ) -> str:
        """Get user-friendly rate limit message"""
        minutes = int(wait_time / 60)
        seconds = int(wait_time % 60)
        
        if minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"
        
        messages = {
            "free": f"⏳ Rate limit reached! Please wait {time_str} or upgrade to Premium for higher limits.",
            "basic": f"⏳ Rate limit reached! Please wait {time_str}. Upgrade to Pro for 3x higher limits!",
            "pro": f"⏳ Rate limit reached! Please wait {time_str}. Upgrade to Prime for 5x higher limits!",
            "prime": f"⏳ Rate limit reached! Please wait {time_str}. Upgrade to Super for 10x higher limits!",
            "super": f"⏳ Rate limit reached! Please wait {time_str}."
        }
        
        return messages.get(user_tier, messages["free"])


# Global rate limiter instance
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
