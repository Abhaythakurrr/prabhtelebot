"""
Complete Configuration System
All environment variables and settings
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Complete system configuration"""
    
    def __init__(self):
        # Telegram
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_use_polling = os.getenv("TELEGRAM_USE_POLLING", "true").lower() == "true"
        
        # AI Models
        self.nemotron_key = os.getenv("NEMOTRON_API_KEY")
        self.llama4_key = os.getenv("LLAMA4_API_KEY")
        self.minimax_key = os.getenv("MINIMAX_API_KEY")
        self.dolphin_key = os.getenv("DOLPHIN_VENICE_API_KEY")
        
        # Bytez (35 models)
        self.bytez_key_1 = os.getenv("BYTEZ_API_KEY_1")
        self.bytez_key_2 = os.getenv("BYTEZ_API_KEY_2")
        
        # Payment
        self.razorpay_key_id = os.getenv("RAZORPAY_KEY_ID")
        self.razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        
        # Voice
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        
        # Redis
        self.redis_url = os.getenv("REDIS_URL")
        
        # Website
        self.website_url = os.getenv("WEBSITE_URL", "http://localhost:8000")
        self.port = int(os.getenv("PORT", "8000"))
        
        # Feature flags
        self.voice_enabled = os.getenv("VOICE_PREMIUM_LIFETIME_ONLY", "true").lower() == "true"
        
    def validate(self) -> bool:
        """Validate required configuration"""
        required = [
            ("TELEGRAM_BOT_TOKEN", self.telegram_token),
            ("BYTEZ_API_KEY_1", self.bytez_key_1),
        ]
        
        missing = [name for name, value in required if not value]
        
        if missing:
            print(f"❌ Missing required config: {', '.join(missing)}")
            return False
        
        return True


# Global config instance
_config = None


def get_config() -> Config:
    """Get global config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
