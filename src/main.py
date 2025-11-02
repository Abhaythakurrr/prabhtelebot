"""
Main Entry Point - Advanced Bot + Website
"""

import logging
import threading
from src.core.config import get_config
from src.bot.advanced_handler import AdvancedBotHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def run_website_thread():
    """Run website in separate thread"""
    try:
        from website.love_app import run_website
        logger.info("💕 Starting Memory Lane website...")
        config = get_config()
        run_website(port=config.port)
    except Exception as e:
        logger.error(f"❌ Website error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("💕 MEMORY LANE - KEEP LOVE ALIVE FOREVER")
    logger.info("=" * 60)
    logger.info("📊 Features:")
    logger.info("   • Deep Story Processing")
    logger.info("   • Persona-Based Conversations")
    logger.info("   • Memory Preservation")
    logger.info("   • Proactive Messaging")
    logger.info("   • Image/Video Generation")
    logger.info("   • Beautiful Website")
    logger.info("   • Payment Integration")
    logger.info("=" * 60)
    
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
    logger.info("🤖 Starting Advanced Telegram Bot...")
    bot = AdvancedBotHandler()
    bot.run()


if __name__ == "__main__":
    main()
