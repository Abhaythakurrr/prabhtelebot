"""
Telegram Bot Handler - Minimal Working Version
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from src.core.config import get_config
from src.ai.generator import get_generator

logger = logging.getLogger(__name__)


class BotHandler:
    """Main bot handler"""
    
    def __init__(self):
        self.config = get_config()
        self.generator = get_generator()
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        keyboard = [
            [InlineKeyboardButton("🎨 Generate Image", callback_data="gen_image")],
            [InlineKeyboardButton("🎬 Generate Video", callback_data="gen_video")],
            [InlineKeyboardButton("🎙️ Generate Audio", callback_data="gen_audio")],
            [InlineKeyboardButton("💎 Premium", callback_data="premium")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🌟 *Welcome to My Prabh AI!*\n\n"
            "I'm your revolutionary AI companion with:\n"
            "• 35+ AI models\n"
            "• Image & video generation\n"
            "• Voice synthesis\n"
            "• Story-based personalization\n\n"
            "Choose an option below:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    async def generate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /generate command"""
        keyboard = [
            [InlineKeyboardButton("🎨 Image", callback_data="gen_image")],
            [InlineKeyboardButton("🎬 Video", callback_data="gen_video")],
            [InlineKeyboardButton("🎙️ Audio", callback_data="gen_audio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎨 *What would you like to generate?*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "gen_image":
            await query.message.reply_text(
                "🎨 *Image Generation*\n\n"
                "Send me a description of the image you want!\n\n"
                "Example: _A beautiful sunset over mountains_",
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "image_prompt"
        
        elif query.data == "gen_video":
            await query.message.reply_text(
                "🎬 *Video Generation*\n\n"
                "Send me a description of the video you want!\n\n"
                "Example: _A cat playing with a ball_",
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "video_prompt"
        
        elif query.data == "gen_audio":
            await query.message.reply_text(
                "🎙️ *Audio Generation*\n\n"
                "Send me the text you want me to speak!\n\n"
                "Example: _Hello, I love you_",
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "audio_text"
        
        elif query.data == "premium":
            await query.message.reply_text(
                "💎 *Premium Plans*\n\n"
                f"Visit: {self.config.website_url}/pricing\n\n"
                "Unlock unlimited generation!",
                parse_mode="Markdown"
            )
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text
        waiting_for = context.user_data.get("waiting_for")
        
        if waiting_for == "image_prompt":
            await update.message.reply_text("🎨 Generating your image... Please wait!")
            result = self.generator.generate_image(text)
            
            if result["success"]:
                await update.message.reply_photo(
                    photo=result["url"],
                    caption=f"✨ Generated: {result['prompt'][:100]}"
                )
            else:
                await update.message.reply_text(
                    f"❌ Generation failed: {result['error']}\n\n"
                    "Please try again!"
                )
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "video_prompt":
            await update.message.reply_text("🎬 Generating your video... This may take 2-3 minutes!")
            result = self.generator.generate_video(text)
            
            if result["success"]:
                await update.message.reply_video(
                    video=result["url"],
                    caption=f"✨ Generated: {result['prompt'][:100]}"
                )
            else:
                await update.message.reply_text(
                    f"❌ Generation failed: {result['error']}\n\n"
                    "Please try again!"
                )
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "audio_text":
            await update.message.reply_text("🎙️ Generating audio... Please wait!")
            result = self.generator.generate_audio(text)
            
            if result["success"]:
                await update.message.reply_audio(
                    audio=result["url"],
                    caption=f"✨ Generated audio"
                )
            else:
                await update.message.reply_text(
                    f"❌ Generation failed: {result['error']}\n\n"
                    "Please try again!"
                )
            context.user_data["waiting_for"] = None
        
        else:
            await update.message.reply_text(
                "👋 Hi! Use /start to see what I can do!"
            )
    
    def setup(self):
        """Setup bot handlers"""
        self.app = Application.builder().token(self.config.telegram_token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("generate", self.generate_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
        
        logger.info("✅ Bot handlers registered")
    
    def run(self):
        """Run the bot"""
        if not self.app:
            self.setup()
        
        logger.info("🤖 Starting bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
