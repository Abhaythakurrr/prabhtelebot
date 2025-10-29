"""
Redis Manager - Real-time communication and caching
"""

import logging
import redis
import json
from typing import Any, Optional
from src.core.config import get_config

logger = logging.getLogger(__name__)


class RedisManager:
    """Manage Redis connections and operations"""
    
    def __init__(self):
        self.config = get_config()
        self.client = None
        self.pubsub = None
        
        if self.config.redis_url:
            try:
                self.client = redis.from_url(self.config.redis_url)
                self.client.ping()
                logger.info("✅ Redis connected")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed: {e}")
                self.client = None
    
    def set(self, key: str, value: Any, expire: int = None):
        """Set value in Redis"""
        if not self.client:
            return False
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            self.client.set(key, value)
            
            if expire:
                self.client.expire(key, expire)
            
            return True
        except Exception as e:
            logger.error(f"❌ Redis set failed: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.client:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                try:
                    return json.loads(value)
                except:
                    return value.decode('utf-8')
            return None
        except Exception as e:
            logger.error(f"❌ Redis get failed: {e}")
            return None
    
    def publish(self, channel: str, message: Any):
        """Publish message to channel"""
        if not self.client:
            return False
        
        try:
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            
            self.client.publish(channel, message)
            return True
        except Exception as e:
            logger.error(f"❌ Redis publish failed: {e}")
            return False
    
    def subscribe(self, channel: str):
        """Subscribe to channel"""
        if not self.client:
            return None
        
        try:
            if not self.pubsub:
                self.pubsub = self.client.pubsub()
            
            self.pubsub.subscribe(channel)
            return self.pubsub
        except Exception as e:
            logger.error(f"❌ Redis subscribe failed: {e}")
            return None


# Global instance
_redis_manager = None


def get_redis_manager() -> RedisManager:
    """Get global Redis manager"""
    global _redis_manager
    if _redis_manager is None:
        _redis_manager = RedisManager()
    return _redis_manager
