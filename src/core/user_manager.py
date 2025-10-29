"""
User Management System with Subscriptions, Memories, and Limits
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from src.core.redis_manager import get_redis_manager

logger = logging.getLogger(__name__)


class UserManager:
    """Manage users, subscriptions, memories, and usage limits"""
    
    TIERS = {
        "free": {
            "messages_per_day": 10,
            "images_per_month": 1,
            "videos_per_month": 0,
            "audio_per_month": 5,
            "nsfw_enabled": False,
            "memory_slots": 10,
            "proactive_messages": False
        },
        "basic": {
            "price": 299,
            "messages_per_day": 999999,
            "images_per_month": 50,
            "videos_per_month": 5,
            "audio_per_month": 100,
            "nsfw_enabled": False,
            "memory_slots": 50,
            "proactive_messages": True
        },
        "prime": {
            "price": 899,
            "messages_per_day": 999999,
            "images_per_month": 500,
            "videos_per_month": 50,
            "audio_per_month": 500,
            "nsfw_enabled": True,
            "memory_slots": 200,
            "proactive_messages": True
        },
        "lifetime": {
            "price": 2999,
            "messages_per_day": 999999,
            "images_per_month": 999999,
            "videos_per_month": 999999,
            "audio_per_month": 999999,
            "nsfw_enabled": True,
            "memory_slots": 999999,
            "proactive_messages": True
        }
    }
    
    def __init__(self):
        self.redis = get_redis_manager()
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user data"""
        key = f"user:{user_id}"
        data = self.redis.get(key)
        
        if not data:
            # Create new user
            data = {
                "user_id": user_id,
                "tier": "free",
                "created_at": datetime.now().isoformat(),
                "subscription_expires": None,
                "usage": {
                    "messages_today": 0,
                    "images_this_month": 0,
                    "videos_this_month": 0,
                    "audio_this_month": 0,
                    "last_reset": datetime.now().isoformat()
                },
                "memories": [],
                "story": None,
                "preferences": {
                    "roleplay_style": "friendly",
                    "nsfw_consent": False
                }
            }
            self.redis.set(key, data, expire=None)
        
        return data
    
    def update_user(self, user_id: int, data: Dict[str, Any]):
        """Update user data"""
        key = f"user:{user_id}"
        self.redis.set(key, data, expire=None)
    
    def upgrade_subscription(self, user_id: int, tier: str, duration_days: int = 30):
        """Upgrade user subscription"""
        user = self.get_user(user_id)
        user["tier"] = tier
        
        if tier == "lifetime":
            user["subscription_expires"] = "lifetime"
        else:
            expires = datetime.now() + timedelta(days=duration_days)
            user["subscription_expires"] = expires.isoformat()
        
        self.update_user(user_id, user)
        logger.info(f"✅ User {user_id} upgraded to {tier}")
    
    def check_limit(self, user_id: int, action: str) -> tuple[bool, str]:
        """Check if user can perform action"""
        user = self.get_user(user_id)
        tier = user["tier"]
        limits = self.TIERS[tier]
        usage = user["usage"]
        
        # Reset daily/monthly counters if needed
        last_reset = datetime.fromisoformat(usage["last_reset"])
        now = datetime.now()
        
        if now.date() > last_reset.date():
            usage["messages_today"] = 0
        
        if now.month != last_reset.month:
            usage["images_this_month"] = 0
            usage["videos_this_month"] = 0
            usage["audio_this_month"] = 0
        
        usage["last_reset"] = now.isoformat()
        
        # Check limits
        if action == "message":
            if usage["messages_today"] >= limits["messages_per_day"]:
                return False, f"Daily limit reached ({limits['messages_per_day']} messages). Upgrade to continue!"
            usage["messages_today"] += 1
        
        elif action == "image":
            if usage["images_this_month"] >= limits["images_per_month"]:
                return False, f"Monthly limit reached ({limits['images_per_month']} images). Upgrade for more!"
            usage["images_this_month"] += 1
        
        elif action == "video":
            if usage["videos_this_month"] >= limits["videos_per_month"]:
                return False, f"Monthly limit reached ({limits['videos_per_month']} videos). Upgrade for more!"
            usage["videos_this_month"] += 1
        
        elif action == "audio":
            if usage["audio_this_month"] >= limits["audio_per_month"]:
                return False, f"Monthly limit reached ({limits['audio_per_month']} audio). Upgrade for more!"
            usage["audio_this_month"] += 1
        
        elif action == "nsfw":
            if not limits["nsfw_enabled"]:
                return False, "NSFW content requires Prime or Lifetime subscription!"
        
        user["usage"] = usage
        self.update_user(user_id, user)
        return True, "OK"
    
    def add_memory(self, user_id: int, memory: str, category: str = "general"):
        """Add memory for user"""
        user = self.get_user(user_id)
        tier = user["tier"]
        max_memories = self.TIERS[tier]["memory_slots"]
        
        memory_entry = {
            "text": memory,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        
        user["memories"].append(memory_entry)
        
        # Keep only recent memories within limit
        if len(user["memories"]) > max_memories:
            user["memories"] = user["memories"][-max_memories:]
        
        self.update_user(user_id, user)
    
    def get_memories(self, user_id: int, limit: int = 10) -> list:
        """Get user memories"""
        user = self.get_user(user_id)
        return user["memories"][-limit:]
    
    def set_story(self, user_id: int, story: Dict[str, Any]):
        """Set user's story for roleplay"""
        user = self.get_user(user_id)
        user["story"] = story
        self.update_user(user_id, user)
    
    def get_story(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's story"""
        user = self.get_user(user_id)
        return user.get("story")
    
    def get_tier_info(self, tier: str) -> Dict[str, Any]:
        """Get tier information"""
        return self.TIERS.get(tier, self.TIERS["free"])


# Global instance
_user_manager = None


def get_user_manager() -> UserManager:
    """Get global user manager instance"""
    global _user_manager
    if _user_manager is None:
        _user_manager = UserManager()
    return _user_manager
