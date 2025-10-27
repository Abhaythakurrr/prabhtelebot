"""
My Prabh - AI Companion Bot
Main application entry point - Sync telebot approach
"""

import logging
import telebot
from src.core.config import get_config
from src.bot.sync_bot_handler import SyncBotHandler

logger = logging.getLogger(__name__)

def run_bot():
    """Run the Telegram bot - Sync telebot"""
    try:
        logger.info("Starting AI Companion Telegram Bot...")
        
        config = get_config()
        
        if not config.telegram.token:
            raise ValueError("Telegram bot token not configured")
        
        # Create sync bot
        bot = telebot.TeleBot(config.telegram.token)
        
        # Initialize bot handler
        bot_handler = SyncBotHandler(bot)
        
        # Register handlers
        bot_handler.register_handlers()
        
        logger.info("All components initialized successfully")
        
        # Start polling - this blocks but works in threads
        logger.info("Starting Telegram bot with polling...")
        bot.polling(none_stop=True, interval=1, timeout=20)
        
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise