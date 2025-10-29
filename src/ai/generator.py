"""
AI Generator - Complete with NSFW Support and Multiple Models
"""

import logging
from typing import Dict, Any
from bytez import Bytez
from src.core.config import get_config

logger = logging.getLogger(__name__)


class AIGenerator:
    """AI content generator with NSFW support"""
    
    # Model configurations
    IMAGE_MODELS = {
        "sfw": "black-forest-labs/FLUX.1-schnell",
        "nsfw": "stabilityai/stable-diffusion-xl-base-1.0",
        "anime": "cagliostrolab/animagine-xl-3.1",
        "realistic": "playgroundai/playground-v2.5-1024px-aesthetic"
    }
    
    VIDEO_MODELS = {
        "default": "ali-vilab/text-to-video-ms-1.7b",
        "hd": "damo-vilab/text-to-video-ms-1.7b"
    }
    
    AUDIO_MODELS = {
        "default": "suno/bark-small",
        "voice": "elevenlabs/eleven-multilingual-v2"
    }
    
    def __init__(self):
        self.config = get_config()
        self.bytez = Bytez(self.config.bytez_key_1)
    
    def generate_image(self, prompt: str, nsfw: bool = False, style: str = "default") -> Dict[str, Any]:
        """Generate image with NSFW support"""
        try:
            logger.info(f"🎨 Generating image (NSFW={nsfw}): {prompt[:50]}...")
            
            # Select model based on NSFW and style
            if nsfw:
                model_name = self.IMAGE_MODELS["nsfw"]
                # Enhance NSFW prompt
                prompt = f"highly detailed, explicit, nsfw, {prompt}"
            elif style == "anime":
                model_name = self.IMAGE_MODELS["anime"]
            elif style == "realistic":
                model_name = self.IMAGE_MODELS["realistic"]
            else:
                model_name = self.IMAGE_MODELS["sfw"]
            
            model = self.bytez.model(model_name)
            result = model.run(prompt)
            
            # Handle result
            if isinstance(result, list) and result:
                image_url = result[0]
            elif isinstance(result, str):
                image_url = result
            else:
                image_url = str(result)
            
            logger.info(f"✅ Image generated: {image_url[:50]}...")
            
            return {
                "success": True,
                "url": image_url,
                "prompt": prompt,
                "nsfw": nsfw
            }
            
        except Exception as e:
            logger.error(f"❌ Image generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_video(self, prompt: str, nsfw: bool = False, hd: bool = False) -> Dict[str, Any]:
        """Generate video with NSFW support"""
        try:
            logger.info(f"🎬 Generating video (NSFW={nsfw}, HD={hd}): {prompt[:50]}...")
            
            if nsfw:
                prompt = f"explicit, adult content, nsfw, {prompt}"
            
            model_name = self.VIDEO_MODELS["hd"] if hd else self.VIDEO_MODELS["default"]
            model = self.bytez.model(model_name)
            result = model.run(prompt)
            
            if isinstance(result, list) and result:
                video_url = result[0]
            elif isinstance(result, str):
                video_url = result
            else:
                video_url = str(result)
            
            logger.info(f"✅ Video generated: {video_url[:50]}...")
            
            return {
                "success": True,
                "url": video_url,
                "prompt": prompt,
                "nsfw": nsfw
            }
            
        except Exception as e:
            logger.error(f"❌ Video generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_audio(self, text: str, user_tier: str = "free") -> Dict[str, Any]:
        """Generate audio using Bytez"""
        try:
            logger.info(f"🎙️ Generating audio: {text[:50]}...")
            
            model = self.bytez.model("suno/bark-small")
            result = model.run(text)
            
            if isinstance(result, list) and result:
                audio_url = result[0]
            elif isinstance(result, str):
                audio_url = result
            else:
                audio_url = str(result)
            
            logger.info(f"✅ Audio generated")
            
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
