"""
My Prabh - AI Companion Bot
Main application entry point - Fixed for threading
"""

import logging
from telegram.ext import Application
from src.core.config import get_config
from src.bot.telegram_bot_handler import TelegramBotHandler

logger = logging.getLogger(__name__)

def run_bot():
    """Run the Telegram bot - No async conflicts"""
    try:
        logger.info("Starting AI Companion Telegram Bot...")
        
        config = get_config()
        
        if not config.telegram.token:
            raise ValueError("Telegram bot token not configured")
        
        # Initialize bot handler
        bot_handler = TelegramBotHandler()
        
        # Create application
        application = Application.builder().token(config.telegram.token).build()
        
        # Register handlers
        bot_handler.register_handlers(application)
        
        logger.info("All components initialized successfully")
        
        # Start polling
        logger.info("Starting Telegram bot with polling...")
        application.run_polling(
            allowed_updates=["message", "callback_query", "inline_query"]
        )
        
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise