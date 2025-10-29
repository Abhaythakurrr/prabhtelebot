"""
Main Entry Point - Bot + Website
"""

import logging
import threading
from src.core.config import get_config
from src.bot.handler import BotHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def run_website_thread():
    """Run website in separate thread"""
    try:
        from website.app import run_website
        logger.info("🌐 Starting website...")
        run_website()
    except Exception as e:
        logger.error(f"❌ Website error: {e}")


def main():
    """Main function"""
    logger.info("🚀 Starting My Prabh AI Companion...")
    logger.info("📊 System: 35 AI Models | Redis | SocketIO | Payment")
    
    # Load config
    config = get_config()
    
    # Validate
    if not config.validate():
        logger.error("❌ Configuration validation failed")
        return
    
    logger.info("✅ Configuration loaded")
    
    # Start website in background thread
    website_thread = threading.Thread(target=run_website_thread, daemon=True)
    website_thread.start()
    logger.info("✅ Website thread started")
    
    # Start bot (main thread)
    logger.info("🤖 Starting Telegram bot...")
    bot = BotHandler()
    bot.run()


if __name__ == "__main__":
    main()
