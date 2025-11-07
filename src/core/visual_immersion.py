"""
Visual Immersion Engine - Generates matching visuals for every advanced mode interaction
Uses fast image generation, GIF library fallback, and Redis caching
"""

import logging
import asyncio
import hashlib
from typing import Optional, Dict, List
from datetime import timedelta

logger = logging.getLogger(__name__)


class VisualImmersionEngine:
    """
    Generates or retrieves matching visuals for immersive experiences
    - Fast image generation (2-3 seconds)
    - GIF library fallback
    - Redis caching for performance
    - CDN integration
    """
    
    def __init__(self, bytez_client=None, redis_manager=None):
        self.bytez = bytez_client
        self.redis = redis_manager
        self.generation_timeout = 3.0  # 3 second max for image generation
        
        # GIF library categories
        self.gif_library = self._initialize_gif_library()
        
    def _initialize_gif_library(self) -> Dict[str, List[str]]:
        """Initialize curated GIF library by category"""
        return {
            # Emotions
            "happy": [
                "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
                "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
            ],
            "sad": [
                "https://media.giphy.com/media/L95W4wv8nnb9K/giphy.gif",
                "https://media.giphy.com/media/ISOckXUybVfQ4/giphy.gif",
            ],
            "excited": [
                "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif",
                "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif",
            ],
            "romantic": [
                "https://media.giphy.com/media/26u4cqiYI30juCOGY/giphy.gif",
                "https://media.giphy.com/media/3o7qDSOvfaCO9b3MlO/giphy.gif",
            ],
            "flirty": [
                "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
                "https://media.giphy.com/media/xUPGcC0R9QjyxkPnS8/giphy.gif",
            ],
            
            # Roleplay scenes
            "thriller": [
                "https://media.giphy.com/media/3o7TKB3oifq46DDhOE/giphy.gif",
                "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
            ],
            "romance": [
                "https://media.giphy.com/media/3o7qDQ4kcSD1PLM3BK/giphy.gif",
                "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
            ],
            "adventure": [
                "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
                "https://media.giphy.com/media/l0HlHFRbmaZtBRhXG/giphy.gif",
            ],
            "fantasy": [
                "https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif",
                "https://media.giphy.com/media/3o7TKtnuHOHHUjR38Y/giphy.gif",
            ],
            "horror": [
                "https://media.giphy.com/media/3o7TKxZzyBk4IlS7Is/giphy.gif",
                "https://media.giphy.com/media/l0HlvtIPzPdt2usKs/giphy.gif",
            ],
            "scifi": [
                "https://media.giphy.com/media/3o7TKP9ln2Dr6ze6f6/giphy.gif",
                "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
            ],
            
            # Dream Life scenarios
            "success": [
                "https://media.giphy.com/media/a0h7sAqON67nO/giphy.gif",
                "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif",
            ],
            "luxury": [
                "https://media.giphy.com/media/67ThRZlYBvibtdF9JH/giphy.gif",
                "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            ],
            "travel": [
                "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
                "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
            ],
            
            # Luci Mode
            "motivation": [
                "https://media.giphy.com/media/3o7qDQ4kcSD1PLM3BK/giphy.gif",
                "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
            ],
            "challenge": [
                "https://media.giphy.com/media/3o7TKB3oifq46DDhOE/giphy.gif",
                "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
            ],
            "intense": [
                "https://media.giphy.com/media/3o7TKxZzyBk4IlS7Is/giphy.gif",
                "https://media.giphy.com/media/l0HlvtIPzPdt2usKs/giphy.gif",
            ],
            
            # Generic fallbacks
            "neutral": [
                "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
            ],
            "thinking": [
                "https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif",
            ],
        }
    
    async def get_scene_visual(
        self, 
        scene_description: str, 
        mood: str = "neutral",
        force_generate: bool = False
    ) -> Optional[str]:
        """
        Returns image URL or GIF URL within 3 seconds
        
        Strategy:
        1. Check cache (100ms)
        2. Try fast generation (3s timeout)
        3. Use GIF fallback (instant)
        """
        try:
            # Generate cache key
            cache_key = self._generate_cache_key(scene_description, mood)
            
            # Check cache first (unless force_generate)
            if not force_generate and self.redis:
                cached_url = await self._get_from_cache(cache_key)
                if cached_url:
                    logger.info(f"✅ Visual cache hit for: {mood}")
                    return cached_url
            
            # Try fast image generation
            if self.bytez:
                try:
                    image_url = await asyncio.wait_for(
                        self._generate_image(scene_description, mood),
                        timeout=self.generation_timeout
                    )
                    
                    if image_url:
                        # Cache the generated image
                        if self.redis:
                            await self._save_to_cache(cache_key, image_url)
                        
                        logger.info(f"✅ Generated visual for: {mood}")
                        return image_url
                        
                except asyncio.TimeoutError:
                    logger.warning(f"⚠️ Image generation timeout, using GIF fallback")
                except Exception as e:
                    logger.error(f"Image generation error: {e}")
            
            # Fallback to GIF library
            gif_url = self.get_fallback_gif(mood)
            logger.info(f"✅ Using GIF fallback for: {mood}")
            return gif_url
            
        except Exception as e:
            logger.error(f"Error in get_scene_visual: {e}")
            return self.get_fallback_gif("neutral")
    
    async def _generate_image(
        self, 
        scene_description: str, 
        mood: str
    ) -> Optional[str]:
        """Generates image using Flux-schnell (fast model)"""
        try:
            # Create optimized prompt for fast generation
            prompt = self._create_image_prompt(scene_description, mood)
            
            # Use Flux-schnell for 2-3 second generation
            model = self.bytez.model("black-forest-labs/flux-schnell")
            
            result = model.run({
                "prompt": prompt,
                "width": 1024,
                "height": 768,
                "num_inference_steps": 4,  # Fast generation
            })
            
            # Extract image URL
            if hasattr(result, 'output'):
                if isinstance(result.output, dict):
                    return result.output.get('url') or result.output.get('image_url')
                elif isinstance(result.output, str):
                    return result.output
            
            return None
            
        except Exception as e:
            logger.error(f"Flux image generation error: {e}")
            return None
    
    def _create_image_prompt(self, scene_description: str, mood: str) -> str:
        """Creates optimized prompt for image generation"""
        mood_styles = {
            "happy": "bright, cheerful, warm colors, joyful atmosphere",
            "sad": "melancholic, soft lighting, muted colors, emotional",
            "excited": "dynamic, energetic, vibrant colors, action",
            "romantic": "soft lighting, warm tones, intimate, dreamy",
            "flirty": "playful, charming, warm atmosphere, inviting",
            "thriller": "dark, suspenseful, dramatic lighting, tense",
            "romance": "romantic, soft focus, warm lighting, intimate",
            "adventure": "epic, dynamic, dramatic, adventurous",
            "fantasy": "magical, ethereal, fantastical, enchanting",
            "horror": "dark, eerie, ominous, scary atmosphere",
            "scifi": "futuristic, high-tech, sci-fi aesthetic",
            "success": "triumphant, inspiring, golden hour, achievement",
            "luxury": "elegant, luxurious, high-end, sophisticated",
            "travel": "scenic, beautiful destination, wanderlust",
            "motivation": "inspiring, powerful, determined, strong",
            "challenge": "intense, focused, determined, powerful",
            "intense": "dramatic, powerful, high energy, focused",
        }
        
        style = mood_styles.get(mood, "cinematic, atmospheric, high quality")
        
        prompt = f"{scene_description}, {style}, professional photography, 8k, detailed"
        
        # Keep prompt concise for fast generation
        if len(prompt) > 200:
            prompt = prompt[:200]
        
        return prompt
    
    def get_fallback_gif(self, category: str) -> str:
        """Instant GIF retrieval from curated library"""
        import random
        
        # Get GIFs for category
        gifs = self.gif_library.get(category, self.gif_library["neutral"])
        
        # Return random GIF from category
        return random.choice(gifs)
    
    async def generate_character_portrait(
        self, 
        character_desc: str,
        character_name: str
    ) -> Optional[str]:
        """Generates and caches character portraits"""
        try:
            # Check cache
            cache_key = f"character:{character_name}"
            
            if self.redis:
                cached_url = await self._get_from_cache(cache_key)
                if cached_url:
                    return cached_url
            
            # Generate portrait
            prompt = f"portrait of {character_desc}, professional headshot, detailed face, high quality, 8k"
            
            if self.bytez:
                image_url = await self._generate_image(prompt, "neutral")
                
                if image_url and self.redis:
                    # Cache character portrait for 7 days
                    await self._save_to_cache(cache_key, image_url, ttl=604800)
                
                return image_url
            
            return None
            
        except Exception as e:
            logger.error(f"Character portrait generation error: {e}")
            return None
    
    def _generate_cache_key(self, scene_description: str, mood: str) -> str:
        """Generates cache key from scene description and mood"""
        content = f"{scene_description}:{mood}"
        hash_obj = hashlib.md5(content.encode())
        return f"visual:{hash_obj.hexdigest()}"
    
    async def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Retrieves visual URL from Redis cache"""
        try:
            if self.redis and hasattr(self.redis, 'get'):
                return await self.redis.get(cache_key)
            return None
        except Exception as e:
            logger.debug(f"Cache get error: {e}")
            return None
    
    async def _save_to_cache(
        self, 
        cache_key: str, 
        visual_url: str,
        ttl: int = 86400  # 24 hours default
    ):
        """Saves visual URL to Redis cache"""
        try:
            if self.redis and hasattr(self.redis, 'set'):
                await self.redis.set(cache_key, visual_url, ex=ttl)
        except Exception as e:
            logger.debug(f"Cache save error: {e}")


# Global instance
_visual_immersion_engine = None


def get_visual_immersion_engine(bytez_client=None, redis_manager=None):
    """Get global visual immersion engine instance"""
    global _visual_immersion_engine
    if _visual_immersion_engine is None:
        _visual_immersion_engine = VisualImmersionEngine(bytez_client, redis_manager)
    return _visual_immersion_engine
