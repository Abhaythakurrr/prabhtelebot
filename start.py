#!/usr/bin/env python3
"""
My Prabh - AI Companion Bot
Production Entry Point - Fixed Event Loop
"""

import logging
import os
import threading
import time
from src.main import run_bot
from website.app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_website():
    """Run Flask website in a separate thread"""
    try:
        logger.info("🌐 Starting Flask website...")
        port = int(os.environ.get('PORT', 8000))
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"❌ Website error: {e}")

def start_bot():
    """Start the Telegram bot in separate thread"""
    try:
        logger.info("🤖 Starting Telegram bot...")
        run_bot()
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")

def main():
    """Main application entry point - No asyncio conflicts"""
    logger.info("🚀 AI Companion Platform - Railway Deployment")
    logger.info("============================================================")
    logger.info(f"🌍 Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'development')}")
    logger.info(f"🔌 Port: {os.getenv('PORT', 8000)}")
    logger.info(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check environment variables
    logger.info("🔍 Checking environment variables...")
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'BYTEZ_API_KEY_1',
        'BYTEZ_API_KEY_2'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {missing_vars}")
        return
    
    logger.info("✅ All required environment variables found")
    
    # Log available AI model keys
    ai_keys = [
        'NEMOTRON_API_KEY', 'LLAMA4_API_KEY', 'MINIMAX_API_KEY', 
        'DOLPHIN_VENICE_API_KEY', 'BYTEZ_API_KEY_1', 'BYTEZ_API_KEY_2'
    ]
    available_keys = [key for key in ai_keys if os.getenv(key)]
    logger.info(f"🤖 Available AI model keys: {', '.join(available_keys)}")
    
    # Start website in background thread
    logger.info("🌐 Launching website thread...")
    website_thread = threading.Thread(target=run_website, daemon=True)
    website_thread.start()
    
    # Wait for website to initialize
    logger.info("⏳ Waiting for website to initialize...")
    time.sleep(3)
    
    if website_thread.is_alive():
        logger.info("✅ Website thread is running")
    else:
        logger.warning("⚠️ Website thread may have issues")
    
    # Start Telegram bot in separate thread
    logger.info("🤖 Launching Telegram bot...")
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    logger.info("🌐 Both services running, keeping alive...")
    
    # Keep the application running
    try:
        while True:
            time.sleep(60)
            if not website_thread.is_alive():
                logger.warning("⚠️ Website thread died, restarting...")
                website_thread = threading.Thread(target=run_website, daemon=True)
                website_thread.start()
            
            if not bot_thread.is_alive():
                logger.warning("⚠️ Bot thread died, restarting...")
                bot_thread = threading.Thread(target=start_bot, daemon=True)
                bot_thread.start()
                
    except KeyboardInterrupt:
        logger.info("👋 Shutting down gracefully...")

if __name__ == "__main__":
    main()