"""
Configuration Management
Centralized configuration for all services
"""

import os
from typing import Optional

class Config:
    """Configuration class with all API keys and settings"""
    
    # Telegram Bot
    TELEGRAM_TOKEN: str = "8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY"
    
    # OpenRouter API Keys
    GEMINI_KEY: str = "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"
    NEMOTRON_KEY: str = "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"
    LLAMA33_KEY: str = "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"
    LLAMA4_KEY: str = "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"
    DOLPHIN_KEY: str = "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"
    
    # Razorpay
    RAZORPAY_KEY_ID: str = "rzp_live_RFCUrmIElPNS5m"
    RAZORPAY_KEY_SECRET: str = "IzybX6ykve4VJ8GxldZhVJEC"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Webhook URL (set this to your deployed URL)
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "https://your-app.render.com")
    
    # Database Configuration
    DATABASE_URL: str = "data/loveos.db"
    MEMORY_FILE: str = "data/emotional_memory.json"
    CHROMA_DB_PATH: str = "data/chroma_db"
    
    # Voice Configuration
    VOICE_MODELS_DIR: str = "data/voice_models"
    VOICE_OUTPUT_DIR: str = "data/voice_output"
    MAX_VOICE_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # AI Model Configuration
    DEFAULT_MODEL: str = "nemotron"
    MAX_TOKENS: int = 300
    TEMPERATURE: float = 0.8
    
    # Rate Limiting
    FREE_TIER_DAILY_LIMIT: int = 100
    PREMIUM_TIER_DAILY_LIMIT: int = -1  # Unlimited
    
    # File Upload Limits
    MAX_STORY_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_STORY_EXTENSIONS: list = ['.txt', '.pdf']
    
    # Subscription Plans
    SUBSCRIPTION_PLANS = {
        "premium": {
            "amount": 299,
            "currency": "INR",
            "duration_days": 30,
            "features": [
                "Unlimited messages",
                "Voice cloning",
                "Advanced AI models",
                "Image generation",
                "Priority support"
            ]
        },
        "lifetime": {
            "amount": 2999,
            "currency": "INR",
            "duration_days": 36500,  # 100 years
            "features": [
                "All premium features",
                "Lifetime access",
                "Future updates",
                "VIP support",
                "Early access to new features"
            ]
        }
    }
    
    # Model Capabilities
    MODEL_CAPABILITIES = {
        "gemini": {
            "name": "google/gemini-2.0-flash-exp:free",
            "key": GEMINI_KEY,
            "strengths": ["analysis", "reasoning", "mood_detection"],
            "max_tokens": 500,
            "supports_vision": True
        },
        "nemotron": {
            "name": "nvidia/nemotron-nano-9b-v2:free",
            "key": NEMOTRON_KEY,
            "strengths": ["conversation", "emotional_intelligence"],
            "max_tokens": 300,
            "supports_vision": False
        },
        "llama33": {
            "name": "meta-llama/llama-3.3-8b-instruct:free",
            "key": LLAMA33_KEY,
            "strengths": ["general_chat", "storytelling"],
            "max_tokens": 400,
            "supports_vision": False
        },
        "llama4": {
            "name": "meta-llama/llama-4-maverick:free",
            "key": LLAMA4_KEY,
            "strengths": ["vision", "multimodal", "creative"],
            "max_tokens": 400,
            "supports_vision": True
        },
        "dolphin": {
            "name": "cognitivecomputations/dolphin3.0-mistral-24b:free",
            "key": DOLPHIN_KEY,
            "strengths": ["intimate", "romantic", "nsfw"],
            "max_tokens": 350,
            "supports_vision": False
        }
    }
    
    # Mood to Model Mapping
    MOOD_MODEL_MAPPING = {
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
    
    # Voice Cloning Configuration
    VOICE_CONFIG = {
        "sample_rate": 22050,
        "min_duration": 5,  # seconds
        "max_duration": 60,  # seconds
        "supported_formats": ['.wav', '.mp3', '.ogg', '.m4a'],
        "quality": "high"
    }
    
    # Image Generation Configuration
    IMAGE_CONFIG = {
        "default_style": "anime",
        "resolution": "512x512",
        "quality": "high",
        "nsfw_filter": True
    }
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    CORS_ORIGINS: list = ["*"]
    
    # Performance Configuration
    MAX_CONCURRENT_REQUESTS: int = 100
    REQUEST_TIMEOUT: int = 30
    
    # Feature Flags
    FEATURES = {
        "voice_cloning": True,
        "image_generation": True,
        "story_processing": True,
        "payment_system": True,
        "analytics": True,
        "rate_limiting": True
    }
    
    @classmethod
    def get_model_config(cls, model_name: str) -> dict:
        """Get configuration for a specific model"""
        return cls.MODEL_CAPABILITIES.get(model_name, cls.MODEL_CAPABILITIES["nemotron"])
    
    @classmethod
    def get_subscription_plan(cls, plan_name: str) -> dict:
        """Get subscription plan details"""
        return cls.SUBSCRIPTION_PLANS.get(plan_name, cls.SUBSCRIPTION_PLANS["premium"])
    
    @classmethod
    def is_feature_enabled(cls, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        return cls.FEATURES.get(feature_name, False)
    
    @classmethod
    def get_models_for_mood(cls, mood: str) -> list:
        """Get recommended models for a specific mood"""
        return cls.MOOD_MODEL_MAPPING.get(mood, cls.MOOD_MODEL_MAPPING["default"])

# Environment-specific configurations
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    WEBHOOK_URL = "https://your-ngrok-url.ngrok.io"

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "INFO"
    WEBHOOK_URL = "https://your-app.render.com"

class TestingConfig(Config):
    DEBUG = True
    DATABASE_URL = "data/test_loveos.db"
    WEBHOOK_URL = "http://localhost:8000"

# Configuration factory
def get_config(env: str = "production") -> Config:
    """Get configuration based on environment"""
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    return configs.get(env, ProductionConfig)()