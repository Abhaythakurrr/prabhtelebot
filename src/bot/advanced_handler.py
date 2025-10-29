"""
Advanced Telegram Bot Handler with Roleplay, NSFW, Memories, and Monetization
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.ai.generator import get_generator
from src.ai.roleplay_engine import get_roleplay_engine
from src.story.processor import get_story_processor
from src.payment.razorpay import get_payment_handler

logger = logging.getLogger(__name__)


class AdvancedBotHandler:
    """Advanced bot with roleplay, NSFW, memories, and monetization"""
    
    def __init__(self):
        self.config = get_config()
        self.user_manager = get_user_manager()
        self.generator = get_generator()
        self.roleplay = get_roleplay_engine()
        self.story_processor = get_story_processor()
        self.payment = get_payment_handler()
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user = self.user_manager.get_user(user_id)
        
        keyboard = [
            [InlineKeyboardButton("💬 Chat with Me", callback_data="chat")],
            [InlineKeyboardButton("🎨 Generate Image", callback_data="gen_image"),
             InlineKeyboardButton("🎬 Generate Video", callback_data="gen_video")],
            [InlineKeyboardButton("📖 Set My Story", callback_data="set_story"),
             InlineKeyboardButton("🧠 My Memories", callback_data="view_memories")],
            [InlineKeyboardButton("🔞 NSFW Mode", callback_data="toggle_nsfw"),
             InlineKeyboardButton("💎 Upgrade", callback_data="premium")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = f"""🌟 *Welcome to My Prabh AI!*

I'm your advanced AI companion with:
✨ Deep roleplay & personality
🎨 Image & video generation
🧠 Memory & context awareness
📖 Story-based personalization
🔞 NSFW content (Prime+)
💬 Proactive conversations

*Your Status:*
Tier: {user['tier'].upper()}
Messages Today: {user['usage']['messages_today']}
Images This Month: {user['usage']['images_this_month']}

