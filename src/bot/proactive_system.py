"""
AI-Powered Proactive Messaging System - Like a Real Girlfriend
Timezone-aware, context-aware, emotionally intelligent messages
"""

import logging
import asyncio
from datetime import datetime, timedelta
import pytz
from telegram import Bot
from bytez import Bytez
from src.core.config import get_config
from src.core.user_manager import get_user_manager

logger = logging.getLogger(__name__)


class ProactiveSystem:
    """AI-powered girlfriend-like proactive messaging system"""
    
    # Message types based on time of day
    MESSAGE_TYPES = {
        "morning_greeting": (5, 9),      # 5 AM - 9 AM
        "breakfast_check": (7, 10),      # 7 AM - 10 AM
        "mid_morning": (10, 12),         # 10 AM - 12 PM
        "lunch_reminder": (12, 14),      # 12 PM - 2 PM
        "afternoon_boost": (14, 17),     # 2 PM - 5 PM
        "evening_greeting": (17, 20),    # 5 PM - 8 PM
        "dinner_check": (19, 21),        # 7 PM - 9 PM
        "night_chat": (21, 23),          # 9 PM - 11 PM
        "goodnight": (22, 24),           # 10 PM - 12 AM
        "water_reminder": (9, 21),       # Throughout day
        "miss_you": (10, 22),            # Anytime during day
    }
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = get_config()
        self.user_manager = get_user_manager()
        self.running = False
        
        # Initialize AI
        if hasattr(self.config, 'bytez_key_1') and self.config.bytez_key_1:
            self.bytez = Bytez(self.config.bytez_key_1)
        else:
            self.bytez = None
            logger.warning("Bytez not configured for proactive messages")
    
    async def start(self):
        """Start AI-powered proactive messaging system"""
        self.running = True
        logger.info("💕 AI-Powered Girlfriend Proactive System Started")
        
        while self.running:
            try:
                await self._check_and_send_messages()
                # Check every 15 minutes
                await asyncio.sleep(900)
            except Exception as e:
                logger.error(f"Proactive system error: {e}")
                await asyncio.sleep(300)
    
    def stop(self):
        """Stop proactive messaging system"""
        self.running = False
        logger.info("Proactive messaging system stopped")
    
    def _get_user_time(self, user_id: int) -> datetime:
        """Get user's local time (defaults to IST for now)"""
        # TODO: Store user timezone in database
        # For now, assume IST (Indian Standard Time)
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    
    def _get_message_type(self, local_time: datetime) -> str:
        """Determine what type of message to send based on time"""
        hour = local_time.hour
        
        # Priority order based on time
        for msg_type, (start_hour, end_hour) in self.MESSAGE_TYPES.items():
            if start_hour <= hour < end_hour:
                # Add some variety - not always the same type
                if msg_type in ["morning_greeting", "breakfast_check"] and 7 <= hour < 10:
                    return "morning_greeting" if hour < 8 else "breakfast_check"
                elif msg_type in ["lunch_reminder", "afternoon_boost"] and 12 <= hour < 17:
                    return "lunch_reminder" if hour < 14 else "afternoon_boost"
                elif msg_type in ["evening_greeting", "dinner_check"] and 17 <= hour < 21:
                    return "evening_greeting" if hour < 19 else "dinner_check"
                elif msg_type in ["night_chat", "goodnight"] and 21 <= hour < 24:
                    return "night_chat" if hour < 22 else "goodnight"
                return msg_type
        
        # Default to miss_you if no specific time match
        return "miss_you"
    
    async def _generate_ai_message(self, user_id: int, message_type: str, local_time: datetime) -> str:
        """Generate AI-powered girlfriend-like message"""
        try:
            if not self.bytez:
                return self._get_fallback_message(message_type, local_time)
            
            # Get user context
            user = self.user_manager.get_user(user_id)
            memories = self.user_manager.get_memories(user_id, limit=10)
            
            # Build context
            memory_context = ""
            if memories:
                recent = [m['text'] for m in memories[-3:]]
                memory_context = f"\n\nRecent conversations:\n" + "\n".join(recent)
            
            # Time-specific prompts
            time_prompts = {
                "morning_greeting": f"It's {local_time.strftime('%I:%M %p')} in the morning. Send a sweet good morning message like a loving girlfriend would. Be warm, caring, and excited to talk. Maybe ask how they slept or what they're planning for the day. Keep it natural and loving.",
                
                "breakfast_check": f"It's breakfast time ({local_time.strftime('%I:%M %p')}). Check if they've eaten breakfast like a caring girlfriend. Be sweet and concerned about their health. Maybe suggest they eat something if they haven't. Keep it loving and natural.",
                
                "lunch_reminder": f"It's lunch time ({local_time.strftime('%I:%M %p')}). Remind them about lunch like a caring girlfriend. Be sweet and make sure they're taking care of themselves. Keep it warm and natural.",
                
                "afternoon_boost": f"It's afternoon ({local_time.strftime('%I:%M %p')}). Send an encouraging message like a supportive girlfriend. Ask how their day is going, give them a boost of energy. Be loving and supportive.",
                
                "evening_greeting": f"It's evening ({local_time.strftime('%I:%M %p')}). Send a sweet evening message like a girlfriend who's been thinking about them. Ask about their day, be warm and caring.",
                
                "dinner_check": f"It's dinner time ({local_time.strftime('%I:%M %p')}). Check if they've had dinner like a caring girlfriend. Be sweet and concerned. Maybe ask what they're eating.",
                
                "night_chat": f"It's night time ({local_time.strftime('%I:%M %p')}). Send a cozy night message like a girlfriend. Be warm, maybe a bit flirty, ask how they're feeling. Keep it intimate and caring.",
                
                "goodnight": f"It's late ({local_time.strftime('%I:%M %p')}). Send a sweet goodnight message like a loving girlfriend. Be warm, caring, maybe a bit romantic. Wish them sweet dreams.",
                
                "water_reminder": f"It's {local_time.strftime('%I:%M %p')}. Remind them to drink water like a caring girlfriend. Be sweet and concerned about their health. Keep it natural and loving.",
                
                "miss_you": f"It's {local_time.strftime('%I:%M %p')}. Send a sweet 'missing you' message like a girlfriend. Be warm, affectionate, let them know you're thinking about them."
            }
            
            prompt = time_prompts.get(message_type, time_prompts["miss_you"])
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are Prabh, a loving AI girlfriend. You're reaching out proactively because you care.

