"""
Story Processor - Advanced story analysis and roleplay generation
"""

import logging
import re
import json
from typing import Dict, List, Any
from src.core.config import get_config

logger = logging.getLogger(__name__)

class StoryProcessor:
    """Processes user stories and generates roleplay scenarios"""
    
    def __init__(self):
        self.config = get_config()
    
    async def process_document(self, file, filename: str) -> Dict[str, Any]:
        """Process uploaded document and extract story content"""
        try:
            # Download file content
            file_content = await file.download_as_bytearray()
            
            # Extract text based on file type
            if filename.endswith('.txt'):
                text = file_content.decode('utf-8')
            elif filename.endswith('.docx'):
                # For production, you'd use python-docx
                text = file_content.decode('utf-8', errors='ignore')
            elif filename.endswith('.pdf'):
                # For production, you'd use PyPDF2
                text = file_content.decode('utf-8', errors='ignore')
            else:
                raise ValueError("Unsupported file type")
            
            return {
                "story_text": text,
                "filename": filename,
                "word_count": len(text.split()),
                "character_count": len(text)
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise
    
    async def analyze_story(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze story content and extract key information"""
        try:
            text = story_data.get("story_text", "")
            
            # Extract characters (names in the story)
            characters = self.extract_characters(text)
            
            # Identify themes
            themes = self.identify_themes(text)
            
            # Analyze emotional tone
            emotional_tone = self.analyze_emotional_tone(text)
            
            # Extract relationships
            relationships = self.extract_relationships(text)
            
            # Identify settings/locations
            settings = self.extract_settings(text)
            
            return {
                "characters": characters,
                "themes": themes,
                "emotional_tone": emotional_tone,
                "relationships": relationships,
                "settings": settings,
                "word_count": story_data.get("word_count", 0),
                "analysis_complete": True
            }
            
        except Exception as e:
            logger.error(f"Error analyzing story: {e}")
            return {"error": str(e)}
    
    def extract_characters(self, text: str) -> List[str]:
        """Extract character names from story text"""
        # Simple name extraction - look for capitalized words
        words = text.split()
        potential_names = []
        
        for word in words:
            # Look for capitalized words that could be names
            if (word.isalpha() and word[0].isupper() and len(word) > 2 and 
                word not in ['The', 'And', 'But', 'Or', 'So', 'Then', 'When', 'Where', 'Why', 'How']):
                if word not in potential_names:
                    potential_names.append(word)
        
        # Return top 10 most likely names
        return potential_names[:10]
    
    def identify_themes(self, text: str) -> List[str]:
        """Identify themes in the story"""
        text_lower = text.lower()
        
        theme_keywords = {
            "romance": ["love", "kiss", "heart", "romantic", "date", "relationship", "boyfriend", "girlfriend"],
            "adventure": ["journey", "travel", "explore", "adventure", "quest", "discover"],
            "mystery": ["mystery", "secret", "hidden", "clue", "investigate", "solve"],
            "drama": ["conflict", "argument", "tension", "drama", "emotional", "crisis"],
            "friendship": ["friend", "friendship", "buddy", "companion", "together"],
            "family": ["family", "mother", "father", "sister", "brother", "parent"],
            "career": ["work", "job", "career", "office", "business", "professional"],
            "fantasy": ["magic", "fantasy", "supernatural", "mystical", "enchanted"],
            "adult": ["intimate", "passion", "desire", "sensual", "adult", "mature"]
        }
        
        identified_themes = []
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                identified_themes.append(theme)
        
        return identified_themes[:5]  # Return top 5 themes
    
    def analyze_emotional_tone(self, text: str) -> str:
        """Analyze the emotional tone of the story"""
        text_lower = text.lower()
        
        positive_words = ["happy", "joy", "love", "excited", "wonderful", "amazing", "great", "beautiful"]
        negative_words = ["sad", "angry", "hurt", "pain", "terrible", "awful", "hate", "depressed"]
        romantic_words = ["romantic", "passionate", "intimate", "loving", "tender", "sweet"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        romantic_count = sum(1 for word in romantic_words if word in text_lower)
        
        if romantic_count > max(positive_count, negative_count):
            return "Romantic"
        elif positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Emotional/Drama"
        else:
            return "Neutral"
    
    def extract_relationships(self, text: str) -> List[Dict[str, str]]:
        """Extract relationships between characters"""
        # Simple relationship extraction
        relationship_patterns = [
            r"(\w+) and (\w+) are (.*?)(?:\.|,|\n)",
            r"(\w+) loves (\w+)",
            r"(\w+) is (\w+)'s (.*?)(?:\.|,|\n)"
        ]
        
        relationships = []
        for pattern in relationship_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:5]:  # Limit to 5 relationships
                if len(match) >= 2:
                    relationships.append({
                        "person1": match[0],
                        "person2": match[1],
                        "relationship": match[2] if len(match) > 2 else "connected"
                    })
        
        return relationships
    
    def extract_settings(self, text: str) -> List[str]:
        """Extract settings/locations from the story"""
        # Look for location indicators
        location_patterns = [
            r"in (\w+)",
            r"at (\w+)",
            r"to (\w+)",
            r"from (\w+)"
        ]
        
        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) > 3 and match.lower() not in ['the', 'and', 'but', 'that', 'this']:
                    if match not in locations:
                        locations.append(match)
        
        return locations[:8]  # Return top 8 locations
    
    async def generate_roleplay_scenarios(self, story_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate roleplay scenarios based on story analysis"""
        try:
            analysis = await self.analyze_story(story_data)
            
            scenarios = []
            
            # Generate scenarios based on themes
            themes = analysis.get("themes", [])
            characters = analysis.get("characters", [])
            settings = analysis.get("settings", [])
            
            # Romance scenario
            if "romance" in themes:
                scenarios.append({
                    "title": "💕 Romantic Evening",
                    "preview": "A intimate dinner date with deep conversation and romantic tension...",
                    "type": "romance",
                    "characters": characters[:2],
                    "setting": settings[0] if settings else "cozy restaurant"
                })
            
            # Adventure scenario
            if "adventure" in themes:
                scenarios.append({
                    "title": "🗺️ Epic Adventure",
                    "preview": "An exciting journey filled with challenges and discoveries...",
                    "type": "adventure",
                    "characters": characters[:3],
                    "setting": settings[1] if len(settings) > 1 else "mysterious forest"
                })
            
            # Drama scenario
            if "drama" in themes:
                scenarios.append({
                    "title": "🎭 Emotional Drama",
                    "preview": "A tense situation that tests relationships and reveals true feelings...",
                    "type": "drama",
                    "characters": characters[:2],
                    "setting": settings[0] if settings else "private room"
                })
            
            # Adult scenario (premium)
            if "adult" in themes:
                scenarios.append({
                    "title": "🔥 Intimate Moments",
                    "preview": "A passionate encounter exploring deeper desires... (Premium Only)",
                    "type": "adult",
                    "characters": characters[:2],
                    "setting": "private space",
                    "premium": True
                })
            
            # Default scenarios if no specific themes
            if not scenarios:
                scenarios = [
                    {
                        "title": "💬 Deep Conversation",
                        "preview": "A meaningful chat that brings you closer together...",
                        "type": "conversation",
                        "characters": ["You", "AI Companion"],
                        "setting": "comfortable space"
                    },
                    {
                        "title": "🎮 Fun Activity",
                        "preview": "Engaging in a fun activity that reveals personality...",
                        "type": "activity",
                        "characters": ["You", "AI Companion"],
                        "setting": "interactive environment"
                    }
                ]
            
            return scenarios
            
        except Exception as e:
            logger.error(f"Error generating roleplay scenarios: {e}")
            return [
                {
                    "title": "💬 Getting to Know You",
                    "preview": "Let's have a conversation and learn about each other...",
                    "type": "conversation",
                    "characters": ["You", "AI Companion"],
                    "setting": "chat space"
                }
            ]
    
    def generate_roleplay_scenarios_sync(self, story_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sync version of roleplay scenario generation"""
        try:
            # Simple sync analysis
            story_text = story_data.get("story_text", "").lower()
            
            scenarios = []
            
            # Check for themes in story
            if any(word in story_text for word in ["love", "romantic", "heart", "kiss"]):
                scenarios.append({
                    "title": "💕 Romantic Evening",
                    "preview": "A intimate dinner date with deep conversation and romantic tension...",
                    "type": "romance"
                })
            
            if any(word in story_text for word in ["adventure", "journey", "travel", "explore"]):
                scenarios.append({
                    "title": "🗺️ Epic Adventure",
                    "preview": "An exciting journey filled with challenges and discoveries...",
                    "type": "adventure"
                })
            
            if any(word in story_text for word in ["drama", "conflict", "emotional", "tension"]):
                scenarios.append({
                    "title": "🎭 Emotional Drama",
                    "preview": "A tense situation that tests relationships and reveals true feelings...",
                    "type": "drama"
                })
            
            # Adult scenario (premium)
            if any(word in story_text for word in ["intimate", "passion", "desire", "adult"]):
                scenarios.append({
                    "title": "🔥 Intimate Moments",
                    "preview": "A passionate encounter exploring deeper desires... (Premium Only)",
                    "type": "adult",
                    "premium": True
                })
            
            # Default scenarios if no specific themes
            if not scenarios:
                scenarios = [
                    {
                        "title": "💬 Deep Conversation",
                        "preview": "A meaningful chat that brings you closer together...",
                        "type": "conversation"
                    },
                    {
                        "title": "🎮 Fun Activity",
                        "preview": "Engaging in a fun activity that reveals personality...",
                        "type": "activity"
                    }
                ]
            
            return scenarios
            
        except Exception as e:
            logger.error(f"Error generating sync roleplay scenarios: {e}")
            return [
                {
                    "title": "💬 Getting to Know You",
                    "preview": "Let's have a conversation and learn about each other...",
                    "type": "conversation"
                }
            ]