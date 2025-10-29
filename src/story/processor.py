"""
Story Processor - Extract and analyze user stories
"""

import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class StoryProcessor:
    """Process and analyze user stories"""
    
    def __init__(self):
        self.stories = {}
    
    def process_story(self, user_id: str, story_text: str) -> Dict[str, Any]:
        """Process uploaded story"""
        try:
            logger.info(f"📚 Processing story for user {user_id}")
            
            # Extract characters
            characters = self.extract_characters(story_text)
            
            # Extract themes
            themes = self.extract_themes(story_text)
            
            # Extract emotions
            emotions = self.extract_emotions(story_text)
            
            # Store story
            self.stories[user_id] = {
                "text": story_text,
                "characters": characters,
                "themes": themes,
                "emotions": emotions,
                "processed_at": str(logging.time())
            }
            
            logger.info(f"✅ Story processed: {len(characters)} characters, {len(themes)} themes")
            
            return {
                "success": True,
                "characters": characters,
                "themes": themes,
                "emotions": emotions
            }
            
        except Exception as e:
            logger.error(f"❌ Story processing failed: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_characters(self, text: str) -> List[str]:
        """Extract character names from story"""
        # Simple extraction - find capitalized words
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        # Get unique names
        characters = list(set(words))[:10]  # Limit to 10
        return characters
    
    def extract_themes(self, text: str) -> List[str]:
        """Extract themes from story"""
        themes = []
        text_lower = text.lower()
        
        theme_keywords = {
            "love": ["love", "romance", "heart", "affection"],
            "adventure": ["adventure", "journey", "travel", "explore"],
            "mystery": ["mystery", "secret", "hidden", "unknown"],
            "friendship": ["friend", "companion", "together", "bond"],
            "passion": ["passion", "desire", "intense", "fire"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def extract_emotions(self, text: str) -> List[str]:
        """Extract emotions from story"""
        emotions = []
        text_lower = text.lower()
        
        emotion_keywords = {
            "happy": ["happy", "joy", "smile", "laugh"],
            "sad": ["sad", "cry", "tear", "sorrow"],
            "excited": ["excited", "thrill", "eager", "enthusiastic"],
            "romantic": ["romantic", "intimate", "tender", "loving"],
            "nostalgic": ["memory", "remember", "past", "nostalgia"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotions.append(emotion)
        
        return emotions
    
    def get_story_context(self, user_id: str) -> Dict[str, Any]:
        """Get story context for user"""
        return self.stories.get(user_id, {})


# Global instance
_processor = None


def get_story_processor() -> StoryProcessor:
    """Get global story processor"""
    global _processor
    if _processor is None:
        _processor = StoryProcessor()
    return _processor
