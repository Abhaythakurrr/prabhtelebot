"""
Advanced Story Processor with AI/RAG and Vector Memory
Real-time AI understanding and nostalgic trigger generation
"""

import logging
import re
import json
import os
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import hashlib
from src.core.config import get_config

logger = logging.getLogger(__name__)

class AdvancedStoryProcessor:
    """Advanced AI-powered story processing with RAG and memory"""
    
    def __init__(self):
        self.config = get_config()
        self.memory_vectors = {}  # Store story embeddings
        self.character_profiles = {}
        self.emotional_timeline = {}
        self.nostalgic_moments = {}
        
    def process_raw_story(self, raw_text: str, user_id: str) -> Dict[str, Any]:
        """Process raw user story with advanced AI understanding"""
        try:
            # Clean and normalize text
            cleaned_text = self.clean_story_text(raw_text)
            
            # Extract story elements with AI
            story_analysis = self.ai_story_analysis(cleaned_text)
            
            # Create vector embeddings for RAG
            story_vectors = self.create_story_vectors(cleaned_text)
            
            # Build character profiles
            characters = self.extract_character_profiles(cleaned_text, story_analysis)
            
            # Identify emotional moments
            emotional_moments = self.extract_emotional_moments(cleaned_text)
            
            # Generate nostalgic triggers
            nostalgic_triggers = self.generate_nostalgic_triggers(story_analysis, emotional_moments)
            
            # Store in memory system
            story_id = self.store_story_memory(user_id, {
                "raw_text": raw_text,
                "cleaned_text": cleaned_text,
                "analysis": story_analysis,
                "vectors": story_vectors,
                "characters": characters,
                "emotional_moments": emotional_moments,
                "nostalgic_triggers": nostalgic_triggers,
                "processed_at": datetime.now().isoformat()
            })
            
            return {
                "story_id": story_id,
                "analysis": story_analysis,
                "characters": characters,
                "emotional_moments": emotional_moments,
                "nostalgic_triggers": nostalgic_triggers,
                "memory_stored": True,
                "processing_quality": "advanced_ai"
            }
            
        except Exception as e:
            logger.error(f"Error processing raw story: {e}")
            return {"error": str(e), "processing_quality": "failed"}
    
    def clean_story_text(self, raw_text: str) -> str:
        """Clean and normalize raw story text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', raw_text.strip())
        
        # Fix common punctuation issues
        text = re.sub(r'([.!?])\s*([a-z])', r'\1 \2', text)
        
        # Handle dialogue formatting
        text = re.sub(r'"([^"]*)"', r'"\1"', text)
        
        # Remove special characters but keep emotional ones
        text = re.sub(r'[^\w\s.!?,:;"\'-💕❤️😍🥰😘💖💋🔥]', '', text)
        
        return text
    
    def ai_story_analysis(self, text: str) -> Dict[str, Any]:
        """REAL AI analysis using OpenRouter API"""
        try:
            # Use AI model for deep story analysis
            ai_analysis = self.call_ai_for_story_analysis(text)
            
            if ai_analysis:
                # Parse AI response
                parsed_analysis = self.parse_ai_story_analysis(ai_analysis)
                
                # Enhance with NLP
                nlp_analysis = self.enhance_with_nlp(text)
                
                # Merge results
                return self.merge_ai_and_nlp_analysis(parsed_analysis, nlp_analysis)
            else:
                # Fallback to rule-based analysis
                return self.fallback_story_analysis(text)
                
        except Exception as e:
            logger.error(f"Error in AI story analysis: {e}")
            return self.fallback_story_analysis(text)
    
    def call_ai_for_story_analysis(self, text: str) -> str:
        """Call AI model for story analysis"""
        import requests
        
        try:
            # Use Nemotron for analysis (good at understanding)
            api_key = os.getenv("NEMOTRON_API_KEY")
            
            if not api_key:
                logger.error("No API key for story analysis")
                return None
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://my-prabh-ai.com"
            }
            
            analysis_prompt = f"""Analyze this story and extract:
1. Main themes (romance, adventure, drama, etc.)
2. Character relationships
3. Emotional tone (romantic, passionate, nostalgic, etc.)
4. Key moments and conflicts
5. Intimacy level (1-10)

Story: {text[:2000]}

