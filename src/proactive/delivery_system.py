"""
Message scheduling and delivery system for proactive messaging.
Handles background task scheduling, delivery tracking, and user preferences.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta, time
from enum import Enum
import json
from dataclasses import dataclass, asdict
import pytz

from src.core.interfaces import DatabaseInterface
from src.premium.access_control import FeatureAccessControl, FeatureType
from src.proactive.message_scheduler import MessageScheduler
from src.proactive.message_personalizer import MessagePersonalizer
from src.proactive.nostalgic_messaging import NostalgicMessaging


class MessageStatus(Enum):
    """Message delivery status."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MessageType(Enum):
    """Types of proactive messages."""
    MORNING_GREETING = "morning_greeting"
    EVENING_CHECKIN = "evening_checkin"
    GOODNIGHT = "goodnight"
    NOSTALGIC = "nostalgic"
    ANNIVERSARY = "anniversary"
    EMOTIONAL_CHECKIN = "emotional_checkin"
    CUSTOM_REMINDER = "custom_reminder"


@dataclass
class ScheduledMessage:
    """Represents a scheduled message."""
    id: Optional[str]
    user_id: str
    message_type: MessageType
    content: str
    scheduled_time: datetime
    status: MessageStatus
    created_at: datetime
    delivered_at: Optional[datetime] = None
    failed_reason: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['message_type'] = self.message_type.value
        data['status'] = self.status.value
        data['scheduled_time'] = self.scheduled_time.isoformat()
        data['created_at'] = self.created_at.isoformat()
        if self.delivered_at:
            data['delivered_at'] = self.delivered_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScheduledMessage':
        """Create from dictionary."""
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            message_type=MessageType(data['message_type']),
            content=data['content'],
            scheduled_time=datetime.fromisoformat(data['scheduled_time']),
            status=MessageStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            delivered_at=datetime.fromisoformat(data['delivered_at']) if data.get('delivered_at') else None,
            failed_reason=data.get('failed_reason'),
            retry_count=data.get('retry_count', 0),
            max_retries=data.get('max_retries', 3),
            metadata=data.get('metadata', {})
        )


