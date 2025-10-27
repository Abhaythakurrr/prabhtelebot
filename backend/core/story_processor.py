"""
Story Processor
Extract emotional and contextual information from user stories
"""

import asyncio
import re
from typing import Dict, Any, List
from openai import AsyncOpenAI
import PyPDF2
import io

class StoryProcessor:
    def __init__(self, model_orchestrator, memory_system):
        self.model_orchestrator = model_orchestrator
        self.memory_system = memory_system

    async def process_story(self, story_text: str, user_id: str, companion_name: str = "Prabh") -> Dict[str, Any]:
        """Process user story and extract comprehensive information"""
        try:
            # Clean and preprocess story
            cleaned_story = self._clean_story_text(story_text)
            
            # Extract information using different models
            emotional_analysis = await self._analyze_emotions(cleaned_story)
            personality_traits = await self._extract_personality(cleaned_story, companion_name)
            key_memories = await self._extract_key_memories(cleaned_story)
            relationship_dynamics = await self._analyze_relationship(cleaned_story)
            story_summary = await self._generate_summary(cleaned_story)
            
            # Compile processed data
            processed_data = {
                "summary": story_summary,
                "emotions": emotional_analysis,
                "personality": personality_traits,
                "memories": key_memories,
                "relationship_dynamics": relationship_dynamics,
                "companion_name": companion_name,
                "word_count": len(cleaned_story.split()),
                "processing_timestamp": asyncio.get_event_loop().time()
            }
            
            # Store in memory system
            await self.memory_system.store_user_story(user_id, story_text, processed_data)
            
            return processed_data
            
        except Exception as e:
            print(f"Story processing error: {e}")
            return self._get_fallback_story_data(companion_name)

    def _clean_story_text(self, story_text: str) -> str:
        """Clean and normalize story text"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', story_text)
        
        # Remove special characters but keep punctuation
        cleaned = re.sub(r'[^\w\s\.,!?;:\'"()-]', ' ', cleaned)
        
        # Normalize punctuation
        cleaned = re.sub(r'\.{2,}', '.', cleaned)
        cleaned = re.sub(r'\?{2,}', '?', cleaned)
        cleaned = re.sub(r'!{2,}', '!', cleaned)
        
        return cleaned.strip()

    async def _analyze_emotions(self, story_text: str) -> List[str]:
        """Analyze emotional themes using keyword matching"""
        return self._fallback_emotion_analysis(story_text)

    async def _extract_personality(self, story_text: str, companion_name: str) -> List[str]:
        """Extract personality traits using keyword analysis"""
        story_lower = story_text.lower()
        traits = []
        
        trait_keywords = {
            "romantic": ["love", "romance", "romantic", "kiss", "heart"],
            "caring": ["care", "help", "support", "comfort", "kind"],
            "understanding": ["understand", "listen", "patient", "empathy"],
            "playful": ["fun", "laugh", "joke", "play", "tease"],
            "supportive": ["support", "encourage", "help", "stand by"],
            "passionate": ["passion", "intense", "fire", "desire"],
            "gentle": ["gentle", "soft", "tender", "sweet"],
            "confident": ["confident", "strong", "bold", "sure"],
            "humorous": ["funny", "humor", "laugh", "joke"],
            "loyal": ["loyal", "faithful", "devoted", "committed"],
            "protective": ["protect", "safe", "secure", "guard"],
            "affectionate": ["affection", "cuddle", "hug", "warm"]
        }
        
        for trait, keywords in trait_keywords.items():
            if any(keyword in story_lower for keyword in keywords):
                traits.append(trait)
        
        # Default traits if none found
        if not traits:
            traits = ["romantic", "caring", "understanding", "supportive"]
            
        return traits[:6]

    async def _extract_key_memories(self, story_text: str) -> List[Dict[str, str]]:
        """Extract key memories using sentence analysis"""
        sentences = re.split(r'[.!?]+', story_text)
        processed_sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        memory_keywords = ['first', 'met', 'date', 'kiss', 'together', 'special', 'remember', 'moment', 'time', 'day']
        memories = []
        
        for i, sentence in enumerate(processed_sentences[:20]):  # Check first 20 sentences
            if any(keyword in sentence.lower() for keyword in memory_keywords):
                memories.append({
                    "id": f"memory_{len(memories)+1}",
                    "description": sentence[:150],
                    "importance": "high" if len(memories) < 3 else "medium"
                })
                
                if len(memories) >= 8:
                    break
        
        return memories if memories else self._fallback_memories()

    async def _analyze_relationship(self, story_text: str) -> Dict[str, Any]:
        """Analyze relationship dynamics using Dolphin"""
        try:
            client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key="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"
            )
            
            prompt = f"""Analyze the relationship dynamics in this story. Focus on communication style, intimacy level, and relationship stage.

            Story: {story_text[:1000]}
            
            Return in this format:
            Communication: [casual/formal/intimate/playful]
            Intimacy: [low/medium/high]
            Stage: [dating/committed/married/complicated]
            Duration: [new/months/years/long-term]"""
            
            response = await client.chat.completions.create(
                model="cognitivecomputations/dolphin3.0-mistral-24b:free",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse the response
            dynamics = {
                "communication_style": "intimate",
                "intimacy_level": "medium",
                "relationship_stage": "committed",
                "duration": "long-term"
            }
            
            for line in analysis_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip().lower()
                    
                    if key in dynamics:
                        dynamics[key] = value
            
            return dynamics
            
        except Exception as e:
            print(f"Relationship analysis error: {e}")
            return {
                "communication_style": "intimate",
                "intimacy_level": "medium",
                "relationship_stage": "committed",
                "duration": "long-term"
            }

    async def _generate_summary(self, story_text: str) -> str:
        """Generate summary using text analysis"""
        # Extract first few sentences as summary
        sentences = re.split(r'[.!?]+', story_text)
        meaningful_sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 30]
        
        if len(meaningful_sentences) >= 3:
            summary = '. '.join(meaningful_sentences[:3]) + '.'
        elif len(meaningful_sentences) >= 1:
            summary = '. '.join(meaningful_sentences) + '.'
        else:
            summary = story_text[:200] + '...' if len(story_text) > 200 else story_text
            
        return summary[:300]

    def _fallback_emotion_analysis(self, story_text: str) -> List[str]:
        """Fallback emotion analysis using keyword matching"""
        emotion_keywords = {
            "love": ["love", "adore", "cherish", "heart", "beloved"],
            "happiness": ["happy", "joy", "smile", "laugh", "cheerful"],
            "sadness": ["sad", "cry", "tears", "hurt", "pain"],
            "nostalgia": ["remember", "memory", "past", "miss", "used to"],
            "passion": ["passion", "desire", "intense", "fire", "burning"],
            "romance": ["romantic", "kiss", "embrace", "tender", "sweet"]
        }
        
        story_lower = story_text.lower()
        detected_emotions = []
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in story_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions[:5] if detected_emotions else ["love", "happiness"]

    def _fallback_memories(self) -> List[Dict[str, str]]:
        """Fallback memories when extraction fails"""
        return [
            {"id": "memory_1", "description": "First meeting and connection", "importance": "high"},
            {"id": "memory_2", "description": "Special moments together", "importance": "high"},
            {"id": "memory_3", "description": "Shared experiences and growth", "importance": "medium"}
        ]

    def _get_fallback_story_data(self, companion_name: str) -> Dict[str, Any]:
        """Fallback story data when processing fails"""
        return {
            "summary": "A beautiful love story filled with emotions and memories.",
            "emotions": ["love", "happiness", "romance"],
            "personality": ["romantic", "caring", "understanding"],
            "memories": self._fallback_memories(),
            "relationship_dynamics": {
                "communication_style": "intimate",
                "intimacy_level": "medium",
                "relationship_stage": "committed",
                "duration": "long-term"
            },
            "companion_name": companion_name,
            "word_count": 0,
            "processing_timestamp": asyncio.get_event_loop().time()
        }

    async def process_pdf_story(self, pdf_data: bytes, user_id: str, companion_name: str = "Prabh") -> Dict[str, Any]:
        """Process story from PDF file"""
        try:
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
            story_text = ""
            
            for page in pdf_reader.pages:
                story_text += page.extract_text() + "\n"
            
            # Process the extracted text
            return await self.process_story(story_text, user_id, companion_name)
            
        except Exception as e:
            print(f"PDF processing error: {e}")
            return self._get_fallback_story_data(companion_name)