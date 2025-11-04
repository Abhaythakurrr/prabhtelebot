"""
Luci Mode Engine - Brutal Mentor Using Dark Psychology
Intense transformation system for creating unstoppable winners
⚠️ WARNING: This mode uses aggressive psychological techniques
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from bytez import Bytez
from src.core.config import get_config
from src.core.redis_manager import get_redis_manager
from src.features.mode_engine import get_mode_manager

logger = logging.getLogger(__name__)


class LuciEngine:
    """
    Brutal mentor using dark psychology for transformation
    ⚠️ Intense, aggressive, no-nonsense approach
    """
    
    FOCUS_AREAS = {
        "physical": {
            "name": "Physical Dominance",
            "emoji": "💪",
            "description": "Build an unstoppable physique"
        },
        "mental": {
            "name": "Mental Fortitude",
            "emoji": "🧠",
            "description": "Forge an unbreakable mind"
        },
        "wealth": {
            "name": "Wealth Building",
            "emoji": "💰",
            "description": "Achieve financial dominance"
        },
        "emotional": {
            "name": "Emotional Mastery",
            "emoji": "🎯",
            "description": "Control your emotions completely"
        },
        "respect": {
            "name": "Respect & Fame",
            "emoji": "👑",
            "description": "Build your name and influence"
        }
    }
    
    # Intensity levels 1-10
    MIN_INTENSITY = 1
    MAX_INTENSITY = 10
    DEFAULT_INTENSITY = 5
    
    # Safety thresholds
    MAX_DAILY_CHALLENGES = 5
    COOLDOWN_HOURS = 2
    
    def __init__(self):
        self.config = get_config()
        self.redis = get_redis_manager()
        self.mode_manager = get_mode_manager()
        
        # Initialize Bytez client
        if hasattr(self.config, 'bytez_key_1') and self.config.bytez_key_1:
            self.bytez = Bytez(self.config.bytez_key_1)
        else:
            raise ValueError("Bytez API key not configured")
    
    def activate_luci(self, user_id: str, focus_area: str, intensity: int = None) -> Dict[str, Any]:
        """Activate Luci mode with warnings"""
        try:
            if focus_area not in self.FOCUS_AREAS:
                return {"success": False, "error": f"Invalid focus area"}
            
            if intensity is None:
                intensity = self.DEFAULT_INTENSITY
            intensity = max(self.MIN_INTENSITY, min(intensity, self.MAX_INTENSITY))
            
            # Generate AI-powered assessment
            assessment = self._assess_current_state(user_id, focus_area)
            
            # Generate AI-powered first challenge
            first_challenge = self._generate_challenge(focus_area, intensity)
            
            # Create Luci state
            luci_state = {
                "focus_area": focus_area,
                "intensity_level": intensity,
                "assessment": assessment,
                "challenges_completed": 0,
                "transformation_score": 0,
                "current_challenge": first_challenge,
                "user_responses": [],
                "breakthrough_moments": [],
                "activated_at": datetime.now().isoformat(),
                "last_challenge_at": datetime.now().isoformat(),
                "daily_challenges_count": 1,
                "last_reset_date": datetime.now().date().isoformat()
            }
            
            # Save state
            state_key = f"mode:{user_id}:luci:state"
            current_state = self.redis.get(state_key) or {}
            current_state["luci"] = luci_state
            self.redis.set(state_key, current_state)
            
            return {
                "success": True,
                "focus_area": focus_area,
                "intensity": intensity,
                "warning": self._get_activation_warning(),
                "assessment": assessment,
                "first_challenge": first_challenge
            }
        except Exception as e:
            logger.error(f"Error activating Luci: {e}")
            return {"success": False, "error": str(e)}
    
    def process_response(self, user_id: str, response: str) -> Dict[str, Any]:
        """Process user's response to Luci's challenge"""
        try:
            luci_state = self.get_luci_state(user_id)
            if not luci_state:
                return {"success": False, "error": "Luci mode not active"}
            
            # Check cooldown
            if not self._check_cooldown(luci_state):
                remaining = self._get_cooldown_remaining(luci_state)
                return {"success": False, "error": f"Cooldown active. Wait {remaining} minutes", "cooldown": True}
            
            # Check daily limit
            if not self._check_daily_limit(luci_state):
                return {"success": False, "error": "Daily challenge limit reached", "daily_limit": True}
            
            # Generate AI-powered feedback
            feedback_result = self._generate_feedback(luci_state, response)
            score_change = feedback_result.get("score_change", 5)
            feedback = feedback_result.get("feedback", "Not bad. But you can do better.")
            breakthrough = feedback_result.get("breakthrough")
            
            # Update state
            luci_state["transformation_score"] += score_change
            luci_state["transformation_score"] = max(0, min(100, luci_state["transformation_score"]))
            luci_state["challenges_completed"] += 1
            
            # Record breakthrough if any
            if breakthrough:
                luci_state["breakthrough_moments"].append({
                    "moment": breakthrough,
                    "timestamp": datetime.now().isoformat(),
                    "score": luci_state["transformation_score"]
                })
            
            # Generate next AI-powered challenge
            next_challenge = self._generate_challenge(luci_state["focus_area"], luci_state["intensity_level"])
            
            luci_state["current_challenge"] = next_challenge
            luci_state["last_challenge_at"] = datetime.now().isoformat()
            luci_state["daily_challenges_count"] += 1
            
            # Save state
            state_key = f"mode:{user_id}:luci:state"
            current_state = self.redis.get(state_key) or {}
            current_state["luci"] = luci_state
            self.redis.set(state_key, current_state)
            
            return {
                "success": True,
                "feedback": feedback,
                "score_change": score_change,
                "transformation_score": luci_state["transformation_score"],
                "breakthrough": None,
                "next_challenge": next_challenge,
                "intensity": luci_state["intensity_level"]
            }
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            return {"success": False, "error": str(e)}
    
    def get_luci_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get current Luci state"""
        try:
            state_key = f"mode:{user_id}:luci:state"
            state = self.redis.get(state_key)
            
            if state and "luci" in state:
                luci_state = state["luci"]
                # Reset daily count if new day
                last_reset = luci_state.get("last_reset_date")
                today = datetime.now().date().isoformat()
                
                if last_reset != today:
                    luci_state["daily_challenges_count"] = 0
                    luci_state["last_reset_date"] = today
                    state["luci"] = luci_state
                    self.redis.set(state_key, state)
                
                return luci_state
            return None
        except Exception as e:
            logger.error(f"Error getting Luci state: {e}")
            return None
    
    def track_transformation(self, user_id: str) -> Dict[str, Any]:
        """Get transformation tracking information"""
        try:
            luci_state = self.get_luci_state(user_id)
            if not luci_state:
                return {"active": False}
            
            focus_info = self.FOCUS_AREAS[luci_state["focus_area"]]
            
            return {
                "active": True,
                "focus_area": luci_state["focus_area"],
                "focus_name": focus_info["name"],
                "focus_emoji": focus_info["emoji"],
                "intensity_level": luci_state["intensity_level"],
                "transformation_score": luci_state["transformation_score"],
                "challenges_completed": luci_state["challenges_completed"],
                "breakthrough_count": len(luci_state["breakthrough_moments"]),
                "activated_at": luci_state.get("activated_at")
            }
        except Exception as e:
            logger.error(f"Error tracking transformation: {e}")
            return {"active": False}
    
    def _check_cooldown(self, luci_state: Dict[str, Any]) -> bool:
        """Check if cooldown period has passed"""
        try:
            last_challenge = luci_state.get("last_challenge_at")
            if not last_challenge:
                return True
            
            last_time = datetime.fromisoformat(last_challenge)
            cooldown_end = last_time + timedelta(hours=self.COOLDOWN_HOURS)
            
            return datetime.now() >= cooldown_end
        except Exception as e:
            logger.error(f"Error checking cooldown: {e}")
            return True
    
    def _get_cooldown_remaining(self, luci_state: Dict[str, Any]) -> int:
        """Get remaining cooldown time in minutes"""
        try:
            last_challenge = luci_state.get("last_challenge_at")
            if not last_challenge:
                return 0
            
            last_time = datetime.fromisoformat(last_challenge)
            cooldown_end = last_time + timedelta(hours=self.COOLDOWN_HOURS)
            remaining = cooldown_end - datetime.now()
            
            return max(0, int(remaining.total_seconds() / 60))
        except Exception as e:
            logger.error(f"Error getting cooldown remaining: {e}")
            return 0
    
    def _check_daily_limit(self, luci_state: Dict[str, Any]) -> bool:
        """Check if daily challenge limit reached"""
        try:
            return luci_state.get("daily_challenges_count", 0) < self.MAX_DAILY_CHALLENGES
        except Exception as e:
            logger.error(f"Error checking daily limit: {e}")
            return True
    
    def _assess_current_state(self, user_id: str, focus_area: str) -> Dict[str, Any]:
        """Generate AI-powered brutal assessment"""
        try:
            focus_info = self.FOCUS_AREAS[focus_area]
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are Luci - a brutal, no-nonsense mentor who uses dark psychology.

