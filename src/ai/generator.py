"""
AI Generator - Complete with NSFW Support and Multiple Models
"""

import logging
from typing import Dict, Any
from bytez import Bytez
from src.core.config import get_config

logger = logging.getLogger(__name__)


class AIGenerator:
    """AI content generator with rate limit handling"""
    
    # Model configurations - Using your available models
    IMAGE_MODELS = {
        "normal": "dreamlike-art/dreamlike-photoreal-2.0",
        "anime": "dreamlike-art/dreamlike-anime-1.0",
        "realistic": "stabilityai/stable-diffusion-xl-base-1.0",
        "artistic": "Lykon/DreamShaper",
        "kohaku": "KBlueLeaf/Kohaku-XL-Zeta"
    }
    
    VIDEO_MODELS = {
        "default": "ali-vilab/text-to-video-ms-1.7b",
        "hd": "cerspense/zeroscope_v2_576w"
    }
    
    AUDIO_MODELS = {
        "speech": "suno/bark-small",
        "voice": "suno/bark",
        "music": "facebook/musicgen-stereo-small",
        "music_large": "facebook/musicgen-stereo-large"
    }
    
    def __init__(self):
        self.config = get_config()
        # Use multiple API keys for rate limit handling
        self.api_keys = []
        
        # Add available API keys
        if hasattr(self.config, 'bytez_key_1') and self.config.bytez_key_1:
            self.api_keys.append(self.config.bytez_key_1)
        if hasattr(self.config, 'bytez_key_2') and self.config.bytez_key_2:
            self.api_keys.append(self.config.bytez_key_2)
        if hasattr(self.config, 'bytez_key_3') and self.config.bytez_key_3:
            self.api_keys.append(self.config.bytez_key_3)
        
        if not self.api_keys:
            raise ValueError("No Bytez API keys configured!")
        
        self.current_key_index = 0
        self.bytez = Bytez(self.api_keys[0])
    
    def _get_next_client(self):
        """Rotate to next API key to avoid rate limits (1 concurrent per key)"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Switching to API key {self.current_key_index + 1}/{len(self.api_keys)}")
        return Bytez(self.api_keys[self.current_key_index])
    
    def generate_image(self, prompt: str, style: str = "normal") -> Dict[str, Any]:
        """Generate image with style support"""
        try:
            logger.info(f"🎨 Generating image ({style}): {prompt[:50]}...")
            
            # Select model based on style
            model_name = self.IMAGE_MODELS.get(style, self.IMAGE_MODELS["normal"])
            
            # Enhance prompt for better results
            if style == "anime":
                prompt = f"anime style, high quality, detailed, {prompt}"
            elif style == "realistic":
                prompt = f"photorealistic, high quality, detailed, {prompt}"
            
            # Try with current client, rotate if rate limited
            for attempt in range(len(self.api_keys)):
                try:
                    client = self._get_next_client() if attempt > 0 else self.bytez
                    model = client.model(model_name)
                    result = model.run(prompt)
                    break
                except Exception as e:
                    if "rate limit" in str(e).lower() and attempt < len(self.api_keys) - 1:
                        logger.warning(f"Rate limited, trying next API key...")
                        continue
                    raise
            
            # Handle result - extract URL properly
            if hasattr(result, 'output'):
                # Bytez Response object
                image_url = result.output
            elif isinstance(result, list) and result:
                image_url = result[0]
            elif isinstance(result, str):
                image_url = result
            else:
                image_url = str(result)
            
            # Ensure it's a valid URL string
            if not isinstance(image_url, str):
                image_url = str(image_url)
            
            logger.info(f"✅ Image generated: {str(result)[:100]}...")
            
            return {
                "success": True,
                "url": image_url,
                "prompt": prompt,
                "style": style
            }
            
        except Exception as e:
            logger.error(f"❌ Image generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_video(self, prompt: str) -> Dict[str, Any]:
        """Generate video with rate limit handling"""
        try:
            logger.info(f"🎬 Generating video: {prompt[:50]}...")
            
            model_name = self.VIDEO_MODELS["default"]
            
            # Try with multiple API keys
            for attempt in range(len(self.api_keys)):
                try:
                    client = self._get_next_client() if attempt > 0 else self.bytez
                    model = client.model(model_name)
                    result = model.run(prompt)
                    break
                except Exception as e:
                    if "rate limit" in str(e).lower() and attempt < len(self.api_keys) - 1:
                        logger.warning(f"Rate limited, trying next API key...")
                        continue
                    raise
            
            # Handle result - extract URL properly
            if hasattr(result, 'output'):
                video_url = result.output
            elif isinstance(result, list) and result:
                video_url = result[0]
            elif isinstance(result, str):
                video_url = result
            else:
                video_url = str(result)
            
            if not isinstance(video_url, str):
                video_url = str(video_url)
            
            logger.info(f"✅ Video generated: {str(result)[:100]}...")
            
            return {
                "success": True,
                "url": video_url,
                "prompt": prompt
            }
            
        except Exception as e:
            logger.error(f"❌ Video generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_audio(self, text: str, audio_type: str = "speech") -> Dict[str, Any]:
        """Generate audio using Bytez"""
        try:
            logger.info(f"🎙️ Generating audio ({audio_type}): {text[:50]}...")
            
            # Select model based on type
            model_name = self.AUDIO_MODELS.get(audio_type, self.AUDIO_MODELS["speech"])
            
            # Try with multiple API keys
            for attempt in range(len(self.api_keys)):
                try:
                    client = self._get_next_client() if attempt > 0 else self.bytez
                    model = client.model(model_name)
                    result = model.run(text)
                    break
                except Exception as e:
                    if "rate limit" in str(e).lower() and attempt < len(self.api_keys) - 1:
                        logger.warning(f"Rate limited, trying next API key...")
                        continue
                    raise
            
            # Handle result - extract URL properly
            if hasattr(result, 'output'):
                audio_url = result.output
            elif isinstance(result, list) and result:
                audio_url = result[0]
            elif isinstance(result, str):
                audio_url = result
            else:
                audio_url = str(result)
            
            if not isinstance(audio_url, str):
                audio_url = str(audio_url)
            
            logger.info(f"✅ Audio generated: {str(result)[:100]}...")
            
            return {
                "success": True,
                "url": audio_url,
                "text": text
            }
            
        except Exception as e:
            logger.error(f"❌ Audio generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
_generator = None


def get_generator() -> AIGenerator:
    """Get global generator instance"""
    global _generator
    if _generator is None:
        _generator = AIGenerator()
    return _generator
