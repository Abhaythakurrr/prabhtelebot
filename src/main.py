"""
My Prabh - AI Companion Bot
Main application entry point
"""

import asyncio
import logging
from telegram.ext import Application
from src.core.config import get_config
from src.bot.telegram_bot_handler import TelegramBotHandler

logger = logging.getLogger(__name__)

class AICompanionApp:
    """Main AI Companion application"""
    
    def __init__(self):
        self.config = get_config()
        self.bot_handler = None
        self.application = None
    
    async def start(self):
        """Start the AI Companion application"""
        try:
            logger.info("Starting AI Companion Telegram Bot...")
            
            # Initialize components
            await self.initialize_components()
            
            # Start the bot
            await self.start_bot()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
    
    async def initialize_components(self):
        """Initialize all application components"""
        logger.info("Initializing AI Companion application components...")
        
        # Initialize bot handler
        self.bot_handler = TelegramBotHandler()
        
        logger.info("All components initialized successfully")
    
    async def start_bot(self):
        """Start the Telegram bot"""
        if not self.config.telegram.token:
            raise ValueError("Telegram bot token not configured")
        
        # Create application
        self.application = Application.builder().token(self.config.telegram.token).build()
        
        # Register handlers
        self.bot_handler.register_handlers(self.application)
        
        # Start polling
        logger.info("Starting Telegram bot with polling...")
        await self.application.run_polling(
            allowed_updates=["message", "callback_query", "inline_query"]
        )

async def main():
    """Main entry point"""
    app = AICompanionApp()
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())