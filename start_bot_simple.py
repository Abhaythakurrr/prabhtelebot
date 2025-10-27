"""
Simple Bot Starter - For Testing Buttons
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Start bot with detailed logging"""
    print("\n" + "="*60)
    print("🤖 STARTING BOT - SIMPLE MODE")
    print("="*60)
    
    # Check token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ No TELEGRAM_BOT_TOKEN found!")
        return
    
    print(f"✅ Bot token found: {token[:10]}...")
    
    # Import and start
    try:
        import telebot
        from src.bot.sync_bot_handler import SyncBotHandler
        
        print("✅ Imports successful")
        
        # Create bot
        bot = telebot.TeleBot(token)
        print("✅ Bot instance created")
        
        # Create handler
        handler = SyncBotHandler(bot)
        print("✅ Handler created")
        
        # Register handlers
        handler.register_handlers()
        print("✅ Handlers registered")
        
        # Get bot info
        me = bot.get_me()
        print(f"\n🤖 Bot Info:")
        print(f"   Name: @{me.username}")
        print(f"   ID: {me.id}")
        print(f"   First Name: {me.first_name}")
        
        print(f"\n📋 Registered Handlers:")
        print(f"   Message handlers: {len(bot.message_handlers)}")
        print(f"   Callback handlers: {len(bot.callback_query_handlers)}")
        
        print("\n" + "="*60)
        print("🚀 BOT IS NOW RUNNING!")
        print("="*60)
        print("\n💡 Try these commands in Telegram:")
        print("   /start - Welcome message with buttons")
        print("   /story - Upload story")
        print("   /roleplay - Generate scenarios")
        print("   /plans - View pricing")
        print("\n🔘 Click any button to test callback handling")
        print("\n⏹️  Press Ctrl+C to stop\n")
        
        # Start polling
        bot.polling(none_stop=True, interval=1, timeout=20)
        
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
