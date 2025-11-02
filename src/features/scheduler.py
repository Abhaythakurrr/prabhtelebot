"""
Scheduled Messages & Reminders - Send messages at specific times
"""

import logging
from datetime import datetime, time
from typing import Dict, List
from src.core.user_manager import get_user_manager
from src.story.advanced_processor import get_advanced_processor

logger = logging.getLogger(__name__)


class MessageScheduler:
    """Schedule messages for specific times"""
    
    def __init__(self):
        self.user_manager = get_user_manager()
        self.processor = get_advanced_processor()
        self.schedules = {}  # user_id: [schedule_items]
    
    def add_schedule(self, user_id: int, schedule_type: str, time_of_day: time, message: str = None):
        """Add a scheduled message"""
        if user_id not in self.schedules:
            self.schedules[user_id] = []
        
        schedule_item = {
            "type": schedule_type,
            "time": time_of_day,
            "message": message,
            "enabled": True
        }
        
        self.schedules[user_id].append(schedule_item)
        logger.info(f"Added schedule for user {user_id}: {schedule_type} at {time_of_day}")
    
    def get_schedules(self, user_id: int) -> List[Dict]:
        """Get all schedules for user"""
        return self.schedules.get(user_id, [])
    
    def should_send_now(self, user_id: int) -> List[Dict]:
        """Check if any messages should be sent now"""
        now = datetime.now().time()
        schedules = self.get_schedules(user_id)
        
        to_send = []
        for schedule in schedules:
            if schedule["enabled"]:
                schedule_time = schedule["time"]
                # Check if within 1 minute window
                if abs((now.hour * 60 + now.minute) - (schedule_time.hour * 60 + schedule_time.minute)) <= 1:
                    to_send.append(schedule)
        
        return to_send
    
    def generate_scheduled_message(self, user_id: int, schedule_type: str) -> str:
        """Generate message based on schedule type"""
        user = self.user_manager.get_user(user_id)
        persona = user.get('persona')
        
        if not persona:
            return "Good morning! Have a wonderful day! 💕"
        
        messages = {
            "morning": f"Good morning! I hope you slept well. Ready for a beautiful day? 💕",
            "afternoon": f"Hey! How's your day going? Just checking in on you. 💕",
            "evening": f"Good evening! How was your day? I'd love to hear about it. 💕",
            "night": f"Good night! Sweet dreams. I'll be here when you wake up. 💕",
            "custom": schedule.get("message", "Thinking of you... 💕")
        }
        
        return messages.get(schedule_type, self.processor.generate_proactive_message(persona))


# Global instance
_scheduler = None


def get_scheduler():
    """Get global scheduler"""
    global _scheduler
    if _scheduler is None:
        _scheduler = MessageScheduler()
    return _scheduler