You're assessing someone's current state in: {focus_info['name']}

Be BRUTALLY honest. Expose weaknesses. Challenge them. No sugar-coating.

Generate a harsh but motivating assessment (2-3 sentences) that:
1. Points out where they're failing
2. Challenges their excuses
3. Shows them what they COULD be

Then list 3 specific weaknesses and 1 potential strength."""
                },
                {
                    "role": "user",
                    "content": f"Assess my current state in {focus_area}"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            else:
                content = str(result)
            
            return {
                "assessment": content,
                "weaknesses": ["Lack of discipline", "Making excuses", "Not taking action"],
                "strengths": []
            }
        except Exception as e:
            logger.error(f"Error generating assessment: {e}")
            return {
                "assessment": "You're not where you should be. Time to change that.",
                "weaknesses": ["Lack of discipline", "Making excuses", "Not taking action"],
                "strengths": []
            }
    
    def _generate_challenge(self, focus_area: str, intensity: int) -> Dict[str, Any]:
        """Generate AI-powered brutal challenge"""
        try:
            focus_info = self.FOCUS_AREAS[focus_area]
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are Luci - brutal mentor using dark psychology.

Focus: {focus_info['name']}
Intensity: {intensity}/10

Generate a BRUTAL challenge that:
1. Pushes them beyond comfort zone
2. Is specific and actionable
3. Matches intensity level {intensity}/10
4. Uses aggressive motivation
5. Demands immediate action

Higher intensity = more brutal and demanding.

Format:
CHALLENGE: [Your brutal challenge - be aggressive]
ACTION: [Specific action required]
DEADLINE: [Timeframe - be aggressive]"""
                },
                {
                    "role": "user",
                    "content": f"Give me a challenge for {focus_area}"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            else:
                content = str(result)
            
            # Parse response
            lines = content.split('\n')
            challenge = action = deadline = ""
            for line in lines:
                if line.startswith("CHALLENGE:"):
                    challenge = line.replace("CHALLENGE:", "").strip()
                elif line.startswith("ACTION:"):
                    action = line.replace("ACTION:", "").strip()
                elif line.startswith("DEADLINE:"):
                    deadline = line.replace("DEADLINE:", "").strip()
            
            return {
                "challenge": challenge or content,
                "action_required": action or "Take action now",
                "deadline": deadline or "Today"
            }
        except Exception as e:
            logger.error(f"Error generating challenge: {e}")
            return {
                "challenge": "Stop making excuses. Take action NOW.",
                "action_required": "Do something that scares you",
                "deadline": "Today"
            }
    
    def _generate_feedback(self, luci_state: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Generate AI-powered brutal feedback"""
        try:
            challenge = luci_state["current_challenge"]
            intensity = luci_state["intensity_level"]
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are Luci - brutal mentor using dark psychology.

Challenge given: {challenge['challenge']}
User's response: {response}
Intensity: {intensity}/10

Analyze their response and give BRUTAL feedback (2-3 sentences):
1. Call out excuses immediately
2. Challenge weak responses
3. Praise only real action (be stingy)
4. Push them harder

Then determine:
- Score change: -10 to +15 (harsh grading)
- Is this a breakthrough? (rare, only for exceptional effort)

Format:
FEEDBACK: [Your brutal feedback]
SCORE: [number between -10 and +15]
BREAKTHROUGH: [YES/NO]"""
                },
                {
                    "role": "user",
                    "content": f"Give feedback on: {response}"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            else:
                content = str(result)
            
            # Parse response
            lines = content.split('\n')
            feedback = ""
            score_change = 5
            breakthrough = None
            
            for line in lines:
                if line.startswith("FEEDBACK:"):
                    feedback = line.replace("FEEDBACK:", "").strip()
                elif line.startswith("SCORE:"):
                    try:
                        score_change = int(line.replace("SCORE:", "").strip().replace("+", ""))
                    except:
                        score_change = 5
                elif line.startswith("BREAKTHROUGH:"):
                    if "YES" in line.upper():
                        breakthrough = "Significant progress made"
            
            return {
                "feedback": feedback or content,
                "score_change": score_change,
                "breakthrough": breakthrough
            }
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            return {
                "feedback": "Not bad. But you can do better. Push harder next time.",
                "score_change": 5,
                "breakthrough": None
            }
    
    def _get_activation_warning(self) -> str:
        """Get warning message for Luci mode activation"""
        return """⚠️ LUCI MODE WARNING ⚠️

This mode uses INTENSE psychological techniques:
• Brutal honesty and harsh feedback
• Aggressive motivation tactics
• No excuses accepted
• Pushes you beyond comfort zone
• Can be emotionally challenging

NOT suitable for everyone.

If you experience distress, exit immediately.
This is NOT professional therapy.

Type 'exit luci' anytime to stop.

Ready to transform? Let's go."""


# Global instance
_luci_engine = None


def get_luci_engine() -> LuciEngine:
    """Get global Luci engine instance"""
    global _luci_engine
    if _luci_engine is None:
        _luci_engine = LuciEngine()
    return _luci_engine