@dataclass
class UserPreferences:
    """User preferences for proactive messaging."""
    user_id: str
    enabled: bool = True
    timezone: str = "UTC"
    morning_time: time = time(9, 0)  # 9:00 AM
    evening_time: time = time(18, 0)  # 6:00 PM
    goodnight_time: time = time(22, 0)  # 10:00 PM
    frequency: str = "daily"  # daily, weekly, custom
    message_types: List[MessageType] = None
    quiet_hours_start: time = time(23, 0)  # 11:00 PM
    quiet_hours_end: time = time(7, 0)  # 7:00 AM
    max_daily_messages: int = 3
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.message_types is None:
            self.message_types = [
                MessageType.MORNING_GREETING,
                MessageType.EVENING_CHECKIN,
                MessageType.GOODNIGHT,
                MessageType.NOSTALGIC
            ]
        if self.last_updated is None:
            self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'enabled': self.enabled,
            'timezone': self.timezone,
            'morning_time': self.morning_time.isoformat(),
            'evening_time': self.evening_time.isoformat(),
            'goodnight_time': self.goodnight_time.isoformat(),
            'frequency': self.frequency,
            'message_types': [mt.value for mt in self.message_types],
            'quiet_hours_start': self.quiet_hours_start.isoformat(),
            'quiet_hours_end': self.quiet_hours_end.isoformat(),
            'max_daily_messages': self.max_daily_messages,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create from dictionary."""
        return cls(
            user_id=data['user_id'],
            enabled=data.get('enabled', True),
            timezone=data.get('timezone', 'UTC'),
            morning_time=time.fromisoformat(data.get('morning_time', '09:00:00')),
            evening_time=time.fromisoformat(data.get('evening_time', '18:00:00')),
            goodnight_time=time.fromisoformat(data.get('goodnight_time', '22:00:00')),
            frequency=data.get('frequency', 'daily'),
            message_types=[MessageType(mt) for mt in data.get('message_types', [])],
            quiet_hours_start=time.fromisoformat(data.get('quiet_hours_start', '23:00:00')),
            quiet_hours_end=time.fromisoformat(data.get('quiet_hours_end', '07:00:00')),
            max_daily_messages=data.get('max_daily_messages', 3),
            last_updated=datetime.fromisoformat(data['last_updated'])
        )


class ProactiveMessageDeliverySystem:
    """Main system for scheduling and delivering proactive messages."""
    
    def __init__(self, database: DatabaseInterface, 
                 access_control: FeatureAccessControl,
                 message_scheduler: MessageScheduler,
                 message_personalizer: MessagePersonalizer,
                 nostalgic_messaging: NostalgicMessaging,
                 telegram_bot_handler):
        self.database = database
        self.access_control = access_control
        self.message_scheduler = message_scheduler
        self.message_personalizer = message_personalizer
        self.nostalgic_messaging = nostalgic_messaging
        self.telegram_bot_handler = telegram_bot_handler
        self.logger = logging.getLogger(__name__)
        
        # Background task management
        self.scheduler_task = None
        self.delivery_task = None
        self.is_running = False
        
        # Message delivery callbacks
        self.delivery_callbacks: List[Callable] = []
        
        # Statistics
        self.delivery_stats = {
            "total_scheduled": 0,
            "total_delivered": 0,
            "total_failed": 0,
            "delivery_rate": 0.0
        }
        
        self.logger.info("Proactive Message Delivery System initialized")
    
    async def start(self) -> None:
        """Start the background scheduling and delivery tasks."""
        if self.is_running:
            self.logger.warning("Delivery system is already running")
            return
        
        self.is_running = True
        
        # Start background tasks
        self.scheduler_task = asyncio.create_task(self._scheduler_loop())
        self.delivery_task = asyncio.create_task(self._delivery_loop())
        
        self.logger.info("Proactive message delivery system started")
    
    async def stop(self) -> None:
        """Stop the background tasks."""
        self.is_running = False
        
        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass
        
        if self.delivery_task:
            self.delivery_task.cancel()
            try:
                await self.delivery_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Proactive message delivery system stopped")
    
    async def schedule_message(self, user_id: str, message_type: MessageType, 
                             scheduled_time: datetime, content: str = None,
                             metadata: Dict[str, Any] = None) -> ScheduledMessage:
        """Schedule a proactive message for delivery."""
        try:
            # Check if user has proactive messaging access
            await self.access_control.enforce_feature_access(user_id, FeatureType.PROACTIVE_MESSAGING)
            
            # Get user preferences
            preferences = await self.get_user_preferences(user_id)
            
            if not preferences.enabled:
                raise Exception("Proactive messaging is disabled for this user")
            
            if message_type not in preferences.message_types:
                raise Exception(f"Message type {message_type.value} is not enabled for this user")
            
            # Check daily message limit
            daily_count = await self._get_daily_message_count(user_id)
            if daily_count >= preferences.max_daily_messages:
                raise Exception("Daily message limit exceeded")
            
            # Adjust scheduled time for user's timezone and quiet hours
            adjusted_time = await self._adjust_scheduled_time(scheduled_time, preferences)
            
            # Generate content if not provided
            if not content:
                content = await self._generate_message_content(user_id, message_type, metadata)
            
            # Create scheduled message
            message = ScheduledMessage(
                id=None,  # Will be set by database
                user_id=user_id,
                message_type=message_type,
                content=content,
                scheduled_time=adjusted_time,
                status=MessageStatus.SCHEDULED,
                created_at=datetime.now(),
                metadata=metadata or {}
            )
            
            # Store in database
            message_id = await self.database.store_scheduled_message(message.to_dict())
            message.id = message_id
            
            self.delivery_stats["total_scheduled"] += 1
            
            self.logger.info(f"Scheduled {message_type.value} message for user {user_id} at {adjusted_time}")
            return message
            
        except Exception as e:
            self.logger.error(f"Error scheduling message: {e}")
            raise
    
    async def cancel_message(self, message_id: str) -> bool:
        """Cancel a scheduled message."""
        try:
            message_data = await self.database.get_scheduled_message(message_id)
            if not message_data:
                return False
            
            message = ScheduledMessage.from_dict(message_data)
            
            if message.status in [MessageStatus.DELIVERED, MessageStatus.CANCELLED]:
                return False
            
            message.status = MessageStatus.CANCELLED
            await self.database.update_scheduled_message(message_id, message.to_dict())
            
            self.logger.info(f"Cancelled scheduled message {message_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cancelling message {message_id}: {e}")
            return False
    
    async def get_user_preferences(self, user_id: str) -> UserPreferences:
        """Get user's proactive messaging preferences."""
        try:
            prefs_data = await self.database.get_user_proactive_preferences(user_id)
            
            if prefs_data:
                return UserPreferences.from_dict(prefs_data)
            else:
                # Create default preferences
                default_prefs = UserPreferences(user_id=user_id)
                await self.update_user_preferences(default_prefs)
                return default_prefs
                
        except Exception as e:
            self.logger.error(f"Error getting user preferences: {e}")
            return UserPreferences(user_id=user_id)
    
    async def update_user_preferences(self, preferences: UserPreferences) -> None:
        """Update user's proactive messaging preferences."""
        try:
            preferences.last_updated = datetime.now()
            await self.database.store_user_proactive_preferences(preferences.to_dict())
            
            self.logger.info(f"Updated proactive messaging preferences for user {preferences.user_id}")
            
        except Exception as e:
            self.logger.error(f"Error updating user preferences: {e}")
            raise
    
    async def get_pending_messages(self, limit: int = 100) -> List[ScheduledMessage]:
        """Get pending messages ready for delivery."""
        try:
            now = datetime.now()
            messages_data = await self.database.get_pending_scheduled_messages(now, limit)
            
            return [ScheduledMessage.from_dict(data) for data in messages_data]
            
        except Exception as e:
            self.logger.error(f"Error getting pending messages: {e}")
            return []
    
    async def deliver_message(self, message: ScheduledMessage) -> bool:
        """Deliver a scheduled message."""
        try:
            self.logger.info(f"Delivering {message.message_type.value} message to user {message.user_id}")
            
            # Check if user still has access
            access_info = await self.access_control.check_feature_access(
                message.user_id, FeatureType.PROACTIVE_MESSAGING
            )
            
            if not access_info["has_access"]:
                message.status = MessageStatus.FAILED
                message.failed_reason = "User no longer has proactive messaging access"
                await self.database.update_scheduled_message(message.id, message.to_dict())
                return False
            
            # Get user preferences to check if still enabled
            preferences = await self.get_user_preferences(message.user_id)
            if not preferences.enabled:
                message.status = MessageStatus.CANCELLED
                message.failed_reason = "User disabled proactive messaging"
                await self.database.update_scheduled_message(message.id, message.to_dict())
                return False
            
            # Deliver via Telegram bot
            success = await self._send_telegram_message(message)
            
            if success:
                message.status = MessageStatus.DELIVERED
                message.delivered_at = datetime.now()
                self.delivery_stats["total_delivered"] += 1
                
                # Call delivery callbacks
                for callback in self.delivery_callbacks:
                    try:
                        await callback(message)
                    except Exception as e:
                        self.logger.error(f"Error in delivery callback: {e}")
            else:
                message.status = MessageStatus.FAILED
                message.retry_count += 1
                message.failed_reason = "Telegram delivery failed"
                self.delivery_stats["total_failed"] += 1
            
            await self.database.update_scheduled_message(message.id, message.to_dict())
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error delivering message {message.id}: {e}")
            
            message.status = MessageStatus.FAILED
            message.retry_count += 1
            message.failed_reason = str(e)
            await self.database.update_scheduled_message(message.id, message.to_dict())
            
            return False
    
    async def schedule_daily_messages(self, user_id: str) -> List[ScheduledMessage]:
        """Schedule daily messages for a user."""
        try:
            preferences = await self.get_user_preferences(user_id)
            
            if not preferences.enabled or preferences.frequency != "daily":
                return []
            
            scheduled_messages = []
            now = datetime.now()
            user_tz = pytz.timezone(preferences.timezone)
            
            # Schedule morning greeting
            if MessageType.MORNING_GREETING in preferences.message_types:
                morning_time = datetime.combine(now.date(), preferences.morning_time)
                morning_time = user_tz.localize(morning_time).astimezone(pytz.UTC)
                
                if morning_time > now:
                    message = await self.schedule_message(
                        user_id, MessageType.MORNING_GREETING, morning_time
                    )
                    scheduled_messages.append(message)
            
            # Schedule evening check-in
            if MessageType.EVENING_CHECKIN in preferences.message_types:
                evening_time = datetime.combine(now.date(), preferences.evening_time)
                evening_time = user_tz.localize(evening_time).astimezone(pytz.UTC)
                
                if evening_time > now:
                    message = await self.schedule_message(
                        user_id, MessageType.EVENING_CHECKIN, evening_time
                    )
                    scheduled_messages.append(message)
            
            # Schedule goodnight message
            if MessageType.GOODNIGHT in preferences.message_types:
                goodnight_time = datetime.combine(now.date(), preferences.goodnight_time)
                goodnight_time = user_tz.localize(goodnight_time).astimezone(pytz.UTC)
                
                if goodnight_time > now:
                    message = await self.schedule_message(
                        user_id, MessageType.GOODNIGHT, goodnight_time
                    )
                    scheduled_messages.append(message)
            
            return scheduled_messages
            
        except Exception as e:
            self.logger.error(f"Error scheduling daily messages for user {user_id}: {e}")
            return []
    
    async def add_delivery_callback(self, callback: Callable) -> None:
        """Add a callback to be called when messages are delivered."""
        self.delivery_callbacks.append(callback)
    
    async def _scheduler_loop(self) -> None:
        """Background loop for scheduling messages."""
        while self.is_running:
            try:
                # Get all users with proactive messaging enabled
                users = await self.database.get_users_with_proactive_messaging()
                
                for user_id in users:
                    try:
                        # Check if user needs daily messages scheduled
                        needs_scheduling = await self._user_needs_daily_scheduling(user_id)
                        
                        if needs_scheduling:
                            await self.schedule_daily_messages(user_id)
                        
                        # Schedule nostalgic messages randomly
                        if await self._should_schedule_nostalgic_message(user_id):
                            await self._schedule_nostalgic_message(user_id)
                        
                    except Exception as e:
                        self.logger.error(f"Error scheduling messages for user {user_id}: {e}")
                
                # Sleep for 1 hour before next scheduling cycle
                await asyncio.sleep(3600)
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(300)  # Sleep 5 minutes on error
    
    async def _delivery_loop(self) -> None:
        """Background loop for delivering scheduled messages."""
        while self.is_running:
            try:
                # Get pending messages
                pending_messages = await self.get_pending_messages(50)
                
                for message in pending_messages:
                    try:
                        await self.deliver_message(message)
                        
                        # Small delay between deliveries
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        self.logger.error(f"Error delivering message {message.id}: {e}")
                
                # Sleep for 1 minute before next delivery cycle
                await asyncio.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Error in delivery loop: {e}")
                await asyncio.sleep(60)
    
    async def _adjust_scheduled_time(self, scheduled_time: datetime, 
                                   preferences: UserPreferences) -> datetime:
        """Adjust scheduled time based on user preferences and quiet hours."""
        user_tz = pytz.timezone(preferences.timezone)
        
        # Convert to user's timezone
        user_time = scheduled_time.astimezone(user_tz)
        
        # Check if time falls within quiet hours
        current_time = user_time.time()
        
        if self._is_quiet_hours(current_time, preferences):
            # Move to end of quiet hours
            next_day = user_time.date()
            if current_time >= preferences.quiet_hours_start:
                next_day += timedelta(days=1)
            
            adjusted_time = datetime.combine(next_day, preferences.quiet_hours_end)
            adjusted_time = user_tz.localize(adjusted_time)
        else:
            adjusted_time = user_time
        
        # Convert back to UTC
        return adjusted_time.astimezone(pytz.UTC)
    
    def _is_quiet_hours(self, current_time: time, preferences: UserPreferences) -> bool:
        """Check if current time is within quiet hours."""
        start = preferences.quiet_hours_start
        end = preferences.quiet_hours_end
        
        if start <= end:
            # Same day quiet hours (e.g., 23:00 to 07:00 next day)
            return current_time >= start or current_time <= end
        else:
            # Quiet hours span midnight
            return start <= current_time <= end
    
    async def _generate_message_content(self, user_id: str, message_type: MessageType,
                                      metadata: Dict[str, Any] = None) -> str:
        """Generate message content based on type."""
        try:
            if message_type == MessageType.NOSTALGIC:
                return await self.nostalgic_messaging.generate_nostalgic_message(user_id)
            elif message_type == MessageType.ANNIVERSARY:
                return await self.nostalgic_messaging.generate_anniversary_message(
                    user_id, metadata.get("anniversary_date") if metadata else None
                )
            else:
                return await self.message_personalizer.generate_personalized_message(
                    user_id, message_type.value, metadata
                )
                
        except Exception as e:
            self.logger.error(f"Error generating message content: {e}")
            return self._get_fallback_message(message_type)
    
    def _get_fallback_message(self, message_type: MessageType) -> str:
        """Get fallback message content."""
        fallback_messages = {
            MessageType.MORNING_GREETING: "Good morning! Hope you have a wonderful day! 🌅",
            MessageType.EVENING_CHECKIN: "How was your day? I'd love to hear about it! 💕",
            MessageType.GOODNIGHT: "Sweet dreams! Sleep well tonight! 🌙",
            MessageType.NOSTALGIC: "I was thinking about some of our special moments together... 💭",
            MessageType.ANNIVERSARY: "Today feels special... like a day worth celebrating! 🎉",
            MessageType.EMOTIONAL_CHECKIN: "How are you feeling today? I'm here if you need to talk! 💝",
            MessageType.CUSTOM_REMINDER: "Just wanted to remind you that you're amazing! ✨"
        }
        
        return fallback_messages.get(message_type, "Thinking of you! 💕")
    
    async def _send_telegram_message(self, message: ScheduledMessage) -> bool:
        """Send message via Telegram bot."""
        try:
            if not self.telegram_bot_handler:
                self.logger.warning("No Telegram bot handler configured")
                return False
            
            # Send the message
            success = await self.telegram_bot_handler.send_proactive_message(
                message.user_id, message.content, message.message_type.value
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending Telegram message: {e}")
            return False
    
    async def _get_daily_message_count(self, user_id: str) -> int:
        """Get count of messages sent to user today."""
        try:
            today = datetime.now().date()
            return await self.database.get_daily_message_count(user_id, today)
        except Exception as e:
            self.logger.error(f"Error getting daily message count: {e}")
            return 0
    
    async def _user_needs_daily_scheduling(self, user_id: str) -> bool:
        """Check if user needs daily messages scheduled."""
        try:
            # Check if messages are already scheduled for today
            today = datetime.now().date()
            scheduled_count = await self.database.get_scheduled_message_count(user_id, today)
            
            return scheduled_count == 0
            
        except Exception as e:
            self.logger.error(f"Error checking daily scheduling needs: {e}")
            return False
    
    async def _should_schedule_nostalgic_message(self, user_id: str) -> bool:
        """Determine if a nostalgic message should be scheduled."""
        try:
            preferences = await self.get_user_preferences(user_id)
            
            if MessageType.NOSTALGIC not in preferences.message_types:
                return False
            
            # Check if nostalgic message was sent recently
            last_nostalgic = await self.database.get_last_message_time(
                user_id, MessageType.NOSTALGIC.value
            )
            
            if last_nostalgic:
                days_since = (datetime.now() - last_nostalgic).days
                return days_since >= 3  # Send nostalgic messages every 3 days
            
            return True  # First nostalgic message
            
        except Exception as e:
            self.logger.error(f"Error checking nostalgic message scheduling: {e}")
            return False
    
    async def _schedule_nostalgic_message(self, user_id: str) -> None:
        """Schedule a nostalgic message for random time today."""
        try:
            preferences = await self.get_user_preferences(user_id)
            user_tz = pytz.timezone(preferences.timezone)
            
            # Schedule for random time between 10 AM and 8 PM user time
            now = datetime.now(user_tz)
            start_hour = max(10, now.hour + 1)  # At least 1 hour from now
            end_hour = min(20, 23)  # Before 8 PM or before quiet hours
            
            if start_hour < end_hour:
                import random
                random_hour = random.randint(start_hour, end_hour)
                random_minute = random.randint(0, 59)
                
                scheduled_time = now.replace(
                    hour=random_hour, minute=random_minute, second=0, microsecond=0
                )
                
                await self.schedule_message(
                    user_id, MessageType.NOSTALGIC, scheduled_time.astimezone(pytz.UTC)
                )
                
        except Exception as e:
            self.logger.error(f"Error scheduling nostalgic message: {e}")
    
    def get_delivery_statistics(self) -> Dict[str, Any]:
        """Get delivery statistics."""
        total_messages = self.delivery_stats["total_scheduled"]
        
        if total_messages > 0:
            self.delivery_stats["delivery_rate"] = (
                self.delivery_stats["total_delivered"] / total_messages
            )
        
        return self.delivery_stats.copy()
    
    async def get_user_message_history(self, user_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """Get user's proactive message history."""
        try:
            return await self.database.get_user_proactive_message_history(user_id, days)
        except Exception as e:
            self.logger.error(f"Error getting message history: {e}")
            return []
"