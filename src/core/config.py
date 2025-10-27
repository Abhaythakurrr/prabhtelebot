"""
Configuration management for the AI Companion system.
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AIModelConfig:
    """Configuration for AI models."""
    key: str
    model: str
    endpoint: str = "https://openrouter.ai/api/v1/chat/completions"
    max_tokens: int = 500
    temperature: float = 0.8
    timeout: int = 30


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str
    echo: bool = False


@dataclass
class TelegramConfig:
    """Telegram bot configuration."""
    token: str
    webhook_url: str = ""
    use_polling: bool = True


@dataclass
class RazorpayConfig:
    """Razorpay payment configuration."""
    key_id: str
    key_secret: str
    webhook_secret: str


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.telegram = TelegramConfig(
            token=os.getenv("TELEGRAM_BOT_TOKEN"),
            webhook_url=os.getenv("TELEGRAM_WEBHOOK_URL", ""),
            use_polling=os.getenv("TELEGRAM_USE_POLLING", "true").lower() == "true"
        )
        
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///ai_companion.db"),
            echo=os.getenv("DB_ECHO", "false").lower() == "true"
        )
        
        self.razorpay = RazorpayConfig(
            key_id=os.getenv("RAZORPAY_KEY_ID", ""),
            key_secret=os.getenv("RAZORPAY_KEY_SECRET", ""),
            webhook_secret=os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
        )
        
        # AI Models configuration
        self.ai_models = {
            "nemotron": AIModelConfig(
                key=os.getenv("NEMOTRON_API_KEY"),
                model=os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-nano-9b-v2:free")
            ),
            "llama4": AIModelConfig(
                key=os.getenv("LLAMA4_API_KEY"),
                model=os.getenv("LLAMA4_MODEL", "meta-llama/llama-4-maverick:free")
            ),
            "minimax": AIModelConfig(
                key=os.getenv("MINIMAX_API_KEY"),
                model=os.getenv("MINIMAX_MODEL", "minimax/minimax-m2:free")
            ),
            "dolphin_venice": AIModelConfig(
                key=os.getenv("DOLPHIN_VENICE_API_KEY"),
                model=os.getenv("DOLPHIN_VENICE_MODEL", "cognitivecomputations/dolphin-mistral-24b-venice-edition:free")
            )
        }
        
        # Bytez API Configuration
        self.bytez_api_key_1 = os.getenv("BYTEZ_API_KEY_1")
        self.bytez_api_key_2 = os.getenv("BYTEZ_API_KEY_2")
        
        # Complete Bytez Models Configuration - ALL 40+ MODELS
        self.bytez_models = {
            # NSFW Image Generation (Premium Revenue Generator) 🔥💰
            "image_nsfw_gen": os.getenv("BYTEZ_IMAGE_NSFW_GEN", "UnfilteredAI/NSFW-gen-v2.1"),
            
            # Text-to-Speech Models
            "tts_bark_small": os.getenv("BYTEZ_TTS_BARK_SMALL", "suno/bark-small"),
            "tts_bark": os.getenv("BYTEZ_TTS_BARK", "suno/bark"),
            
            # Text-to-Video Models
            "text_to_video_ms": os.getenv("BYTEZ_TEXT_TO_VIDEO_MS", "ali-vilab/text-to-video-ms-1.7b"),
            "text_to_video_zeroscope": os.getenv("BYTEZ_TEXT_TO_VIDEO_ZEROSCOPE", "cerspense/zeroscope_v2_576w"),
            "text_to_video_ltx": os.getenv("BYTEZ_TEXT_TO_VIDEO_LTX", "Lightricks/LTX-Video-0.9.7-dev"),
            
            # Text-to-Image Models
            "image_dreamlike_photoreal": os.getenv("BYTEZ_IMAGE_DREAMLIKE_PHOTOREAL", "dreamlike-art/dreamlike-photoreal-2.0"),
            "image_stable_diffusion_xl": os.getenv("BYTEZ_IMAGE_STABLE_DIFFUSION_XL", "stabilityai/stable-diffusion-xl-base-1.0"),
            "image_dreamlike_anime": os.getenv("BYTEZ_IMAGE_DREAMLIKE_ANIME", "dreamlike-art/dreamlike-anime-1.0"),
            
            # Audio Generation Models
            "audio_musicgen_small": os.getenv("BYTEZ_AUDIO_MUSICGEN_SMALL", "facebook/musicgen-stereo-small"),
            "audio_musicgen_large": os.getenv("BYTEZ_AUDIO_MUSICGEN_LARGE", "facebook/musicgen-stereo-large"),
            
            # Text Generation Models
            "text_flan_t5": os.getenv("BYTEZ_TEXT_FLAN_T5", "google/flan-t5-base"),
            "text_gpt4o": os.getenv("BYTEZ_TEXT_GPT4O", "openai/gpt-4o"),
            
            # Analysis Models
            "similarity_minilm": os.getenv("BYTEZ_SIMILARITY_MINILM", "sentence-transformers/all-MiniLM-L6-v2"),
            "text_classification_sentiment": os.getenv("BYTEZ_TEXT_CLASSIFICATION_SENTIMENT", "AdamCodd/distilbert-base-uncased-finetuned-sentiment-amazon")
        }
        
        # ElevenLabs Voice API Configuration
        self.elevenlabs = {
            "api_key": os.getenv("ELEVENLABS_API_KEY"),
            "voice_id": os.getenv("ELEVENLABS_VOICE_ID", "eVItLK1UvXctxuaRV2Oq"),
            "api_url": os.getenv("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1")
        }
        
        # Redis Configuration
        self.redis = {
            "url": os.getenv("REDIS_URL", "redis://default:kPJDA7enp7CkH2qhw4MzHjQsSGX3Ukvm@redis-15044.c212.ap-south-1-1.ec2.redns.redis-cloud.com:15044"),
            "host": os.getenv("REDIS_HOST", "redis-15044.c212.ap-south-1-1.ec2.redns.redis-cloud.com"),
            "port": int(os.getenv("REDIS_PORT", "15044")),
            "password": os.getenv("REDIS_PASSWORD", "kPJDA7enp7CkH2qhw4MzHjQsSGX3Ukvm"),
            "username": os.getenv("REDIS_USERNAME", "default"),
            "db": int(os.getenv("REDIS_DB", "0")),
            "max_connections": int(os.getenv("REDIS_MAX_CONNECTIONS", "10")),
            "socket_timeout": int(os.getenv("REDIS_SOCKET_TIMEOUT", "5")),
            "socket_connect_timeout": int(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT", "5"))
        }
        
        # Business Model Settings
        self.business = {
            "sexting_enabled": os.getenv("SEXTING_ENABLED", "true").lower() == "true",
            "nsfw_images_premium_only": os.getenv("NSFW_IMAGES_PREMIUM_ONLY", "true").lower() == "true",
            "voice_premium_lifetime_only": os.getenv("VOICE_PREMIUM_LIFETIME_ONLY", "true").lower() == "true",
            "voice_free_limit": int(os.getenv("VOICE_FREE_LIMIT", "1"))
        }


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config