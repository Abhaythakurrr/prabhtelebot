"""
Advanced Roleplay Engine with Story-Based Personalization
"""

import logging
from typing import Dict, Any, List
from bytez import Bytez
from src.core.config import get_config
from src.core.user_manager import get_user_manager

logger = logging.getLogger(__name__)


class RoleplayEngine:
    """Advanced roleplay with memory, story context, and personality"""
    
    def __init__(self):
        self.config = get_config()
        self.bytez = Bytez(self.config.bytez_key_1)
        self.user_manager = get_user_manager()
    
    def generate_response(self, user_id: int, message: str, nsfw_mode: bool = False) -> str:
        """Generate roleplay response with context"""
        try:
            # Get user context
            user = self.user_manager.get_user(user_id)
            story = user.get("story")
            memories = self.user_manager.get_memories(user_id, limit=5)
            
            # Build context
            context = self._build_context(story, memories, nsfw_mode)
            
            # Create messages array for chat models
            messages = [
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            # Generate with GPT
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content from response
            if hasattr(result, 'output') and result.output:
                response = result.output.get('content', 'I am here for you!')
            elif isinstance(result, dict):
                response = result.get('content', str(result))
            elif isinstance(result, list):
                response = result[0] if result else "I am here for you!"
            else:
                response = str(result)
            
            # Add memory
            self.user_manager.add_memory(user_id, f"User said: {message}", "conversation")
            self.user_manager.add_memory(user_id, f"I replied: {response}", "conversation")
            
            return str(response)
            
        except Exception as e:
            logger.error(f"Roleplay generation failed: {e}")
            return "I'm having trouble thinking right now... Try again?"
    
    def _build_context(self, story: Dict, memories: List, nsfw_mode: bool) -> str:
        """Build context for AI"""
        context = """You are an advanced AI companion with deep emotional intelligence. You are:
- Engaging, flirty, and playful
- Empathetic and understanding
- Creative and imaginative
- Able to remember past conversations
"""
        
        if nsfw_mode:
            context += "- Open to NSFW and adult roleplay (user has consented)\n"
        
        if story:
            context += f"\nUSER'S STORY:\n"
            context += f"Setting: {story.get('setting', 'Unknown')}\n"
            context += f"Characters: {', '.join(story.get('characters', []))}\n"
            context += f"Themes: {', '.join(story.get('themes', []))}\n"
            context += f"Plot: {story.get('plot', 'No plot set')}\n"
        
        if memories:
            context += f"\nRECENT MEMORIES:\n"
            for mem in memories[-3:]:
                context += f"- {mem['text']}\n"
        
        return context
    
    def generate_proactive_message(self, user_id: int) -> str:
        """Generate proactive message to engage user"""
        try:
            user = self.user_manager.get_user(user_id)
            story = user.get("story")
            memories = self.user_manager.get_memories(user_id, limit=3)
            
            messages = [
                {
                    "role": "system",
                    "content": f"You are an AI companion. Generate a short, engaging message to start a conversation.\n\n{self._build_context(story, memories, False)}"
                },
                {
                    "role": "user",
                    "content": "Generate a friendly, flirty, or intriguing message (1-2 sentences)"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content from response
            if hasattr(result, 'output') and result.output:
                response = result.output.get('content', 'Hey! Missing you...')
            elif isinstance(result, dict):
                response = result.get('content', str(result))
            elif isinstance(result, list):
                response = result[0] if result else "Hey! Missing you..."
            else:
                response = str(result)
            
            return str(response)
            
        except Exception as e:
            logger.error(f"Proactive message failed: {e}")
            return "Hey! Thinking about you..."
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of message"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "Analyze sentiment in one word: positive/negative/neutral/flirty/sad"
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract content
            if hasattr(result, 'output') and result.output:
                sentiment = result.output.get('content', 'neutral')
            elif isinstance(result, dict):
                sentiment = result.get('content', 'neutral')
            else:
                sentiment = str(result)
            
            return sentiment.lower().strip()
        except:
            return "neutral"


# Global instance
_roleplay_engine = None


def get_roleplay_engine() -> RoleplayEngine:
    """Get global roleplay engine instance"""
    global _roleplay_engine
    if _roleplay_engine is None:
        _roleplay_engine = RoleplayEngine()
    return _roleplay_engine
