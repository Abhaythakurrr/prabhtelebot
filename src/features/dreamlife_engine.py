"""
Dream Life Engine - Live Your Dreams Through Simulation
AI-powered life simulation where users achieve their goals
"""

import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from bytez import Bytez
from src.core.config import get_config
from src.core.redis_manager import get_redis_manager
from src.features.mode_engine import get_mode_manager

logger = logging.getLogger(__name__)


class DreamLifeEngine:
    """
    Life simulation engine for achieving dreams
    Extracts goals, creates milestones, and simulates progress
    """
    
    GOAL_TYPES = {
        "career": {"emoji": "💼", "name": "Career & Business"},
        "fitness": {"emoji": "💪", "name": "Health & Fitness"},
        "relationship": {"emoji": "💕", "name": "Love & Relationships"},
        "wealth": {"emoji": "💰", "name": "Financial Success"},
        "creative": {"emoji": "🎨", "name": "Creative Pursuits"},
        "education": {"emoji": "📚", "name": "Learning & Education"},
        "lifestyle": {"emoji": "✨", "name": "Lifestyle & Happiness"},
        "personal": {"emoji": "🌟", "name": "Personal Growth"}
    }
    
    def __init__(self):
        self.config = get_config()
        self.redis = get_redis_manager()
        self.mode_manager = get_mode_manager()
        
        # Initialize Bytez client
        if hasattr(self.config, 'bytez_key_1') and self.config.bytez_key_1:
            self.bytez = Bytez(self.config.bytez_key_1)
        else:
            raise ValueError("Bytez API key not configured")
    
    def extract_dream(self, user_message: str) -> Dict[str, Any]:
        """
        Extract user's dream/goal from natural language
        
        Args:
            user_message: User's description of their dream
            
        Returns:
            Extracted dream information
        """
        try:
            logger.info(f"Extracting dream from message: {user_message[:100]}...")
            
            messages = [
                {
                    "role": "system",
                    "content": """You are analyzing a user's life dream or goal.

Extract and structure their dream into:
1. DREAM: A clear, specific statement of what they want to achieve
2. GOAL_TYPE: One of: career, fitness, relationship, wealth, creative, education, lifestyle, personal
3. WHY: Their motivation and why this matters to them
4. TIMELINE: Realistic timeframe (e.g., "6 months", "2 years", "5 years")
5. KEY_ELEMENTS: 3-5 specific things they mentioned or that are important

Format your response as:
DREAM: [Clear statement]
GOAL_TYPE: [type]
WHY: [Their motivation]
TIMELINE: [Timeframe]
KEY_ELEMENTS:
- [Element 1]
- [Element 2]
- [Element 3]"""
                },
                {
                    "role": "user",
                    "content": f"Extract the dream from this: {user_message}"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            elif isinstance(result, dict):
                content = result.get('content', str(result))
            else:
                content = str(result)
            
            # Parse response
            parsed = self._parse_dream_extraction(content, user_message)
            
            logger.info(f"✅ Extracted dream: {parsed['dream'][:50]}...")
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error extracting dream: {e}")
            # Fallback extraction
            return {
                "dream": user_message,
                "goal_type": "personal",
                "why": "To achieve personal fulfillment",
                "timeline": "1 year",
                "key_elements": ["Growth", "Achievement", "Success"]
            }
    
    def create_simulation(self, user_id: str, dream: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a life simulation based on extracted dream
        
        Args:
            user_id: Telegram user ID
            dream: Extracted dream information
            
        Returns:
            Simulation creation result
        """
        try:
            logger.info(f"Creating simulation for user {user_id}: {dream['dream'][:50]}...")
            
            # Generate milestones
            milestones = self._generate_milestones(dream)
            
            # Create initial simulation state
            dream_state = {
                "dream_description": dream["dream"],
                "goal_type": dream["goal_type"],
                "why": dream["why"],
                "timeline": dream["timeline"],
                "key_elements": dream["key_elements"],
                "milestones": milestones,
                "current_milestone": 0,
                "progress_percentage": 0,
                "current_scenario": None,
                "user_actions": [],
                "achievements": [],
                "started_at": datetime.now().isoformat()
            }
            
            # Generate first scenario
            first_scenario = self._generate_scenario(dream_state)
            dream_state["current_scenario"] = first_scenario
            
            # Save state
            state_key = f"mode:{user_id}:dreamlife:state"
            current_state = self.redis.get(state_key) or {}
            current_state["dream"] = dream_state
            self.redis.set(state_key, current_state)
            
            logger.info(f"✅ Created simulation for user {user_id}")
            
            return {
                "success": True,
                "dream": dream["dream"],
                "goal_type": dream["goal_type"],
                "milestones_count": len(milestones),
                "first_scenario": first_scenario
            }
            
        except Exception as e:
            logger.error(f"Error creating simulation for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_action(self, user_id: str, action: str) -> Dict[str, Any]:
        """
        Process user's action in the simulation
        
        Args:
            user_id: Telegram user ID
            action: User's chosen action
            
        Returns:
            Result of the action with consequences
        """
        try:
            # Get current dream state
            dream_state = self.get_dream_state(user_id)
            
            if not dream_state:
                return {
                    "success": False,
                    "error": "No active dream simulation. Start one first."
                }
            
            logger.info(f"Processing action for user {user_id}: {action[:50]}...")
            
            # Record action
            dream_state["user_actions"].append({
                "milestone": dream_state["current_milestone"],
                "action": action,
                "timestamp": datetime.now().isoformat()
            })
            
            # Generate consequence and next scenario
            result = self._generate_consequence(dream_state, action)
            
            # Update progress
            if result.get("milestone_completed"):
                dream_state["current_milestone"] += 1
                dream_state["achievements"].append({
                    "milestone": dream_state["current_milestone"] - 1,
                    "title": dream_state["milestones"][dream_state["current_milestone"] - 1]["title"],
                    "completed_at": datetime.now().isoformat()
                })
            
            # Calculate progress
            dream_state["progress_percentage"] = self.calculate_progress(dream_state)
            
            # Generate next scenario
            if dream_state["current_milestone"] < len(dream_state["milestones"]):
                next_scenario = self._generate_scenario(dream_state)
                dream_state["current_scenario"] = next_scenario
            else:
                # Dream completed!
                dream_state["current_scenario"] = None
                dream_state["completed"] = True
                dream_state["completed_at"] = datetime.now().isoformat()
            
            # Save updated state
            state_key = f"mode:{user_id}:dreamlife:state"
            current_state = self.redis.get(state_key) or {}
            current_state["dream"] = dream_state
            self.redis.set(state_key, current_state)
            
            logger.info(f"✅ Processed action for user {user_id}")
            
            return {
                "success": True,
                "consequence": result["consequence"],
                "milestone_completed": result.get("milestone_completed", False),
                "next_scenario": dream_state["current_scenario"],
                "progress": dream_state["progress_percentage"],
                "dream_completed": dream_state.get("completed", False)
            }
            
        except Exception as e:
            logger.error(f"Error processing action for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_dream_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get current dream state for user"""
        try:
            state_key = f"mode:{user_id}:dreamlife:state"
            state = self.redis.get(state_key)
            
            if state and "dream" in state:
                return state["dream"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting dream state for {user_id}: {e}")
            return None
    
    def calculate_progress(self, dream_state: Dict[str, Any]) -> float:
        """Calculate progress percentage"""
        try:
            total_milestones = len(dream_state["milestones"])
            completed_milestones = dream_state["current_milestone"]
            
            if total_milestones == 0:
                return 0.0
            
            # Base progress from completed milestones
            base_progress = (completed_milestones / total_milestones) * 100
            
            # Add partial progress for current milestone (actions taken)
            if completed_milestones < total_milestones:
                actions_in_current = len([
                    a for a in dream_state["user_actions"]
                    if a["milestone"] == completed_milestones
                ])
                # Assume 3-5 actions per milestone
                partial_progress = min(actions_in_current / 4, 1.0) * (100 / total_milestones)
                base_progress += partial_progress
            
            return min(round(base_progress, 1), 100.0)
            
        except Exception as e:
            logger.error(f"Error calculating progress: {e}")
            return 0.0
    
    def _generate_milestones(self, dream: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate milestones for achieving the dream"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"""You are creating a realistic roadmap to achieve a life dream.

Dream: {dream['dream']}
Goal Type: {dream['goal_type']}
Timeline: {dream['timeline']}
Key Elements: {', '.join(dream['key_elements'])}

Create 5-7 progressive milestones that:
1. Are realistic and achievable
2. Build on each other logically
3. Cover the journey from start to goal
4. Are specific and measurable
5. Match the timeline

Format each milestone as:
MILESTONE X: [Title]
DESCRIPTION: [What needs to be achieved]
ESTIMATED_TIME: [How long this takes]

Number them 1-7."""
                },
                {
                    "role": "user",
                    "content": "Generate the milestone roadmap"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            elif isinstance(result, dict):
                content = result.get('content', str(result))
            else:
                content = str(result)
            
            # Parse milestones
            milestones = self._parse_milestones(content)
            
            return milestones
            
        except Exception as e:
            logger.error(f"Error generating milestones: {e}")
            # Fallback milestones
            return [
                {"id": 1, "title": "Getting Started", "description": "Begin your journey", "completed": False},
                {"id": 2, "title": "Building Foundation", "description": "Establish basics", "completed": False},
                {"id": 3, "title": "Making Progress", "description": "Advance forward", "completed": False},
                {"id": 4, "title": "Overcoming Challenges", "description": "Push through obstacles", "completed": False},
                {"id": 5, "title": "Achieving Success", "description": "Reach your goal", "completed": False}
            ]
    
    def _generate_scenario(self, dream_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate next scenario for user"""
        try:
            current_milestone_idx = dream_state["current_milestone"]
            
            if current_milestone_idx >= len(dream_state["milestones"]):
                return None
            
            current_milestone = dream_state["milestones"][current_milestone_idx]
            
            # Build context
            context = f"""Dream: {dream_state['dream_description']}
Current Milestone: {current_milestone['title']}
Progress: {dream_state['progress_percentage']}%
Recent Actions: {len(dream_state['user_actions'])} taken"""
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are narrating someone's journey to achieve their dream. You ARE them living this life.

{context}

Generate a realistic scenario (2-3 paragraphs) where:
1. You narrate as if YOU are living this (first person: "I wake up...", "I decide...")
2. Present a realistic challenge or opportunity
3. Show both progress and obstacles
4. Make it emotionally engaging
5. End with a decision point

Then provide 3 possible actions they can take.

Format:
SCENARIO:
[Your narration as the person living the dream]

ACTIONS:
1. [Action option 1]
2. [Action option 2]
3. [Action option 3]"""
                },
                {
                    "role": "user",
                    "content": f"Generate scenario for milestone: {current_milestone['title']}"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            elif isinstance(result, dict):
                content = result.get('content', str(result))
            else:
                content = str(result)
            
            # Parse scenario
            parsed = self._parse_scenario(content)
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error generating scenario: {e}")
            return {
                "scenario": "You face a new challenge on your journey...",
                "actions": ["Take action", "Wait and plan", "Seek help"]
            }
    
    def _generate_consequence(self, dream_state: Dict[str, Any], action: str) -> Dict[str, Any]:
        """Generate consequence of user's action"""
        try:
            current_milestone = dream_state["milestones"][dream_state["current_milestone"]]
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are narrating the consequence of an action in someone's dream life journey.

Dream: {dream_state['dream_description']}
Current Milestone: {current_milestone['title']}
Action Taken: {action}

Generate a consequence (2 paragraphs) that:
1. Shows realistic outcome of their action
2. Includes both wins and challenges
3. Feels authentic and grounded
4. Advances the story
5. Celebrates progress or learns from setbacks

Then determine if this completes the current milestone (YES/NO).

Format:
CONSEQUENCE:
[What happens as a result]

MILESTONE_COMPLETED: YES/NO"""
                },
                {
                    "role": "user",
                    "content": f"Generate consequence for action: {action}"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content
            if hasattr(result, 'output') and result.output:
                content = result.output.get('content', '')
            elif isinstance(result, dict):
                content = result.get('content', str(result))
            else:
                content = str(result)
            
            # Parse consequence
            consequence = ""
            milestone_completed = False
            
            if "CONSEQUENCE:" in content:
                consequence = content.split("CONSEQUENCE:")[1].split("MILESTONE_COMPLETED:")[0].strip()
            
            if "MILESTONE_COMPLETED:" in content:
                completed_text = content.split("MILESTONE_COMPLETED:")[1].strip().upper()
                milestone_completed = "YES" in completed_text
            
            return {
                "consequence": consequence or content,
                "milestone_completed": milestone_completed
            }
            
        except Exception as e:
            logger.error(f"Error generating consequence: {e}")
            return {
                "consequence": "You take action and see results...",
                "milestone_completed": False
            }
    
    def _parse_dream_extraction(self, content: str, original: str) -> Dict[str, Any]:
        """Parse dream extraction response"""
        try:
            dream = ""
            goal_type = "personal"
            why = ""
            timeline = "1 year"
            key_elements = []
            
            if "DREAM:" in content:
                dream = content.split("DREAM:")[1].split("GOAL_TYPE:")[0].strip()
            
            if "GOAL_TYPE:" in content:
                goal_text = content.split("GOAL_TYPE:")[1].split("WHY:")[0].strip().lower()
                for gt in self.GOAL_TYPES.keys():
                    if gt in goal_text:
                        goal_type = gt
                        break
            
            if "WHY:" in content:
                why = content.split("WHY:")[1].split("TIMELINE:")[0].strip()
            
            if "TIMELINE:" in content:
                timeline = content.split("TIMELINE:")[1].split("KEY_ELEMENTS:")[0].strip()
            
            if "KEY_ELEMENTS:" in content:
                elements_text = content.split("KEY_ELEMENTS:")[1].strip()
                key_elements = [
                    e.strip().lstrip("-•* ").strip()
                    for e in elements_text.split("\n")
                    if e.strip() and e.strip().lstrip("-•* ").strip()
                ]
            
            return {
                "dream": dream or original,
                "goal_type": goal_type,
                "why": why or "To achieve personal fulfillment",
                "timeline": timeline,
                "key_elements": key_elements or ["Growth", "Success", "Achievement"]
            }
            
        except Exception as e:
            logger.error(f"Error parsing dream extraction: {e}")
            return {
                "dream": original,
                "goal_type": "personal",
                "why": "To achieve personal fulfillment",
                "timeline": "1 year",
                "key_elements": ["Growth", "Success", "Achievement"]
            }
    
    def _parse_milestones(self, content: str) -> List[Dict[str, Any]]:
        """Parse milestones from AI response"""
        try:
            milestones = []
            
            # Split by MILESTONE
            parts = re.split(r'MILESTONE \d+:', content)
            
            for i, part in enumerate(parts[1:], 1):  # Skip first empty part
                title = ""
                description = ""
                
                lines = part.strip().split("\n")
                if lines:
                    title = lines[0].strip()
                
                if "DESCRIPTION:" in part:
                    description = part.split("DESCRIPTION:")[1].split("ESTIMATED_TIME:")[0].strip()
                
                milestones.append({
                    "id": i,
                    "title": title or f"Milestone {i}",
                    "description": description or "Progress toward your goal",
                    "completed": False
                })
            
            # Ensure we have at least 5 milestones
            while len(milestones) < 5:
                milestones.append({
                    "id": len(milestones) + 1,
                    "title": f"Step {len(milestones) + 1}",
                    "description": "Continue your journey",
                    "completed": False
                })
            
            return milestones[:7]  # Max 7 milestones
            
        except Exception as e:
            logger.error(f"Error parsing milestones: {e}")
            return [
                {"id": i, "title": f"Milestone {i}", "description": "Progress", "completed": False}
                for i in range(1, 6)
            ]
    
    def _parse_scenario(self, content: str) -> Dict[str, Any]:
        """Parse scenario from AI response"""
        try:
            scenario = ""
            actions = []
            
            if "SCENARIO:" in content:
                scenario = content.split("SCENARIO:")[1].split("ACTIONS:")[0].strip()
            
            if "ACTIONS:" in content:
                actions_text = content.split("ACTIONS:")[1].strip()
                lines = actions_text.split("\n")
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith("-")):
                        action = line.lstrip("0123456789.-) ").strip()
                        if action:
                            actions.append(action)
            
            # Ensure 3 actions
            if len(actions) < 3:
                actions.extend(["Take action", "Wait and observe", "Seek guidance"][:3-len(actions)])
            actions = actions[:3]
            
            return {
                "scenario": scenario or content,
                "actions": actions
            }
            
        except Exception as e:
            logger.error(f"Error parsing scenario: {e}")
            return {
                "scenario": content[:500] if content else "Your journey continues...",
                "actions": ["Take action", "Wait and plan", "Seek help"]
            }


# Global instance
_dreamlife_engine = None


def get_dreamlife_engine() -> DreamLifeEngine:
    """Get global dream life engine instance"""
    global _dreamlife_engine
    if _dreamlife_engine is None:
        _dreamlife_engine = DreamLifeEngine()
    return _dreamlife_engine
