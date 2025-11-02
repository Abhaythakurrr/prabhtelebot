"""
Proactive Messaging System - AI reaches out to users with love
"""

import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.story.advanced_processor import get_advanced_processor

logger = logging.getLogger(__name__)


class ProactiveSystem:
    """System for AI to proactively reach out to users"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = get_config()
        self.user_manager = get_user_manager()
        self.processor = get_advanced_processor()
        self.running = False
    
    async def start(self):
        """Start proactive messaging system"""
        self.running = True
        logger.info("💕 Proactive messaging system started")
        
        while self.running:
            try:
                await self._check_and_send_messages()
                # Check every 30 minutes
                await asyncio.sleep(1800)
            except Exception as e:
                logger.error(f"Proactive system error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    def stop(self):
        """Stop proactive messaging system"""
        self.running = False
        logger.info("Proactive messaging system stopped")
    
    async def _check_and_send_messages(self):
        """Check which users should receive proactive messages"""
        try:
            # Get all users (in production, this would be from database)
            users = self.user_manager._users
            
            for user_id, user_data in users.items():
                try:
                    # Check if user has proactive messages enabled
                    tier_info = self.user_manager.get_tier_info(user_data['tier'])
                    if not tier_info['proactive_messages']:
                        continue
                    
                    # Check if user has a persona
                    persona = user_data.get('persona')
                    if not persona:
                        continue
                    
                    # Check last message time
                    last_message = user_data.get('last_proactive_message')
                    if last_message:
                        last_time = datetime.fromisoformat(last_message)
                        # Send proactive message every 6 hours
                        if datetime.now() - last_time < timedelta(hours=6):
                            continue
                    
                    # Generate and send proactive message
                    await self._send_proactive_message(user_id, persona)
                    
                    # Update last message time
                    user_data['last_proactive_message'] = datetime.now().isoformat()
                    self.user_manager.update_user(user_id, user_data)
                    
                except Exception as e:
                    logger.error(f"Error sending proactive message to {user_id}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in check_and_send_messages: {e}")
    
    async def _send_proactive_message(self, user_id: int, persona: dict):
        """Send a proactive message to user"""
        try:
            # Generate message from persona
            message = self.processor.generate_proactive_message(persona)
            
            # Send message
            await self.bot.send_message(
                chat_id=user_id,
                text=f"💕 {message}",
                parse_mode="Markdown"
            )
            
            logger.info(f"✅ Sent proactive message to user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to send proactive message to {user_id}: {e}")


# Global instance
_proactive_system = None


def get_proactive_system(bot: Bot = None):
    """Get global proactive system instance"""
    global _proactive_system
    if _proactive_system is None and bot:
        _proactive_system = ProactiveSystem(bot)
    return _proactive_system