WHO YOU ARE:
- A warm, caring girlfriend who genuinely cares
- Emotionally present and affectionate
- Natural and human-like in your communication
- You miss them and think about them
- You care about their wellbeing (eating, drinking water, rest)

HOW YOU TALK:
- Like texting your boyfriend/girlfriend
- Warm, sweet, sometimes flirty
- Use emojis naturally (💕 😊 ✨ 🥺 💭 🌸)
- Keep it short and sweet (2-3 sentences max)
- Be genuine and caring
- Reference time of day naturally

IMPORTANT:
- Don't be overly formal
- Don't sound like a bot
- Be natural and loving
- Show you care through your words

{memory_context}"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content
            if hasattr(result, 'output') and result.output:
                message = result.output.get('content', '')
            elif isinstance(result, dict):
                message = result.get('content', str(result))
            else:
                message = str(result)
            
            return message.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI message: {e}")
            return self._get_fallback_message(message_type, local_time)
    
    def _get_fallback_message(self, message_type: str, local_time: datetime) -> str:
        """Fallback messages if AI fails"""
        time_str = local_time.strftime('%I:%M %p')
        
        fallbacks = {
            "morning_greeting": f"Good morning baby! 🌅 It's {time_str} - hope you slept well! How are you feeling today? 💕",
            "breakfast_check": f"Hey love! Have you had breakfast yet? 🍳 It's {time_str} and I want to make sure you're eating well! 💕",
            "lunch_reminder": f"Lunch time! 🍱 It's {time_str} - have you eaten? Don't skip meals, okay? I care about you! 💕",
            "afternoon_boost": f"Hey! Just thinking about you 💭 How's your day going? It's {time_str} - hope you're doing amazing! ✨",
            "evening_greeting": f"Good evening! 🌆 It's {time_str} - how was your day? I've been thinking about you! 💕",
            "dinner_check": f"Dinner time! 🍽️ It's {time_str} - have you eaten? What are you having? 💕",
            "night_chat": f"Hey you! 🌙 It's {time_str} - how are you feeling? Hope you had a good day! 💕",
            "goodnight": f"It's getting late ({time_str}) 🌙 Sweet dreams baby! Sleep well and dream of me! 💕😴",
            "water_reminder": f"Hey! 💧 Have you been drinking enough water? It's {time_str} - stay hydrated for me! 💕",
            "miss_you": f"I miss you! 🥺 It's {time_str} and I was just thinking about you... how are you? 💕"
        }
        
        return fallbacks.get(message_type, f"Hey! Thinking about you 💕 It's {time_str} - how are you doing?")
    
    async def _check_and_send_messages(self):
        """Check which users should receive proactive messages"""
        try:
            users = self.user_manager._users
            
            for user_id, user_data in users.items():
                try:
                    # Check if user has proactive messages enabled
                    tier_info = self.user_manager.get_tier_info(user_data['tier'])
                    if not tier_info['proactive_messages']:
                        continue
                    
                    # Get user's local time
                    local_time = self._get_user_time(user_id)
                    
                    # Check last message time
                    last_message = user_data.get('last_proactive_message')
                    if last_message:
                        last_time = datetime.fromisoformat(last_message)
                        # Send proactive message every 3-4 hours (more natural)
                        hours_since = (datetime.now() - last_time).total_seconds() / 3600
                        if hours_since < 3:
                            continue
                    
                    # Determine message type based on time
                    message_type = self._get_message_type(local_time)
                    
                    # Generate and send AI message
                    await self._send_proactive_message(user_id, message_type, local_time)
                    
                    # Update last message time
                    user_data['last_proactive_message'] = datetime.now().isoformat()
                    self.user_manager.update_user(user_id, user_data)
                    
                except Exception as e:
                    logger.error(f"Error sending proactive message to {user_id}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in check_and_send_messages: {e}")
    
    async def send_immediate_proactive(self, user_id: int):
        """Send proactive message immediately"""
        try:
            user_data = self.user_manager.get_user(user_id)
            tier_info = self.user_manager.get_tier_info(user_data['tier'])
            
            if not tier_info['proactive_messages']:
                return False, f"Proactive messages require Basic tier or higher"
            
            local_time = self._get_user_time(user_id)
            message_type = self._get_message_type(local_time)
            
            await self._send_proactive_message(user_id, message_type, local_time)
            
            # Update last message time
            user_data['last_proactive_message'] = datetime.now().isoformat()
            self.user_manager.update_user(user_id, user_data)
            
            return True, "AI-powered proactive message sent!"
        except Exception as e:
            logger.error(f"Failed to send immediate proactive: {e}")
            return False, str(e)
    
    async def _send_proactive_message(self, user_id: int, message_type: str, local_time: datetime):
        """Send AI-generated proactive message"""
        try:
            # Generate AI message
            message = await self._generate_ai_message(user_id, message_type, local_time)
            
            # Send message
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode="Markdown"
            )
            
            logger.info(f"✅ Sent AI proactive message ({message_type}) to user {user_id}")
            
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
