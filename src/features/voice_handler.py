"""
Voice Message Handler - Generate voice messages from persona
"""

import logging
from src.ai.generator import get_generator
from src.core.user_manager import get_user_manager
from src.story.advanced_processor import get_advanced_processor

logger = logging.getLogger(__name__)


class VoiceHandler:
    """Handle voice message generation"""
    
    def __init__(self):
        self.generator = get_generator()
        self.user_manager = get_user_manager()
        self.processor = get_advanced_processor()
    
    async def generate_voice_message(self, user_id: int, text: str = None):
        """Generate voice message from persona"""
        try:
            user = self.user_manager.get_user(user_id)
            persona = user.get('persona')
            
            if not text:
                # Generate proactive voice message
                text = self.processor.generate_proactive_message(persona) if persona else "Hey, thinking of you..."
            
            # Generate audio
            result = self.generator.generate_audio(text, audio_type="voice")
            
            if result["success"]:
                return {
                    "success": True,
                    "audio_url": result["url"],
                    "text": text
                }
            
            return {"success": False, "error": result.get("error")}
            
        except Exception as e:
            logger.error(f"Voice generation error: {e}")
            return {"success": False, "error": str(e)}


# Global instance
_voice_handler = None


def get_voice_handler():
    """Get global voice handler"""
    global _voice_handler
    if _voice_handler is None:
        _voice_handler = VoiceHandler()
    return _voice_handler