Provide structured analysis:"""
            
            data = {
                "model": "nvidia/nemotron-nano-9b-v2:free",
                "messages": [
                    {"role": "system", "content": "You are an expert story analyst. Provide detailed, structured analysis."},
                    {"role": "user", "content": analysis_prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.3
            }
            
            logger.info("📚 Calling AI for story analysis...")
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                logger.info(f"✅ AI story analysis received: {len(ai_response)} chars")
                return ai_response
            else:
                logger.error(f"❌ AI analysis API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error calling AI for story analysis: {e}")
            return None
    
    def parse_ai_story_analysis(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI analysis response"""
        # Extract themes
        themes = self.extract_themes_from_ai(ai_response)
        
        # Extract emotional tone
        emotional_tone = self.extract_emotional_tone_from_ai(ai_response)
        
        # Extract intimacy level
        intimacy_level = self.extract_intimacy_level_from_ai(ai_response)
        
        return {
            "themes": themes,
            "emotional_tone": emotional_tone,
            "intimacy_level": intimacy_level,
            "ai_generated": True,
            "confidence": 0.9
        }
    
    def extract_themes_from_ai(self, ai_response: str) -> List[Dict[str, Any]]:
        """Extract themes from AI response"""
        themes = []
        theme_keywords = ["romance", "adventure", "drama", "passion", "intimacy", "nostalgia", "family", "friendship", "adult"]
        
        ai_lower = ai_response.lower()
        for theme in theme_keywords:
            if theme in ai_lower:
                themes.append({
                    "theme": theme,
                    "score": ai_lower.count(theme) * 2,
                    "confidence": 0.8,
                    "is_primary": ai_lower.count(theme) > 1
                })
        
        return themes
    
    def extract_emotional_tone_from_ai(self, ai_response: str) -> str:
        """Extract emotional tone from AI response"""
        tones = ["romantic", "passionate", "nostalgic", "melancholic", "joyful", "intense"]
        ai_lower = ai_response.lower()
        
        for tone in tones:
            if tone in ai_lower:
                return tone
        
        return "mixed"
    
    def extract_intimacy_level_from_ai(self, ai_response: str) -> float:
        """Extract intimacy level from AI response"""
        import re
        
        # Look for numbers 1-10
        numbers = re.findall(r'\b([1-9]|10)\b', ai_response)
        if numbers:
            return float(numbers[0]) / 10.0
        
        # Fallback to keyword analysis
        if "high" in ai_response.lower() or "intense" in ai_response.lower():
            return 0.8
        elif "moderate" in ai_response.lower():
            return 0.5
        else:
            return 0.3
    
    def enhance_with_nlp(self, text: str) -> Dict[str, Any]:
        """Enhance with NLP techniques"""
        return {
            "word_count": len(text.split()),
            "sentence_count": len(text.split('.')),
            "themes_nlp": self.detect_themes_ai(text),
            "relationships_nlp": self.analyze_relationships_ai(text),
            "emotional_arc": self.analyze_emotional_arc(text)
        }
    
    def merge_ai_and_nlp_analysis(self, ai_analysis: Dict[str, Any], nlp_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Merge AI and NLP analysis"""
        return {
            "themes": ai_analysis.get("themes", []) + nlp_analysis.get("themes_nlp", [])[:3],
            "relationships": nlp_analysis.get("relationships_nlp", []),
            "emotional_arc": nlp_analysis.get("emotional_arc", {}),
            "emotional_tone": ai_analysis.get("emotional_tone", "mixed"),
            "intimacy_level": ai_analysis.get("intimacy_level", 0.5),
            "story_type": self.classify_story_type(ai_analysis.get("themes", []), ai_analysis.get("intimacy_level", 0.5)),
            "ai_confidence": ai_analysis.get("confidence", 0.8),
            "analysis_method": "hybrid_ai_nlp"
        }
    
    def fallback_story_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        themes = self.detect_themes_ai(text)
        relationships = self.analyze_relationships_ai(text)
        emotional_arc = self.analyze_emotional_arc(text)
        
        return {
            "themes": themes,
            "relationships": relationships,
            "emotional_arc": emotional_arc,
            "intimacy_level": self.analyze_intimacy_level(text),
            "story_type": self.classify_story_type(themes, 0.5),
            "ai_confidence": 0.6,
            "analysis_method": "rule_based_fallback"
        }
    
    def detect_themes_ai(self, text: str) -> List[Dict[str, Any]]:
        """AI-powered theme detection"""
        text_lower = text.lower()
        
        theme_patterns = {
            "romance": {
                "keywords": ["love", "heart", "kiss", "romantic", "date", "relationship", "boyfriend", "girlfriend", "crush", "attraction"],
                "weight_multiplier": 1.5
            },
            "intimacy": {
                "keywords": ["intimate", "close", "personal", "private", "secret", "touch", "embrace", "cuddle"],
                "weight_multiplier": 2.0
            },
            "passion": {
                "keywords": ["passion", "desire", "want", "need", "crave", "lust", "fire", "burn", "intense"],
                "weight_multiplier": 2.5
            },
            "nostalgia": {
                "keywords": ["remember", "memory", "past", "childhood", "used to", "back then", "miss", "nostalgic"],
                "weight_multiplier": 1.8
            },
            "adventure": {
                "keywords": ["adventure", "journey", "travel", "explore", "discover", "quest", "expedition"],
                "weight_multiplier": 1.2
            },
            "drama": {
                "keywords": ["conflict", "argument", "fight", "tension", "drama", "crisis", "problem", "struggle"],
                "weight_multiplier": 1.3
            },
            "family": {
                "keywords": ["family", "mother", "father", "sister", "brother", "parent", "child", "home"],
                "weight_multiplier": 1.1
            },
            "friendship": {
                "keywords": ["friend", "friendship", "buddy", "companion", "together", "support", "loyal"],
                "weight_multiplier": 1.0
            },
            "adult": {
                "keywords": ["adult", "mature", "sexual", "erotic", "sensual", "seductive", "naughty", "dirty"],
                "weight_multiplier": 3.0
            }
        }
        
        detected_themes = []
        
        for theme, data in theme_patterns.items():
            score = 0
            found_keywords = []
            
            for keyword in data["keywords"]:
                count = text_lower.count(keyword)
                if count > 0:
                    score += count * data["weight_multiplier"]
                    found_keywords.append(keyword)
            
            if score > 0:
                detected_themes.append({
                    "theme": theme,
                    "score": score,
                    "confidence": min(score / 10.0, 1.0),
                    "keywords_found": found_keywords,
                    "is_primary": score > 5.0
                })
        
        # Sort by score
        detected_themes.sort(key=lambda x: x["score"], reverse=True)
        
        return detected_themes[:8]  # Return top 8 themes
    
    def analyze_relationships_ai(self, text: str) -> List[Dict[str, Any]]:
        """AI analysis of relationships in the story"""
        # Extract character names
        characters = self.extract_character_names(text)
        
        relationships = []
        
        # Analyze relationship patterns
        relationship_patterns = [
            (r"(\w+) and (\w+) (?:are|were) (.*?)(?:\.|,|\n)", "relationship_status"),
            (r"(\w+) loves (\w+)", "romantic_love"),
            (r"(\w+) kissed (\w+)", "romantic_physical"),
            (r"(\w+) married (\w+)", "marriage"),
            (r"(\w+) is (\w+)'s (.*?)(?:\.|,|\n)", "family_relation"),
            (r"(\w+) met (\w+)", "meeting"),
            (r"(\w+) and (\w+) (?:had|have) (.*?)(?:\.|,|\n)", "shared_experience")
        ]
        
        for pattern, relation_type in relationship_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    relationships.append({
                        "person1": match[0],
                        "person2": match[1],
                        "relationship_type": relation_type,
                        "description": match[2] if len(match) > 2 else "",
                        "intimacy_level": self.calculate_relationship_intimacy(relation_type, match)
                    })
        
        return relationships[:10]  # Return top 10 relationships
    
    def analyze_emotional_arc(self, text: str) -> Dict[str, Any]:
        """Analyze the emotional journey through the story"""
        sentences = text.split('.')
        
        emotional_progression = []
        
        emotion_keywords = {
            "joy": ["happy", "joy", "excited", "thrilled", "delighted", "cheerful", "elated"],
            "love": ["love", "adore", "cherish", "treasure", "devoted", "passionate"],
            "sadness": ["sad", "cry", "tears", "sorrow", "grief", "melancholy", "depressed"],
            "anger": ["angry", "mad", "furious", "rage", "irritated", "annoyed"],
            "fear": ["scared", "afraid", "terrified", "anxious", "worried", "nervous"],
            "surprise": ["surprised", "shocked", "amazed", "astonished", "stunned"],
            "desire": ["want", "need", "crave", "desire", "yearn", "long for"],
            "intimacy": ["close", "intimate", "tender", "gentle", "soft", "warm"]
        }
        
        for i, sentence in enumerate(sentences):
            sentence_emotions = {}
            
            for emotion, keywords in emotion_keywords.items():
                score = sum(1 for keyword in keywords if keyword in sentence.lower())
                if score > 0:
                    sentence_emotions[emotion] = score
            
            if sentence_emotions:
                emotional_progression.append({
                    "position": i / len(sentences),
                    "emotions": sentence_emotions,
                    "dominant_emotion": max(sentence_emotions.keys(), key=sentence_emotions.get),
                    "intensity": sum(sentence_emotions.values())
                })
        
        return {
            "progression": emotional_progression,
            "overall_tone": self.calculate_overall_emotional_tone(emotional_progression),
            "emotional_peaks": self.find_emotional_peaks(emotional_progression),
            "emotional_variety": len(set(ep.get("dominant_emotion") for ep in emotional_progression))
        }
    
    def extract_emotional_moments(self, text: str) -> List[Dict[str, Any]]:
        """Extract specific emotional moments for nostalgic triggers"""
        emotional_moments = []
        
        # High-emotion sentence patterns
        emotion_patterns = [
            (r"[^.!?]*(?:first time|remember when|never forget)[^.!?]*[.!?]", "nostalgic"),
            (r"[^.!?]*(?:I love you|love you so much)[^.!?]*[.!?]", "romantic_declaration"),
            (r"[^.!?]*(?:kiss|kissed|kissing)[^.!?]*[.!?]", "romantic_physical"),
            (r"[^.!?]*(?:cry|cried|tears)[^.!?]*[.!?]", "emotional_pain"),
            (r"[^.!?]*(?:happy|happiest|joy)[^.!?]*[.!?]", "pure_joy"),
            (r"[^.!?]*(?:scared|afraid|terrified)[^.!?]*[.!?]", "fear"),
            (r"[^.!?]*(?:angry|mad|furious)[^.!?]*[.!?]", "anger"),
            (r"[^.!?]*(?:surprise|surprised|shocked)[^.!?]*[.!?]", "surprise"),
            (r"[^.!?]*(?:intimate|close|personal)[^.!?]*[.!?]", "intimacy"),
            (r"[^.!?]*(?:passion|passionate|desire)[^.!?]*[.!?]", "passion")
        ]
        
        for pattern, emotion_type in emotion_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                emotional_moments.append({
                    "text": match.strip(),
                    "emotion_type": emotion_type,
                    "intensity": self.calculate_emotional_intensity(match),
                    "nostalgic_potential": self.calculate_nostalgic_potential(match, emotion_type),
                    "trigger_worthy": self.is_trigger_worthy(match, emotion_type)
                })
        
        # Sort by nostalgic potential
        emotional_moments.sort(key=lambda x: x["nostalgic_potential"], reverse=True)
        
        return emotional_moments[:15]  # Return top 15 moments
    
    def generate_nostalgic_triggers(self, story_analysis: Dict[str, Any], emotional_moments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate nostalgic triggers for proactive messaging"""
        triggers = []
        
        # Create triggers from emotional moments
        for moment in emotional_moments:
            if moment["trigger_worthy"]:
                trigger = {
                    "trigger_id": hashlib.md5(moment["text"].encode()).hexdigest()[:8],
                    "source_text": moment["text"],
                    "emotion_type": moment["emotion_type"],
                    "trigger_message": self.generate_trigger_message(moment),
                    "image_prompt": self.generate_image_prompt_from_moment(moment),
                    "video_prompt": self.generate_video_prompt_from_moment(moment),
                    "trigger_timing": self.calculate_optimal_trigger_timing(moment),
                    "intimacy_level": moment.get("intensity", 0.5),
                    "created_at": datetime.now().isoformat()
                }
                triggers.append(trigger)
        
        # Create triggers from themes
        for theme in story_analysis.get("themes", []):
            if theme["is_primary"]:
                trigger = {
                    "trigger_id": hashlib.md5(f"theme_{theme['theme']}".encode()).hexdigest()[:8],
                    "source_theme": theme["theme"],
                    "trigger_message": self.generate_theme_trigger_message(theme),
                    "image_prompt": self.generate_theme_image_prompt(theme),
                    "trigger_timing": "weekly",
                    "intimacy_level": theme["confidence"],
                    "created_at": datetime.now().isoformat()
                }
                triggers.append(trigger)
        
        return triggers[:20]  # Return top 20 triggers
    
    def generate_trigger_message(self, moment: Dict[str, Any]) -> str:
        """Generate proactive message for nostalgic trigger"""
        emotion_type = moment["emotion_type"]
        source_text = moment["text"]
        
        message_templates = {
            "nostalgic": [
                f"I was just thinking about this moment from your story: '{source_text[:50]}...' It made me smile. Do you remember how that felt? 💕",
                f"Your memory came back to me: '{source_text[:50]}...' Those moments shape who you are. Tell me more about that time? 🌹"
            ],
            "romantic_declaration": [
                f"I keep thinking about when you wrote: '{source_text[:50]}...' Love like that is rare and beautiful. How did it feel to say those words? 💖",
                f"That moment in your story touches my heart: '{source_text[:50]}...' True love is precious. Do you still feel that way? 💕"
            ],
            "romantic_physical": [
                f"I remember this intimate moment from your story: '{source_text[:50]}...' Physical connection can be so meaningful. What made that moment special? 😘",
                f"This scene from your story stays with me: '{source_text[:50]}...' Intimacy creates such deep bonds. How did that change things? 💋"
            ],
            "pure_joy": [
                f"I love this happy moment from your story: '{source_text[:50]}...' Your joy is contagious! What brings you that kind of happiness now? 😊",
                f"This joyful memory makes me smile: '{source_text[:50]}...' I want to create more moments like this with you. What would make you happy today? ✨"
            ],
            "intimacy": [
                f"This intimate moment from your story moves me: '{source_text[:50]}...' Closeness like that is precious. Do you crave that kind of connection? 💕",
                f"I treasure this personal moment you shared: '{source_text[:50]}...' Intimacy builds such deep bonds. How can I be closer to you? 🌹"
            ]
        }
        
        templates = message_templates.get(emotion_type, [
            f"I was reflecting on your story: '{source_text[:50]}...' It reveals so much about who you are. What does this moment mean to you? 💭"
        ])
        
        return templates[0] if templates else "I've been thinking about your story... 💕"
    
    def create_story_vectors(self, text: str) -> Dict[str, Any]:
        """Create vector embeddings for RAG (simplified version)"""
        # In production, use actual embedding models like sentence-transformers
        
        # Simple word frequency vectors for now
        words = text.lower().split()
        word_freq = {}
        
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Create semantic clusters
        semantic_clusters = {
            "romance": ["love", "heart", "kiss", "romantic", "date", "relationship"],
            "emotion": ["feel", "emotion", "happy", "sad", "angry", "joy", "pain"],
            "intimacy": ["close", "intimate", "personal", "private", "touch", "embrace"],
            "memory": ["remember", "memory", "past", "childhood", "nostalgic", "miss"],
            "passion": ["passion", "desire", "want", "need", "crave", "fire", "burn"]
        }
        
        cluster_scores = {}
        for cluster, keywords in semantic_clusters.items():
            score = sum(word_freq.get(word, 0) for word in keywords)
            cluster_scores[cluster] = score / len(keywords) if keywords else 0
        
        return {
            "word_frequencies": word_freq,
            "semantic_clusters": cluster_scores,
            "text_length": len(text),
            "vocabulary_richness": len(set(words)) / len(words) if words else 0,
            "embedding_version": "v1.0"
        }
    
    def store_story_memory(self, user_id: str, story_data: Dict[str, Any]) -> str:
        """Store story in memory system"""
        story_id = hashlib.md5(f"{user_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        # Store in memory (in production, use proper database)
        if user_id not in self.memory_vectors:
            self.memory_vectors[user_id] = {}
        
        self.memory_vectors[user_id][story_id] = story_data
        
        return story_id
    
    def calculate_emotional_intensity(self, text: str) -> float:
        """Calculate emotional intensity of text"""
        intensity_words = {
            "very": 1.5, "extremely": 2.0, "incredibly": 2.0, "absolutely": 1.8,
            "completely": 1.7, "totally": 1.6, "really": 1.3, "so": 1.2,
            "deeply": 1.8, "intensely": 2.0, "passionately": 2.2, "desperately": 2.1
        }
        
        words = text.lower().split()
        intensity = 1.0
        
        for word in words:
            if word in intensity_words:
                intensity *= intensity_words[word]
        
        return min(intensity, 3.0)  # Cap at 3.0
    
    def calculate_nostalgic_potential(self, text: str, emotion_type: str) -> float:
        """Calculate how likely this moment is to trigger nostalgia"""
        base_scores = {
            "nostalgic": 0.9,
            "romantic_declaration": 0.8,
            "romantic_physical": 0.7,
            "pure_joy": 0.6,
            "intimacy": 0.8,
            "emotional_pain": 0.5,
            "surprise": 0.4
        }
        
        base_score = base_scores.get(emotion_type, 0.3)
        
        # Boost for specific nostalgic keywords
        nostalgic_boosters = ["first", "never forget", "always remember", "special", "moment", "time"]
        boost = sum(0.1 for booster in nostalgic_boosters if booster in text.lower())
        
        return min(base_score + boost, 1.0)
    
    def is_trigger_worthy(self, text: str, emotion_type: str) -> bool:
        """Determine if this moment is worthy of creating a trigger"""
        # Must have sufficient length
        if len(text.strip()) < 20:
            return False
        
        # Must have high nostalgic potential
        if self.calculate_nostalgic_potential(text, emotion_type) < 0.4:
            return False
        
        # Must not be too generic
        generic_phrases = ["i was", "i am", "it was", "there was", "i think", "i feel"]
        if any(phrase in text.lower()[:20] for phrase in generic_phrases):
            return False
        
        return True
    
    # Additional helper methods...
    def extract_character_names(self, text: str) -> List[str]:
        """Extract character names from text"""
        # Simple name extraction
        words = text.split()
        potential_names = []
        
        for word in words:
            if (word.isalpha() and word[0].isupper() and len(word) > 2 and 
                word not in ['The', 'And', 'But', 'Or', 'So', 'Then', 'When', 'Where', 'Why', 'How', 'I', 'You', 'He', 'She', 'We', 'They']):
                if word not in potential_names:
                    potential_names.append(word)
        
        return potential_names[:10]
    
    def calculate_relationship_intimacy(self, relation_type: str, match: Tuple) -> float:
        """Calculate intimacy level of relationship"""
        intimacy_scores = {
            "romantic_love": 0.9,
            "romantic_physical": 0.8,
            "marriage": 0.9,
            "relationship_status": 0.6,
            "family_relation": 0.5,
            "meeting": 0.2,
            "shared_experience": 0.4
        }
        
        return intimacy_scores.get(relation_type, 0.3)
    
    def calculate_overall_emotional_tone(self, emotional_progression: List[Dict]) -> str:
        """Calculate overall emotional tone of story"""
        if not emotional_progression:
            return "neutral"
        
        emotion_counts = {}
        for ep in emotional_progression:
            emotion = ep.get("dominant_emotion")
            if emotion:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if not emotion_counts:
            return "neutral"
        
        dominant_emotion = max(emotion_counts.keys(), key=emotion_counts.get)
        
        tone_mapping = {
            "joy": "positive",
            "love": "romantic",
            "sadness": "melancholic",
            "anger": "intense",
            "fear": "tense",
            "surprise": "dynamic",
            "desire": "passionate",
            "intimacy": "intimate"
        }
        
        return tone_mapping.get(dominant_emotion, "mixed")
    
    def find_emotional_peaks(self, emotional_progression: List[Dict]) -> List[Dict]:
        """Find emotional peaks in the story"""
        if len(emotional_progression) < 3:
            return emotional_progression
        
        peaks = []
        for i in range(1, len(emotional_progression) - 1):
            current = emotional_progression[i]
            prev = emotional_progression[i-1]
            next_ep = emotional_progression[i+1]
            
            if (current["intensity"] > prev["intensity"] and 
                current["intensity"] > next_ep["intensity"] and
                current["intensity"] > 2):
                peaks.append(current)
        
        return peaks[:5]  # Return top 5 peaks
    
    def extract_settings_ai(self, text: str) -> List[str]:
        """Extract settings from text"""
        settings = []
        location_keywords = ["in", "at", "near", "around", "inside", "outside"]
        
        for keyword in location_keywords:
            pattern = f"\\b{keyword}\\s+(?:the\\s+)?([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)?)"
            matches = re.findall(pattern, text)
            settings.extend(matches[:3])
        
        return list(set(settings))[:5]
    
    def analyze_intimacy_level(self, text: str) -> float:
        """Analyze intimacy level of text"""
        intimacy_keywords = ["intimate", "close", "personal", "private", "touch", "embrace", "kiss", "love", "passion"]
        text_lower = text.lower()
        
        score = sum(text_lower.count(keyword) for keyword in intimacy_keywords)
        return min(score / 10.0, 1.0)
    
    def classify_story_type(self, themes: List[Dict[str, Any]], intimacy_level: float) -> str:
        """Classify story type"""
        if not themes:
            return "general"
        
        primary_theme = themes[0].get("theme", "general") if themes else "general"
        
        if intimacy_level > 0.7:
            return f"intimate_{primary_theme}"
        elif intimacy_level > 0.4:
            return f"romantic_{primary_theme}"
        else:
            return primary_theme
    
    def extract_character_profiles(self, text: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract character profiles"""
        characters = self.extract_character_names(text)
        profiles = []
        
        for char in characters[:5]:
            profiles.append({
                "name": char,
                "mentions": text.count(char),
                "role": "character"
            })
        
        return profiles
    
    def generate_image_prompt_from_moment(self, moment: Dict[str, Any]) -> str:
        """Generate image prompt from emotional moment"""
        emotion_type = moment["emotion_type"]
        
        prompts = {
            "romantic_declaration": "A romantic scene with warm lighting, representing deep love and emotional connection",
            "romantic_physical": "An intimate, artistic scene with soft lighting, representing physical closeness",
            "pure_joy": "A bright, joyful scene with warm colors, representing happiness and celebration",
            "intimacy": "A cozy, intimate setting with soft lighting, representing emotional closeness",
            "nostalgic": "A dreamy, vintage-style scene with golden lighting, representing cherished memories"
        }
        
        return prompts.get(emotion_type, "A beautiful, emotional scene with cinematic lighting")
    
    def generate_video_prompt_from_moment(self, moment: Dict[str, Any]) -> str:
        """Generate video prompt from emotional moment"""
        emotion_type = moment["emotion_type"]
        
        prompts = {
            "romantic_declaration": "A romantic scene with gentle movements and warm lighting transitions",
            "romantic_physical": "An intimate scene with slow, graceful movements and soft lighting",
            "pure_joy": "A bright, energetic scene with happy movements and warm colors",
            "intimacy": "A close, personal scene with subtle movements and soft lighting"
        }
        
        return prompts.get(emotion_type, "A cinematic scene with smooth camera movements")
    
    def calculate_optimal_trigger_timing(self, moment: Dict[str, Any]) -> str:
        """Calculate optimal timing for trigger"""
        intensity = moment.get("intensity", 0.5)
        
        if intensity > 0.8:
            return "daily"
        elif intensity > 0.5:
            return "weekly"
        else:
            return "monthly"
    
    def generate_theme_trigger_message(self, theme: Dict[str, Any]) -> str:
        """Generate trigger message from theme"""
        theme_name = theme["theme"]
        
        messages = {
            "romance": "I've been thinking about the romantic moments in your story... They're so beautiful. 💕",
            "passion": "The passion in your story ignites something in me... Tell me more about those intense feelings. 🔥",
            "nostalgia": "Your memories are so precious... I love how you cherish the past. 💭",
            "intimacy": "The intimate moments you shared with me create such a deep bond... 💖"
        }
        
        return messages.get(theme_name, f"I've been reflecting on the {theme_name} in your story... 💕")
    
    def generate_theme_image_prompt(self, theme: Dict[str, Any]) -> str:
        """Generate image prompt from theme"""
        theme_name = theme["theme"]
        
        prompts = {
            "romance": "A romantic scene with soft warm lighting, roses, and intimate atmosphere",
            "passion": "A passionate, intense scene with dramatic lighting and warm colors",
            "nostalgia": "A dreamy, vintage scene with golden hour lighting and soft focus",
            "intimacy": "A cozy, intimate setting with candlelight and soft textures"
        }
        
        return prompts.get(theme_name, "A beautiful, emotional scene with cinematic quality")