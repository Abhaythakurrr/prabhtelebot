"""
Roleplay Story Engine - Interactive Narratives
Thriller, Horror, Romantic, and Dreamy stories with user choices
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from bytez import Bytez
from src.core.config import get_config
from src.core.redis_manager import get_redis_manager
from src.features.mode_engine import get_mode_manager

logger = logging.getLogger(__name__)


class RoleplayStoryEngine:
    """
    Interactive story engine with branching narratives
    Supports: Thriller, Horror, Romantic, Dreamy genres
    """
    
    GENRES = {
        "thriller": {
            "name": "Thriller",
            "emoji": "🔍",
            "description": "Edge-of-your-seat suspense and mystery"
        },
        "horror": {
            "name": "Horror",
            "emoji": "👻",
            "description": "Spine-chilling terror and supernatural"
        },
        "romantic": {
            "name": "Romantic",
            "emoji": "💕",
            "description": "Heartwarming love and connection"
        },
        "dreamy": {
            "name": "Dreamy",
            "emoji": "✨",
            "description": "Magical fantasy and wonder"
        }
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
    
    def start_story(self, user_id: str, genre: str) -> Dict[str, Any]:
        """
        Start a new interactive story
        
        Args:
            user_id: Telegram user ID
            genre: Story genre (thriller, horror, romantic, dreamy)
            
        Returns:
            Story opening with initial choices
        """
        try:
            # Validate genre
            if genre not in self.GENRES:
                return {
                    "success": False,
                    "error": f"Invalid genre. Choose from: {', '.join(self.GENRES.keys())}"
                }
            
            logger.info(f"Starting {genre} story for user {user_id}")
            
            # Generate story opening
            opening = self._generate_story_opening(genre)
            
            # Initialize story state
            story_state = {
                "genre": genre,
                "scene_number": 1,
                "story_context": opening["scene"],
                "previous_choices": [],
                "characters": opening.get("characters", []),
                "current_scene": opening["scene"],
                "choices": opening["choices"],
                "started_at": datetime.now().isoformat()
            }
            
            # Save state
            state_key = f"mode:{user_id}:roleplay:state"
            current_state = self.redis.get(state_key) or {}
            current_state["story"] = story_state
            self.redis.set(state_key, current_state)
            
            logger.info(f"✅ Started {genre} story for user {user_id}")
            
            return {
                "success": True,
                "genre": genre,
                "scene": opening["scene"],
                "choices": opening["choices"],
                "scene_number": 1
            }
            
        except Exception as e:
            logger.error(f"Error starting story for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_choice(self, user_id: str, choice_index: int) -> Dict[str, Any]:
        """
        Process user's choice and generate next scene
        
        Args:
            user_id: Telegram user ID
            choice_index: Index of chosen option (0-2)
            
        Returns:
            Next scene with new choices
        """
        try:
            # Get current story state
            story_state = self.get_story_state(user_id)
            
            if not story_state:
                return {
                    "success": False,
                    "error": "No active story found. Start a new story first."
                }
            
            # Validate choice
            if choice_index < 0 or choice_index >= len(story_state["choices"]):
                return {
                    "success": False,
                    "error": f"Invalid choice. Choose 1-{len(story_state['choices'])}"
                }
            
            # Record choice
            chosen_option = story_state["choices"][choice_index]
            story_state["previous_choices"].append({
                "scene": story_state["scene_number"],
                "choice": chosen_option
            })
            
            # Generate next scene
            next_scene = self._generate_next_scene(story_state, choice_index)
            
            # Update state
            story_state["scene_number"] += 1
            story_state["current_scene"] = next_scene["scene"]
            story_state["choices"] = next_scene["choices"]
            story_state["story_context"] += f"\n\n{next_scene['scene']}"
            
            # Save updated state
            state_key = f"mode:{user_id}:roleplay:state"
            current_state = self.redis.get(state_key) or {}
            current_state["story"] = story_state
            self.redis.set(state_key, current_state)
            
            logger.info(f"✅ Processed choice for user {user_id}, scene {story_state['scene_number']}")
            
            return {
                "success": True,
                "scene": next_scene["scene"],
                "choices": next_scene["choices"],
                "scene_number": story_state["scene_number"]
            }
            
        except Exception as e:
            logger.error(f"Error processing choice for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_story_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get current story state for user"""
        try:
            state_key = f"mode:{user_id}:roleplay:state"
            state = self.redis.get(state_key)
            
            if state and "story" in state:
                return state["story"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting story state for {user_id}: {e}")
            return None
    
    def get_story_progress(self, user_id: str) -> Dict[str, Any]:
        """Get story progress information"""
        try:
            story_state = self.get_story_state(user_id)
            
            if not story_state:
                return {
                    "has_story": False
                }
            
            genre_info = self.GENRES[story_state["genre"]]
            
            return {
                "has_story": True,
                "genre": story_state["genre"],
                "genre_name": genre_info["name"],
                "genre_emoji": genre_info["emoji"],
                "scene_number": story_state["scene_number"],
                "choices_made": len(story_state["previous_choices"]),
                "started_at": story_state.get("started_at")
            }
            
        except Exception as e:
            logger.error(f"Error getting story progress for {user_id}: {e}")
            return {"has_story": False}
    
    def _generate_story_opening(self, genre: str) -> Dict[str, Any]:
        """Generate opening scene for a story"""
        try:
            # Genre-specific prompts
            genre_prompts = {
                "thriller": """Create an engaging thriller story opening. Set up a mysterious situation with tension and intrigue.
Include a protagonist facing a puzzling or dangerous situation. Make it gripping and suspenseful.
The opening should hook the reader immediately.""",
                
                "horror": """Create a chilling horror story opening. Build an eerie atmosphere with unsettling details.
Introduce something supernatural or terrifying. Make the reader feel uneasy and curious.
The opening should be atmospheric and spine-tingling.""",
                
                "romantic": """Create a heartwarming romantic story opening. Introduce a charming meet-cute or emotional moment.
Set up chemistry between characters. Make it sweet, engaging, and emotionally resonant.
The opening should make the reader feel warm and invested.""",
                
                "dreamy": """Create a magical dreamy story opening. Build a fantastical world with wonder and beauty.
Introduce enchanting elements and possibilities. Make it whimsical and captivating.
The opening should transport the reader to another world."""
            }
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a master storyteller creating interactive {genre} stories.

{genre_prompts[genre]}

Generate a story opening (3-4 paragraphs) that:
1. Sets the scene vividly
2. Introduces the protagonist (use "you" for immersion)
3. Creates immediate engagement
4. Ends at a decision point

Then provide exactly 3 meaningful choices that:
- Significantly impact the story direction
- Are all interesting options
- Lead to different outcomes
- Are clearly distinct from each other

Format your response as:
SCENE:
[Your story opening here]

CHOICES:
1. [First choice]
2. [Second choice]
3. [Third choice]

CHARACTERS:
[List main characters mentioned]"""
                },
                {
                    "role": "user",
                    "content": f"Create an engaging {genre} story opening with 3 choices"
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
            parsed = self._parse_story_response(content)
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error generating story opening: {e}")
            # Fallback opening
            return {
                "scene": "The story begins... What will you do?",
                "choices": ["Continue forward", "Look around", "Wait and observe"],
                "characters": ["You"]
            }
    
    def _generate_next_scene(self, story_state: Dict[str, Any], choice_index: int) -> Dict[str, Any]:
        """Generate next scene based on previous choice"""
        try:
            genre = story_state["genre"]
            chosen_option = story_state["choices"][choice_index]
            previous_context = story_state["story_context"][-2000:]  # Last 2000 chars
            
            # Build context from previous choices
            choice_history = "\n".join([
                f"Scene {c['scene']}: Chose '{c['choice']}'"
                for c in story_state["previous_choices"][-3:]  # Last 3 choices
            ])
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are continuing an interactive {genre} story.

Maintain consistency with previous events and the chosen action.
Build on the story naturally while keeping the {genre} genre strong.

Previous context:
{previous_context}

Choice history:
{choice_history}

User chose: "{chosen_option}"

Generate the next scene (2-3 paragraphs) that:
1. Follows naturally from their choice
2. Advances the plot meaningfully
3. Maintains {genre} atmosphere
4. Ends at a new decision point

Then provide exactly 3 new meaningful choices that:
- Build on current situation
- Offer distinct paths forward
- Maintain story momentum
- Are all compelling options

Format your response as:
SCENE:
[Next scene here]

CHOICES:
1. [First choice]
2. [Second choice]
3. [Third choice]"""
                },
                {
                    "role": "user",
                    "content": f"Continue the story after the user chose: {chosen_option}"
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
            parsed = self._parse_story_response(content)
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error generating next scene: {e}")
            # Fallback scene
            return {
                "scene": "The story continues...",
                "choices": ["Continue", "Try something else", "Look around"]
            }
    
    def _parse_story_response(self, content: str) -> Dict[str, Any]:
        """Parse AI response into scene and choices"""
        try:
            scene = ""
            choices = []
            characters = []
            
            # Split by sections
            if "SCENE:" in content:
                scene_part = content.split("SCENE:")[1].split("CHOICES:")[0].strip()
                scene = scene_part
            
            if "CHOICES:" in content:
                choices_part = content.split("CHOICES:")[1]
                if "CHARACTERS:" in choices_part:
                    choices_part = choices_part.split("CHARACTERS:")[0]
                
                # Extract choices
                lines = choices_part.strip().split("\n")
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith("-")):
                        # Remove numbering
                        choice = line.lstrip("0123456789.-) ").strip()
                        if choice:
                            choices.append(choice)
            
            if "CHARACTERS:" in content:
                char_part = content.split("CHARACTERS:")[1].strip()
                characters = [c.strip() for c in char_part.split(",") if c.strip()]
            
            # Ensure we have 3 choices
            if len(choices) < 3:
                choices.extend(["Continue", "Look around", "Wait"][:3-len(choices)])
            choices = choices[:3]  # Max 3 choices
            
            return {
                "scene": scene or "The story unfolds...",
                "choices": choices,
                "characters": characters
            }
            
        except Exception as e:
            logger.error(f"Error parsing story response: {e}")
            return {
                "scene": content[:500] if content else "The story continues...",
                "choices": ["Continue", "Try something else", "Look around"],
                "characters": []
            }


# Global instance
_roleplay_story_engine = None


def get_roleplay_story_engine() -> RoleplayStoryEngine:
    """Get global roleplay story engine instance"""
    global _roleplay_story_engine
    if _roleplay_story_engine is None:
        _roleplay_story_engine = RoleplayStoryEngine()
    return _roleplay_story_engine
