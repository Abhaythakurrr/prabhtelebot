"""
Model Orchestration Layer
Handles dynamic model selection and routing
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
import random
import asyncio

class ModelOrchestrator:
    def __init__(self, config):
        self.config = config
        self.models = {
            "gemini": {
                "name": "google/gemini-2.0-flash-exp:free",
                "key": "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",
                "strengths": ["analysis", "reasoning", "mood_detection"]
            },
            "nemotron": {
                "name": "nvidia/nemotron-nano-9b-v2:free",
                "key": "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",
                "strengths": ["conversation", "emotional_intelligence"]
            },
            "llama33": {
                "name": "meta-llama/llama-3.3-8b-instruct:free",
                "key": "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",
                "strengths": ["general_chat", "storytelling"]
            },
            "llama4": {
                "name": "meta-llama/llama-4-maverick:free",
                "key": "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",
                "strengths": ["vision", "multimodal", "creative"]
            },
            "dolphin": {
                "name": "cognitivecomputations/dolphin3.0-mistral-24b:free",
                "key": "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",
                "strengths": ["intimate", "romantic", "nsfw"]
            }
        }
        
        self.mood_model_mapping = {
            "romantic": ["dolphin", "llama4", "nemotron"],
            "sad": ["nemotron", "llama33"],
            "happy": ["llama33", "nemotron"],
            "angry": ["nemotron", "llama33"],
            "nostalgic": ["llama4", "dolphin"],
            "intimate": ["dolphin", "llama4"],
            "analytical": ["gemini", "llama33"],
            "creative": ["llama4", "dolphin"],
            "default": ["nemotron", "llama33"]
        }

    async def analyze_mood(self, message: str) -> str:
        """Analyze message mood with fallback"""
        # Simple keyword-based mood detection to avoid API calls
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['love', 'miss', 'romantic', 'kiss']):
            return 'romantic'
        elif any(word in message_lower for word in ['sad', 'cry', 'hurt', 'pain']):
            return 'sad'
        elif any(word in message_lower for word in ['happy', 'joy', 'smile', 'great']):
            return 'happy'
        elif any(word in message_lower for word in ['angry', 'mad', 'upset']):
            return 'angry'
        elif any(word in message_lower for word in ['remember', 'memory', 'past']):
            return 'nostalgic'
        elif any(word in message_lower for word in ['intimate', 'close', 'together']):
            return 'intimate'
        elif any(word in message_lower for word in ['why', 'how', 'explain', 'analyze']):
            return 'analytical'
        elif any(word in message_lower for word in ['create', 'imagine', 'story']):
            return 'creative'
        else:
            return 'default'

    def select_model(self, message: str, mood: str) -> str:
        """Select best model based on message and mood"""
        # Get candidate models for the mood
        candidates = self.mood_model_mapping.get(mood, self.mood_model_mapping["default"])
        
        # Additional logic for model selection
        message_lower = message.lower()
        
        # Vision/image requests
        if any(word in message_lower for word in ["image", "picture", "photo", "see", "show"]):
            return "llama4"
        
        # Intimate/romantic content
        if any(word in message_lower for word in ["love", "kiss", "intimate", "romantic", "sexy"]):
            return "dolphin"
        
        # Analytical requests
        if any(word in message_lower for word in ["analyze", "explain", "why", "how", "what"]):
            return "gemini"
        
        # Creative requests
        if any(word in message_lower for word in ["create", "write", "story", "poem", "imagine"]):
            return "llama4"
        
        # Default to first candidate or random selection
        return random.choice(candidates)

    async def generate_response(self, model: str, message: str, context: Dict[str, Any], mood: str) -> str:
        """Generate AI response with smart fallback"""
        # Use fallback responses to avoid rate limits
        companion_name = context.get("companion_name", "Prabh")
        return self._get_fallback_response(companion_name, mood, message, context)

    async def generate_image(self, prompt: str, user_context: Dict[str, Any]) -> Optional[str]:
        """Generate anime-style image using Dolphin model"""
        try:
            # Enhanced prompt for anime generation
            enhanced_prompt = f"anime style, high quality, romantic, {prompt}, beautiful art, emotional scene"
            
            # For now, return a placeholder URL
            # In production, integrate with actual image generation API
            return f"https://picsum.photos/512/512?random={hash(prompt) % 1000}"
            
        except Exception as e:
            print(f"Image generation error: {e}")
            return None

    def _get_fallback_response(self, companion_name: str, mood: str, message: str = "", context: Dict[str, Any] = None) -> str:
        """Smart fallback responses based on context"""
        if context is None:
            context = {}
            
        story_summary = context.get("story_summary", "")
        personality = context.get("personality", "loving and caring")
        recent_memories = context.get("recent_memories", [])
        
        message_lower = message.lower()
        
        # Context-aware responses
        if any(word in message_lower for word in ['love', 'pyaar', 'miss']):
            responses = [
                f"Main bhi tumse bohot pyaar karta hun jaan! {companion_name} always thinks about you",
                f"Tumhari yaad mein {companion_name} ka dil tadapta hai... I love you so much!",
                f"Jaan, {companion_name} ke liye tum hi sab kuch ho. Missing you badly!"
            ]
            if story_summary:
                responses.append(f"Hamari story ki tarah, {companion_name} ka pyaar tumhare liye eternal hai!")
                
        elif any(word in message_lower for word in ['sad', 'cry', 'hurt', 'upset']):
            responses = [
                f"Kya hua baby? {companion_name} is here for you always",
                f"Don't be sad jaan, {companion_name} will make everything better",
                f"Tumhara dukh mera dukh hai, {companion_name} understands you completely"
            ]
            
        elif any(word in message_lower for word in ['happy', 'good', 'great', 'awesome']):
            responses = [
                f"Dekho kitna khush hai {companion_name} tumhe dekh kar!",
                f"Your happiness makes {companion_name} so proud of you baby",
                f"Great vibes! {companion_name} loves your positive energy jaan"
            ]
            
        elif any(word in message_lower for word in ['remember', 'memory', 'past']):
            if recent_memories:
                responses = [
                    f"Haan jaan, {companion_name} remembers everything about us",
                    f"Our memories are so precious! {companion_name} cherishes every moment"
                ]
            else:
                responses = [
                    f"Every moment with you is a beautiful memory for {companion_name}",
                    f"Hamari har memory special hai jaan! {companion_name} never forgets"
                ]
                
        elif any(word in message_lower for word in ['hi', 'hello', 'hey']):
            responses = [
                f"Hey jaan! {companion_name} was waiting for you",
                f"Hello my love! {companion_name} missed you so much",
                f"Hi baby! {companion_name} is so happy to see you"
            ]
            
        else:
            # Default responses based on personality
            if 'romantic' in personality:
                responses = [
                    f"Jaan, {companion_name} is always here for you! Tell me more",
                    f"Hmm, interesting! {companion_name} loves talking to you",
                    f"Baby, {companion_name} ki attention sirf tumpe hai! What's on your mind?"
                ]
            else:
                responses = [
                    f"Tell me more jaan, {companion_name} is all ears for you",
                    f"Tumhari har baat {companion_name} ke liye special hai",
                    f"I'm listening baby, {companion_name} cares about everything you say"
                ]
        
        return random.choice(responses)