Choose an option below! 💕"""
        
        await update.message.reply_text(
            welcome_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    async def chat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /chat command"""
        await update.message.reply_text(
            "💬 *Chat Mode Activated!*\n\n"
            "Just send me any message and I'll respond with personality and context! 💕\n\n"
            "I remember our conversations and adapt to your story.",
            parse_mode="Markdown"
        )
        context.user_data["mode"] = "chat"
    
    async def story_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /story command"""
        await update.message.reply_text(
            "📖 *Tell Me Your Story!*\n\n"
            "Share your story, fantasy, or scenario. I'll remember it and roleplay based on it!\n\n"
            "Example: _I'm a space explorer discovering new planets with my AI companion..._",
            parse_mode="Markdown"
        )
        context.user_data["waiting_for"] = "story"
    
    async def nsfw_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /nsfw command"""
        user_id = update.effective_user.id
        user = self.user_manager.get_user(user_id)
        tier_info = self.user_manager.get_tier_info(user["tier"])
        
        if not tier_info["nsfw_enabled"]:
            await update.message.reply_text(
                "🔞 *NSFW Mode*\n\n"
                "NSFW content requires Prime or Lifetime subscription!\n\n"
                "Upgrade now: /premium",
                parse_mode="Markdown"
            )
            return
        
        # Toggle NSFW
        current = user["preferences"].get("nsfw_consent", False)
        user["preferences"]["nsfw_consent"] = not current
        self.user_manager.update_user(user_id, user)
        
        status = "ENABLED" if not current else "DISABLED"
        await update.message.reply_text(
            f"🔞 *NSFW Mode {status}*\n\n"
            f"Adult content is now {'available' if not current else 'disabled'}.",
            parse_mode="Markdown"
        )
    
    async def premium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /premium command"""
        keyboard = [
            [InlineKeyboardButton("💎 BASIC - ₹299/mo", callback_data="buy_basic")],
            [InlineKeyboardButton("👑 PRIME - ₹899/mo", callback_data="buy_prime")],
            [InlineKeyboardButton("♾️ LIFETIME - ₹2999", callback_data="buy_lifetime")],
            [InlineKeyboardButton("🌐 View Full Details", url=f"{self.config.website_url}/pricing")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "💎 *Premium Plans*\n\n"
            "*BASIC (₹299/mo):*\n"
            "• Unlimited messages\n"
            "• 50 images/month\n"
            "• 5 videos/month\n\n"
            "*PRIME (₹899/mo):*\n"
            "• 500 images/month\n"
            "• 50 videos/month\n"
            "• 🔞 NSFW content\n"
            "• Proactive messages\n\n"
            "*LIFETIME (₹2999):*\n"
            "• Unlimited everything forever\n"
            "• All features unlocked\n"
            "• VIP support",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        user_id = update.effective_user.id
        
        if query.data == "chat":
            await query.message.reply_text(
                "💬 Chat mode activated! Send me any message! 💕"
            )
            context.user_data["mode"] = "chat"
        
        elif query.data == "gen_image":
            # Check limit
            can_generate, msg = self.user_manager.check_limit(user_id, "image")
            if not can_generate:
                await query.message.reply_text(f"❌ {msg}\n\nUpgrade: /premium")
                return
            
            keyboard = [
                [InlineKeyboardButton("🎨 Normal", callback_data="img_normal")],
                [InlineKeyboardButton("🌸 Anime", callback_data="img_anime")],
                [InlineKeyboardButton("📸 Realistic", callback_data="img_realistic")],
                [InlineKeyboardButton("🔞 NSFW", callback_data="img_nsfw")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "🎨 *Choose Image Style:*",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("img_"):
            style = query.data.replace("img_", "")
            context.user_data["image_style"] = style
            context.user_data["waiting_for"] = "image_prompt"
            
            await query.message.reply_text(
                f"🎨 *{style.upper()} Image Generation*\n\n"
                "Send me your prompt!\n\n"
                "Example: _A beautiful anime girl in a garden_",
                parse_mode="Markdown"
            )
        
        elif query.data == "gen_video":
            can_generate, msg = self.user_manager.check_limit(user_id, "video")
            if not can_generate:
                await query.message.reply_text(f"❌ {msg}\n\nUpgrade: /premium")
                return
            
            await query.message.reply_text(
                "🎬 *Video Generation*\n\n"
                "Send me your video prompt!\n\n"
                "Example: _A cat playing in the snow_",
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "video_prompt"
        
        elif query.data == "set_story":
            await query.message.reply_text(
                "📖 *Tell Me Your Story!*\n\n"
                "Share your fantasy, scenario, or roleplay setting.\n\n"
                "I'll remember it and adapt my personality!",
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "story"
        
        elif query.data == "view_memories":
            memories = self.user_manager.get_memories(user_id, limit=10)
            if not memories:
                await query.message.reply_text("🧠 No memories yet! Chat with me to create some! 💕")
                return
            
            mem_text = "🧠 *Your Memories:*\n\n"
            for mem in memories[-5:]:
                mem_text += f"• {mem['text'][:100]}\n"
            
            await query.message.reply_text(mem_text, parse_mode="Markdown")
        
        elif query.data == "toggle_nsfw":
            user = self.user_manager.get_user(user_id)
            tier_info = self.user_manager.get_tier_info(user["tier"])
            
            if not tier_info["nsfw_enabled"]:
                await query.message.reply_text(
                    "🔞 NSFW requires Prime or Lifetime!\n\nUpgrade: /premium"
                )
                return
            
            current = user["preferences"].get("nsfw_consent", False)
            user["preferences"]["nsfw_consent"] = not current
            self.user_manager.update_user(user_id, user)
            
            status = "ENABLED ✅" if not current else "DISABLED ❌"
            await query.message.reply_text(f"🔞 NSFW Mode: {status}")
        
        elif query.data == "premium":
            await self.premium_command(update, context)
        
        elif query.data.startswith("buy_"):
            tier = query.data.replace("buy_", "")
            await self._handle_payment(query.message, user_id, tier)
    
    async def _handle_payment(self, message, user_id: int, tier: str):
        """Handle payment initiation"""
        tier_info = self.user_manager.get_tier_info(tier)
        price = tier_info.get("price", 0)
        
        if price == 0:
            await message.reply_text("❌ Invalid tier!")
            return
        
        # Create payment order
        order = self.payment.create_order(price, f"subscription_{tier}")
        
        if order:
            payment_link = f"{self.config.website_url}/payment?order_id={order['id']}&user_id={user_id}&tier={tier}"
            
            keyboard = [[InlineKeyboardButton("💳 Pay Now", url=payment_link)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await message.reply_text(
                f"💎 *{tier.upper()} Subscription*\n\n"
                f"Amount: ₹{price}\n\n"
                "Click below to complete payment:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await message.reply_text("❌ Payment system error. Try again later!")
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        text = update.message.text
        waiting_for = context.user_data.get("waiting_for")
        mode = context.user_data.get("mode", "chat")
        
        # Check message limit
        can_send, msg = self.user_manager.check_limit(user_id, "message")
        if not can_send:
            await update.message.reply_text(f"❌ {msg}\n\nUpgrade: /premium")
            return
        
        if waiting_for == "story":
            # Process story
            await update.message.reply_text("📖 Analyzing your story... 🔮")
            story_data = self.story_processor.analyze_story(text)
            self.user_manager.set_story(user_id, story_data)
            
            await update.message.reply_text(
                f"✨ *Story Saved!*\n\n"
                f"Setting: {story_data.get('setting', 'Unknown')}\n"
                f"Characters: {', '.join(story_data.get('characters', []))}\n"
                f"Themes: {', '.join(story_data.get('themes', []))}\n\n"
                "I'll remember this in our conversations! 💕",
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "image_prompt":
            style = context.user_data.get("image_style", "normal")
            nsfw = style == "nsfw"
            
            if nsfw:
                can_nsfw, nsfw_msg = self.user_manager.check_limit(user_id, "nsfw")
                if not can_nsfw:
                    await update.message.reply_text(f"❌ {nsfw_msg}")
                    return
            
            await update.message.reply_text("🎨 Creating your image... ✨")
            result = self.generator.generate_image(text, nsfw=nsfw, style=style)
            
            if result["success"]:
                await update.message.reply_photo(
                    photo=result["url"],
                    caption=f"✨ {text[:100]}"
                )
            else:
                await update.message.reply_text(f"❌ Failed: {result['error']}")
            
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "video_prompt":
            user = self.user_manager.get_user(user_id)
            nsfw = user["preferences"].get("nsfw_consent", False)
            
            await update.message.reply_text("🎬 Generating video... This takes 2-3 minutes! ⏳")
            result = self.generator.generate_video(text, nsfw=nsfw)
            
            if result["success"]:
                await update.message.reply_video(
                    video=result["url"],
                    caption=f"✨ {text[:100]}"
                )
            else:
                await update.message.reply_text(f"❌ Failed: {result['error']}")
            
            context.user_data["waiting_for"] = None
        
        else:
            # Regular chat with roleplay
            user = self.user_manager.get_user(user_id)
            nsfw_mode = user["preferences"].get("nsfw_consent", False)
            
            await update.message.reply_chat_action("typing")
            response = self.roleplay.generate_response(user_id, text, nsfw_mode)
            await update.message.reply_text(response)
    
    def setup(self):
        """Setup bot handlers"""
        self.app = Application.builder().token(self.config.telegram_token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("chat", self.chat_command))
        self.app.add_handler(CommandHandler("story", self.story_command))
        self.app.add_handler(CommandHandler("nsfw", self.nsfw_command))
        self.app.add_handler(CommandHandler("premium", self.premium_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
        
        logger.info("✅ Advanced bot handlers registered")
    
    def run(self):
        """Run the bot"""
        if not self.app:
            self.setup()
        
        logger.info("🤖 Starting advanced bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
