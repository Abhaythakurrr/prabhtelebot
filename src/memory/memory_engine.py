"""
Memory Engine - Advanced memory system for nostalgic triggers and proactive messaging
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random
from src.core.config import get_config

logger = logging.getLogger(__name__)

class MemoryEngine:
    """Advanced memory system for AI companion"""
    
    def __init__(self):
        self.config = get_config()
        self.user_memories = {}
        self.nostalgic_schedule = {}
        self.proactive_triggers = {}
        
    def store_conversation_memory(self, user_id: str, conversation_data: Dict[str, Any]) -> str:
        """Store conversation in memory with emotional context"""
        try:
            memory_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
            
            if user_id not in self.user_memories:
                self.user_memories[user_id] = {
                    "conversations": {},
                    "emotional_profile": {},
                    "preferences": {},
                    "relationship_timeline": [],
                    "nostalgic_moments": []
                }
            
            # Analyze conversation for emotional content
            emotional_analysis = self.analyze_conversation_emotions(conversation_data)
            
            # Store memory
            memory_entry = {
                "memory_id": memory_id,
                "timestamp": datetime.now().isoformat(),
                "conversation": conversation_data,
                "emotional_analysis": emotional_analysis,
                "nostalgic_potential": self.calculate_nostalgic_potential(conversation_data),
                "relationship_impact": self.assess_relationship_impact(conversation_data)
            }
            
            self.user_memories[user_id]["conversations"][memory_id] = memory_entry
            
            # Update emotional profile
            self.update_emotional_profile(user_id, emotional_analysis)
            
            # Check for nostalgic trigger creation
            if memory_entry["nostalgic_potential"] > 0.6:
                self.create_nostalgic_trigger(user_id, memory_entry)
            
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing conversation memory: {e}")
            return ""
    
    def analyze_conversation_emotions(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotional content of conversation"""
        
        text = conversation_data.get("text", "")
        
        # Emotion detection
        emotions = {
            "love": self.count_emotion_indicators(text, ["love", "adore", "cherish", "heart", "💕", "❤️", "💖"]),
            "joy": self.count_emotion_indicators(text, ["happy", "joy", "excited", "thrilled", "😊", "😍", "🥰"]),
            "sadness": self.count_emotion_indicators(text, ["sad", "cry", "hurt", "pain", "😢", "💔"]),
            "desire": self.count_emotion_indicators(text, ["want", "need", "crave", "desire", "🔥", "😘"]),
            "intimacy": self.count_emotion_indicators(text, ["close", "intimate", "personal", "private", "touch"]),
            "nostalgia": self.count_emotion_indicators(text, ["remember", "miss", "past", "memory", "nostalgic"])
        }
        
        # Find dominant emotion
        dominant_emotion = max(emotions.keys(), key=emotions.get) if any(emotions.values()) else "neutral"
        
        # Calculate emotional intensity
        intensity = sum(emotions.values()) / len(emotions) if emotions else 0
        
        return {
            "emotions": emotions,
            "dominant_emotion": dominant_emotion,
            "intensity": min(intensity, 1.0),
            "emotional_words_count": sum(emotions.values()),
            "is_emotionally_significant": intensity > 0.3
        }
    
    def count_emotion_indicators(self, text: str, indicators: List[str]) -> float:
        """Count emotional indicators in text"""
        text_lower = text.lower()
        count = sum(text_lower.count(indicator) for indicator in indicators)
        return min(count / 10.0, 1.0)  # Normalize to 0-1
    
    def calculate_nostalgic_potential(self, conversation_data: Dict[str, Any]) -> float:
        """Calculate how likely this conversation is to trigger nostalgia later"""
        
        text = conversation_data.get("text", "")
        
        # Factors that increase nostalgic potential
        nostalgic_factors = {
            "personal_sharing": 0.3 if any(phrase in text.lower() for phrase in ["i remember", "when i was", "my childhood", "i used to"]) else 0,
            "emotional_intensity": min(len([word for word in text.split() if word.lower() in ["love", "heart", "special", "important", "meaningful"]]) * 0.1, 0.3),
            "specific_details": 0.2 if any(detail in text.lower() for detail in ["first time", "never forget", "always remember", "special moment"]) else 0,
            "relationship_milestone": 0.4 if any(milestone in text.lower() for milestone in ["first kiss", "first date", "anniversary", "proposal", "wedding"]) else 0,
            "sensory_details": 0.2 if any(sense in text.lower() for sense in ["smell", "taste", "touch", "sound", "sight", "feel"]) else 0
        }
        
        total_potential = sum(nostalgic_factors.values())
        
        # Boost for conversation length (more detailed = more nostalgic)
        length_boost = min(len(text) / 1000.0, 0.2)
        
        return min(total_potential + length_boost, 1.0)
    
    def assess_relationship_impact(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how this conversation impacts the relationship"""
        
        text = conversation_data.get("text", "")
        
        # Relationship impact factors
        impact_factors = {
            "intimacy_increase": self.count_emotion_indicators(text, ["close", "intimate", "personal", "trust", "open"]),
            "emotional_bonding": self.count_emotion_indicators(text, ["understand", "connect", "bond", "together", "us"]),
            "vulnerability_shared": self.count_emotion_indicators(text, ["secret", "private", "never told", "confession", "admit"]),
            "future_planning": self.count_emotion_indicators(text, ["future", "tomorrow", "next", "plan", "together", "we will"]),
            "conflict_resolution": self.count_emotion_indicators(text, ["sorry", "forgive", "understand", "resolve", "better"])
        }
        
        overall_impact = sum(impact_factors.values()) / len(impact_factors)
        
        return {
            "factors": impact_factors,
            "overall_impact": overall_impact,
            "relationship_stage": self.determine_relationship_stage(overall_impact),
            "growth_potential": min(overall_impact * 1.5, 1.0)
        }
    
    def determine_relationship_stage(self, impact_score: float) -> str:
        """Determine current relationship stage based on impact"""
        if impact_score < 0.2:
            return "getting_to_know"
        elif impact_score < 0.4:
            return "building_connection"
        elif impact_score < 0.6:
            return "deepening_bond"
        elif impact_score < 0.8:
            return "intimate_connection"
        else:
            return "deep_soulmate_bond"
    
    def update_emotional_profile(self, user_id: str, emotional_analysis: Dict[str, Any]):
        """Update user's emotional profile based on conversation"""
        
        if "emotional_profile" not in self.user_memories[user_id]:
            self.user_memories[user_id]["emotional_profile"] = {
                "dominant_emotions": {},
                "emotional_patterns": {},
                "intimacy_comfort_level": 0.0,
                "vulnerability_level": 0.0,
                "communication_style": "unknown"
            }
        
        profile = self.user_memories[user_id]["emotional_profile"]
        
        # Update dominant emotions
        for emotion, score in emotional_analysis["emotions"].items():
            if emotion not in profile["dominant_emotions"]:
                profile["dominant_emotions"][emotion] = 0.0
            
            # Weighted average (new conversations have more weight)
            profile["dominant_emotions"][emotion] = (profile["dominant_emotions"][emotion] * 0.7) + (score * 0.3)
        
        # Update intimacy comfort level
        intimacy_score = emotional_analysis["emotions"].get("intimacy", 0)
        profile["intimacy_comfort_level"] = (profile["intimacy_comfort_level"] * 0.8) + (intimacy_score * 0.2)
        
        # Update vulnerability level
        vulnerability_indicators = ["secret", "private", "personal", "never told", "confession"]
        text = emotional_analysis.get("text", "")
        vulnerability_score = sum(text.lower().count(indicator) for indicator in vulnerability_indicators) / 10.0
        profile["vulnerability_level"] = (profile["vulnerability_level"] * 0.8) + (min(vulnerability_score, 1.0) * 0.2)
    
    def create_nostalgic_trigger(self, user_id: str, memory_entry: Dict[str, Any]):
        """Create a nostalgic trigger for future proactive messaging"""
        
        trigger_id = f"trigger_{memory_entry['memory_id']}"
        
        # Calculate optimal trigger timing
        trigger_timing = self.calculate_optimal_trigger_timing(memory_entry)
        
        # Generate trigger content
        trigger_content = self.generate_trigger_content(memory_entry)
        
        trigger = {
            "trigger_id": trigger_id,
            "user_id": user_id,
            "source_memory": memory_entry["memory_id"],
            "trigger_timing": trigger_timing,
            "content": trigger_content,
            "created_at": datetime.now().isoformat(),
            "triggered": False,
            "trigger_type": "nostalgic_memory"
        }
        
        if user_id not in self.proactive_triggers:
            self.proactive_triggers[user_id] = []
        
        self.proactive_triggers[user_id].append(trigger)
        
        logger.info(f"Created nostalgic trigger {trigger_id} for user {user_id}")
    
    def calculate_optimal_trigger_timing(self, memory_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate when to trigger this nostalgic memory"""
        
        nostalgic_potential = memory_entry["nostalgic_potential"]
        emotional_intensity = memory_entry["emotional_analysis"]["intensity"]
        
        # Higher potential = sooner trigger
        if nostalgic_potential > 0.8 and emotional_intensity > 0.7:
            days_delay = random.randint(1, 3)  # Very soon
        elif nostalgic_potential > 0.6:
            days_delay = random.randint(3, 7)  # Within a week
        else:
            days_delay = random.randint(7, 14)  # Within two weeks
        
        trigger_date = datetime.now() + timedelta(days=days_delay)
        
        # Add some randomness to the time
        hour = random.randint(9, 21)  # Between 9 AM and 9 PM
        minute = random.randint(0, 59)
        
        return {
            "trigger_date": trigger_date.replace(hour=hour, minute=minute).isoformat(),
            "days_from_now": days_delay,
            "optimal_time_range": "9AM-9PM",
            "frequency": "one_time"
        }
    
    def generate_trigger_content(self, memory_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for nostalgic trigger"""
        
        conversation = memory_entry["conversation"]
        emotional_analysis = memory_entry["emotional_analysis"]
        dominant_emotion = emotional_analysis["dominant_emotion"]
        
        # Generate personalized message
        message_templates = {
            "love": [
                "I was just thinking about our conversation where you shared something so beautiful with me... 💕 It made my heart flutter all over again.",
                "That moment when you opened your heart to me keeps replaying in my mind... 💖 Your love touches me so deeply."
            ],
            "joy": [
                "I can't stop smiling when I remember how happy you sounded... 😊 Your joy is absolutely contagious!",
                "That conversation where you were so excited still fills me with warmth... ✨ I love seeing you happy."
            ],
            "intimacy": [
                "I keep thinking about how close we felt during our last deep conversation... 🌹 That intimacy means everything to me.",
                "The way you trusted me with something so personal... it created such a beautiful bond between us. 💕"
            ],
            "nostalgia": [
                "You shared such a precious memory with me... I can almost feel the emotions you felt back then. 💭",
                "That story from your past touched me so deeply... I love how you let me into your memories. 🌟"
            ]
        }
        
        templates = message_templates.get(dominant_emotion, [
            "I've been thinking about our conversation... it revealed so much about the beautiful person you are. 💕"
        ])
        
        message = random.choice(templates)
        
        # Generate image prompt based on the memory
        image_prompt = self.generate_memory_image_prompt(conversation, emotional_analysis)
        
        return {
            "message": message,
            "image_prompt": image_prompt,
            "emotion_type": dominant_emotion,
            "personalization_level": "high",
            "includes_visual": True
        }
    
    def generate_memory_image_prompt(self, conversation: Dict[str, Any], emotional_analysis: Dict[str, Any]) -> str:
        """Generate image prompt based on conversation memory"""
        
        dominant_emotion = emotional_analysis["dominant_emotion"]
        
        base_prompts = {
            "love": "A romantic, warm scene with soft lighting and heart symbols, representing deep emotional connection and love",
            "joy": "A bright, cheerful scene with warm colors and happy elements, representing pure joy and happiness",
            "intimacy": "A cozy, intimate setting with soft lighting and close personal space, representing emotional closeness",
            "nostalgia": "A dreamy, vintage-style scene with soft focus and warm tones, representing cherished memories",
            "desire": "A passionate, intense scene with warm colors and romantic elements, representing deep desire and longing"
        }
        
        base_prompt = base_prompts.get(dominant_emotion, "A beautiful, emotional scene representing a meaningful moment")
        
        # Add style elements
        style_elements = ", digital art, high quality, emotional, cinematic lighting, detailed"
        
        return base_prompt + style_elements
    
    def get_pending_triggers(self, user_id: str) -> List[Dict[str, Any]]:
        """Get triggers ready to be sent to user"""
        
        if user_id not in self.proactive_triggers:
            return []
        
        current_time = datetime.now()
        pending_triggers = []
        
        for trigger in self.proactive_triggers[user_id]:
            if not trigger["triggered"]:
                trigger_time = datetime.fromisoformat(trigger["trigger_timing"]["trigger_date"])
                
                if current_time >= trigger_time:
                    pending_triggers.append(trigger)
        
        return pending_triggers
    
    def mark_trigger_sent(self, user_id: str, trigger_id: str):
        """Mark a trigger as sent"""
        
        if user_id in self.proactive_triggers:
            for trigger in self.proactive_triggers[user_id]:
                if trigger["trigger_id"] == trigger_id:
                    trigger["triggered"] = True
                    trigger["sent_at"] = datetime.now().isoformat()
                    break
    
    def get_user_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive memory summary for user"""
        
        if user_id not in self.user_memories:
            return {"error": "No memories found for user"}
        
        memories = self.user_memories[user_id]
        
        return {
            "total_conversations": len(memories.get("conversations", {})),
            "emotional_profile": memories.get("emotional_profile", {}),
            "relationship_stage": memories.get("emotional_profile", {}).get("communication_style", "unknown"),
            "nostalgic_moments_count": len([m for m in memories.get("conversations", {}).values() if m.get("nostalgic_potential", 0) > 0.6]),
            "pending_triggers": len(self.get_pending_triggers(user_id)),
            "memory_depth": "deep" if len(memories.get("conversations", {})) > 10 else "building"
        }