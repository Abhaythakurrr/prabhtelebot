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
    
    def analyze_story(self, story_text: str) -> Dict[str, Any]:
        """Analyze story and return structured data"""
        try:
            logger.info(f"📚 Analyzing story...")
            
            # Extract characters
            characters = self.extract_characters(story_text)
            
            # Extract themes
            themes = self.extract_themes(story_text)
            
            # Extract emotions
            emotions = self.extract_emotions(story_text)
            
            # Determine setting
            setting = self._extract_setting(story_text)
            
            result = {
                "text": story_text[:500],  # Store first 500 chars
                "characters": characters,
                "themes": themes,
                "emotions": emotions,
                "setting": setting,
                "plot": story_text[:200]  # First 200 chars as plot summary
            }
            
            logger.info(f"✅ Story analyzed: {len(characters)} characters, {len(themes)} themes")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Story analysis failed: {e}")
            return {
                "text": story_text[:500],
                "characters": [],
                "themes": ["general"],
                "emotions": ["neutral"],
                "setting": "Unknown",
                "plot": story_text[:200]
            }
    
    def _extract_setting(self, text: str) -> str:
        """Extract setting from story"""
        text_lower = text.lower()
        
        settings = {
            "Fantasy": ["magic", "dragon", "wizard", "kingdom", "castle"],
            "Sci-Fi": ["space", "robot", "future", "alien", "technology"],
            "Modern": ["city", "office", "apartment", "car", "phone"],
            "Historical": ["ancient", "medieval", "war", "empire", "century"],
            "Romance": ["love", "heart", "kiss", "date", "relationship"]
        }
        
        for setting, keywords in settings.items():
            if any(keyword in text_lower for keyword in keywords):
                return setting
        
        return "General"
    
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
