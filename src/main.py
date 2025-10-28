"""
Main Entry Point - Minimal Working Version
"""

import logging
from src.core.config import get_config
from src.bot.handler import BotHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function"""
    logger.info("🚀 Starting My Prabh AI Companion...")
    
    # Load config
    config = get_config()
    
    # Validate
    if not config.validate():
        logger.error("❌ Configuration validation failed")
        return
    
    logger.info("✅ Configuration loaded")
    
    # Start bot
    bot = BotHandler()
    bot.run()


if __name__ == "__main__":
    main()
