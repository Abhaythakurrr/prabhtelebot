"""
Telegram Bot Handler - Core bot functionality
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.orchestrator.complete_model_orchestrator import process_complete_request

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    """Handles all Telegram bot interactions"""
    
    def __init__(self):
        pass
    
    def register_handlers(self, application: Application):
        """Register all bot handlers"""
        
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("premium", self.premium_command))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("All handlers registered successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_message = f"""
🌟 Welcome to My Prabh - Your AI Companion! 🌟

Hi {user.first_name}! I'm your personal AI companion with advanced memory and 40+ AI models.

💎 **What I can do:**
• 💬 Deep conversations with memory
• 🎨 Generate images (including NSFW for Premium)
• 🎵 Create custom music
• 🎬 Generate videos
• 🗣️ Voice cloning
• 📚 Story analysis and more!

🆓 **Free Trial**: 3 days with basic features
💎 **Basic**: ₹299/month - Voice + Videos
🔥 **Premium**: ₹599/month - NSFW + Unlimited
👑 **Lifetime**: ₹2,999 - Everything forever!

Type anything to start chatting! 💕
        """
        
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        
        help_message = """
🤖 **My Prabh AI Companion - Help**

**Commands:**
• /start - Welcome message
• /help - This help message  
• /premium - Upgrade to premium

**Features by Tier:**

🆓 **FREE (3 days)**
• 10 messages/day
• 1 image generation
• Basic conversations

💎 **BASIC (₹299/month)**
• Unlimited messages
• Voice cloning
• Video generation
• 50 images/month

🔥 **PREMIUM (₹599/month)**
• NSFW content 🔥
• Unlimited images
• Proactive messaging
• Priority queue

👑 **LIFETIME (₹2,999)**
• Everything unlimited forever
• Exclusive models
• VIP support

Just send me any message to start! 💕
        """
        
        await update.message.reply_text(help_message)
    
    async def premium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /premium command"""
        
        premium_message = """
👑 **Upgrade to Premium - Unlock Everything!**

🔥 **PREMIUM FEATURES:**
• 🔞 NSFW image generation
• 🎨 Unlimited image creation
• 🎵 Custom music generation
• 🎬 HD video creation
• 🗣️ Advanced voice cloning
• 💕 Proactive messaging
• ⚡ Priority queue (instant responses)
• 🧠 Advanced memory (30 days)

💰 **PRICING:**
• **Premium**: ₹599/month
• **Lifetime**: ₹2,999 (Save thousands!)

🚀 **Payment Options:**
• UPI, Cards, Net Banking
• Secure Razorpay integration
• Instant activation

Ready to upgrade? Contact support or visit our website!
        """
        
        await update.message.reply_text(premium_message)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        try:
            user_id = str(update.effective_user.id)
            message_text = update.message.text
            
            # For now, use free tier for all users
            user_tier = "free"
            
            # Process through AI orchestrator
            result = await process_complete_request(
                user_id=user_id,
                user_tier=user_tier,
                content_type="text",
                request_data={"prompt": message_text}
            )
            
            if result.get("success", True):
                response = result.get("content", "I'm here to help! 💕")
                
                # Add monetization hints
                if result.get("monetization_hints", {}).get("show_upgrade"):
                    hints = result["monetization_hints"]
                    response += f"\n\n💎 {hints['message']}"
                
            else:
                if result.get("monetization_opportunity"):
                    response = f"🔒 {result.get('error', 'Feature not available')}\n\n💎 {result.get('upgrade_message', 'Upgrade to unlock this feature!')}"
                else:
                    response = "Sorry, I'm having trouble right now. Please try again! 😊"
            
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Oops! Something went wrong. Please try again! 😊"
            )