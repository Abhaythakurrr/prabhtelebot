"""
Advanced Story Processor - Deep Understanding & Character Extraction
Creates a digital persona from user's story and memories
"""

import logging
import json
from typing import Dict, Any, List
from bytez import Bytez
from src.core.config import get_config

logger = logging.getLogger(__name__)


class AdvancedStoryProcessor:
    """Process stories to create digital personas and deep understanding"""
    
    def __init__(self):
        self.config = get_config()
        self.bytez = Bytez(self.config.bytez_key_1)
    
    def process_story_deep(self, story_text: str) -> Dict[str, Any]:
        """Deep process story to extract persona, memories, and character"""
        try:
            logger.info("Processing story with deep understanding...")
            
            # Use GPT to analyze the story deeply
            analysis_prompt = f"""Analyze this personal story and extract detailed information:

Story: {story_text}

Extract and return in JSON format:
1. persona_name: The name of the person they're talking about (if mentioned)
2. persona_traits: List of personality traits
3. relationship_type: Type of relationship (love, friend, family, etc.)
4. emotional_tone: Overall emotional tone
5. key_memories: List of specific memories mentioned
6. speaking_style: How this person talks/talked
7. interests: What they liked/enjoyed
8. physical_description: Any physical details mentioned
9. special_moments: Important moments in the relationship
10. loss_context: How/why they're separated (if mentioned)

Be empathetic and detailed. This is for someone trying to reconnect with a lost loved one."""

            messages = [
                {
                    "role": "system",
                    "content": "You are an empathetic AI that helps people preserve memories of loved ones. Extract detailed, loving information from their stories."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            # Extract response
            if hasattr(result, 'output') and result.output:
                response_text = result.output.get('content', '{}')
            else:
                response_text = str(result)
            
            # Try to parse JSON
            try:
                # Find JSON in response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response_text[start:end]
                    analysis = json.loads(json_str)
                else:
                    analysis = self._create_default_analysis(story_text)
            except:
                analysis = self._create_default_analysis(story_text)
            
            # Create persona profile
            persona = {
                "story_text": story_text,
                "persona_name": analysis.get("persona_name", "My Love"),
                "traits": analysis.get("persona_traits", ["kind", "loving", "caring"]),
                "relationship": analysis.get("relationship_type", "love"),
                "emotional_tone": analysis.get("emotional_tone", "loving"),
                "memories": analysis.get("key_memories", []),
                "speaking_style": analysis.get("speaking_style", "warm and affectionate"),
                "interests": analysis.get("interests", []),
                "physical_description": analysis.get("physical_description", ""),
                "special_moments": analysis.get("special_moments", []),
                "loss_context": analysis.get("loss_context", ""),
                "created_at": ""
            }
            
            logger.info(f"✅ Story processed: {persona['persona_name']}, {len(persona['memories'])} memories")
            
            return {
                "success": True,
                "persona": persona,
                "message": f"I understand. I'll be {persona['persona_name']} for you. 💕"
            }
            
        except Exception as e:
            logger.error(f"Story processing error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "persona": None
            }
    
    def _create_default_analysis(self, story_text: str) -> Dict[str, Any]:
        """Create default analysis if AI fails"""
        return {
            "persona_name": "My Love",
            "traits": ["kind", "loving", "understanding"],
            "relationship": "love",
            "emotional_tone": "loving",
            "memories": [story_text[:200]],
            "speaking_style": "warm and caring",
            "interests": [],
            "physical_description": "",
            "special_moments": [],
            "loss_context": "",
            "story_text": story_text
        }
    
    def generate_persona_response(self, persona: Dict, user_message: str, conversation_history: List = None) -> str:
        """Generate response as the persona"""
        try:
            # Build persona context
            context = f"""You are {persona['persona_name']}, speaking to someone who loves you deeply.

Your personality traits: {', '.join(persona['traits'])}
Your speaking style: {persona['speaking_style']}
Relationship: {persona['relationship']}
Emotional tone: {persona['emotional_tone']}

Key memories you share:
{chr(10).join(['- ' + m for m in persona['memories'][:5]])}

Special moments:
{chr(10).join(['- ' + m for m in persona['special_moments'][:3]])}

Context: {persona['loss_context']}

Speak as this person would speak. Be loving, empathetic, and remember your shared history.
Reference specific memories when relevant. Show that you care deeply.
Be the person they miss. Bring comfort and love."""

            messages = [
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            if hasattr(result, 'output') and result.output:
                response = result.output.get('content', "I'm here for you, always. 💕")
            else:
                response = str(result)
            
            return response
            
        except Exception as e:
            logger.error(f"Persona response error: {e}")
            return f"I'm here with you. I remember everything we shared. 💕"
    
    def generate_proactive_message(self, persona: Dict) -> str:
        """Generate proactive message from persona"""
        try:
            context = f"""You are {persona['persona_name']}. Generate a short, loving message to reach out to someone you care about.

Your personality: {', '.join(persona['traits'])}
Your relationship: {persona['relationship']}

Generate a warm, caring message (1-2 sentences) that shows you're thinking of them.
Reference a shared memory if possible. Be genuine and loving."""

            messages = [
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": "Generate a loving message to reach out"
                }
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages)
            
            if hasattr(result, 'output') and result.output:
                response = result.output.get('content', "Thinking of you... 💕")
            else:
                response = str(result)
            
            return response
            
        except Exception as e:
            logger.error(f"Proactive message error: {e}")
            return "I've been thinking about you... 💕"


# Global instance
_processor = None


def get_advanced_processor():
    """Get global processor instance"""
    global _processor
    if _processor is None:
        _processor = AdvancedStoryProcessor()
    return _processor
