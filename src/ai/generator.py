"""
AI Generator - Minimal Working Version
Will be expanded to full 35 models
"""

import logging
from typing import Dict, Any
from bytez import Bytez
from src.core.config import get_config

logger = logging.getLogger(__name__)


class AIGenerator:
    """AI content generator"""
    
    def __init__(self):
        self.config = get_config()
        self.bytez = Bytez(self.config.bytez_key_1)
    
    def generate_image(self, prompt: str, user_tier: str = "free") -> Dict[str, Any]:
        """Generate image using Bytez"""
        try:
            logger.info(f"🎨 Generating image: {prompt[:50]}...")
            
            # Use reliable model
            model = self.bytez.model("black-forest-labs/FLUX.1-schnell")
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
                "prompt": prompt
            }
            
        except Exception as e:
            logger.error(f"❌ Image generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_video(self, prompt: str, user_tier: str = "free") -> Dict[str, Any]:
        """Generate video using Bytez"""
        try:
            logger.info(f"🎬 Generating video: {prompt[:50]}...")
            
            model = self.bytez.model("ali-vilab/text-to-video-ms-1.7b")
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
                "prompt": prompt
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
