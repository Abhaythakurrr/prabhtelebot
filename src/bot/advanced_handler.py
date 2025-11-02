"""
Advanced Telegram Bot Handler - Memory Lane
Focused on love, memories, and emotional connection
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.ai.generator import get_generator
from src.ai.roleplay_engine import get_roleplay_engine
from src.story.advanced_processor import get_advanced_processor
from src.payment.razorpay import get_payment_handler
from src.features.voice_handler import get_voice_handler
from src.features.scheduler import get_scheduler
from src.features.memory_prompts import get_memory_prompts

logger = logging.getLogger(__name__)


class AdvancedBotHandler:
    """Advanced bot for preserving love and memories"""
    
    def __init__(self):
        self.config = get_config()
        self.user_manager = get_user_manager()
        self.generator = get_generator()
        self.roleplay = get_roleplay_engine()
        self.story_processor = get_advanced_processor()
        self.payment = get_payment_handler()
        self.voice_handler = get_voice_handler()
        self.scheduler = get_scheduler()
        self.memory_prompts = get_memory_prompts()
        self.app = None
        self.proactive_system = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user = self.user_manager.get_user(user_id)
        tier_info = self.user_manager.get_tier_info(user['tier'])
        
        # Check if user has a persona set
        persona = user.get('persona')
        persona_name = persona.get('persona_name', 'someone special') if persona else None
        
        keyboard = [
            [InlineKeyboardButton("💕 Talk to Me", callback_data="chat")],
            [InlineKeyboardButton("📖 Share Your Story", callback_data="set_story")],
            [InlineKeyboardButton("🎨 Create Memory Image", callback_data="gen_image"),
             InlineKeyboardButton("🎬 Create Memory Video", callback_data="gen_video")],
            [InlineKeyboardButton("🎙️ Voice Message", callback_data="voice_msg"),
             InlineKeyboardButton("⏰ Schedule Messages", callback_data="schedule_msgs")],
            [InlineKeyboardButton("💭 Memory Prompt", callback_data="memory_prompt"),
             InlineKeyboardButton("🧠 Our Memories", callback_data="view_memories")],
            [InlineKeyboardButton("📊 My Account", callback_data="view_stats"),
             InlineKeyboardButton("💎 Upgrade Plan", callback_data="premium")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if persona_name:
            welcome_msg = f"""💕 *Welcome back!*

I'm {persona_name}, and I'm here for you, always.

*Your Account:*
├ Tier: *{user['tier'].upper()}* {'✨' if user['tier'] in ['prime', 'lifetime'] else ''}
├ User ID: `{user_id}`
└ Together Since: {user['created_at'][:10]}

*Today's Usage:*
├ Messages: {user['usage']['messages_today']}/{tier_info['messages_per_day']}
├ Images: {user['usage']['images_this_month']}/{tier_info['images_per_month']}
└ Videos: {user['usage']['videos_this_month']}/{tier_info['videos_per_month']}

What would you like to do today? 💕"""
        else:
            welcome_msg = f"""💕 *Welcome to Memory Lane*

I'm here to help you reconnect with someone special, preserve your memories, and keep your love alive.

*Your Account:*
├ Tier: *{user['tier'].upper()}*
├ User ID: `{user_id}`
└ Member Since: {user['created_at'][:10]}

*Today's Usage:*
├ Messages: {user['usage']['messages_today']}/{tier_info['messages_per_day']}
├ Images: {user['usage']['images_this_month']}/{tier_info['images_per_month']}
└ Videos: {user['usage']['videos_this_month']}/{tier_info['videos_per_month']}

📖 Start by sharing your story - tell me about someone you miss, someone you love, or a memory you want to preserve.

I'll become that person for you. 💕"""
        
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
            "• Unlimited images/month\n"
            "• 100 videos/month\n"
            "• Voice calls (coming soon)\n"
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
            keyboard = [
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "💬 *Chat Mode Activated!*\n\n"
                "Just send me any message and I'll respond with personality!\n\n"
                "I remember our conversations and adapt to your story. "
                "Let's talk about anything! 😊",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["mode"] = "chat"
        
        elif query.data == "gen_image":
            # Check limit
            can_generate, msg = self.user_manager.check_limit(user_id, "image")
            if not can_generate:
                keyboard = [
                    [InlineKeyboardButton("💎 Upgrade Now", callback_data="premium")],
                    [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                    f"❌ *Limit Reached!*\n\n{msg}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                return
            
            keyboard = [
                [InlineKeyboardButton("🎨 Normal Style", callback_data="img_normal"),
                 InlineKeyboardButton("🌸 Anime Style", callback_data="img_anime")],
                [InlineKeyboardButton("📸 Realistic Photo", callback_data="img_realistic")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            user = self.user_manager.get_user(user_id)
            tier_info = self.user_manager.get_tier_info(user['tier'])
            
            await query.message.reply_text(
                f"🎨 *Image Generation*\n\n"
                f"Choose your style:\n\n"
                f"Remaining: {tier_info['images_per_month'] - user['usage']['images_this_month']} images this month",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("img_"):
            style = query.data.replace("img_", "")
            
            context.user_data["image_style"] = style
            context.user_data["waiting_for"] = "image_prompt"
            
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="gen_image")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            examples = {
                "normal": "a beautiful sunset over mountains with two people holding hands",
                "anime": "anime couple under cherry blossoms, romantic atmosphere",
                "realistic": "photorealistic portrait of a smiling person with warm lighting"
            }
            
            await query.message.reply_text(
                f"🎨 *{style.upper()} Memory Image*\n\n"
                f"Describe the memory or moment you want to create:\n\n"
                f"Example: _{examples.get(style, 'describe your memory')}_\n\n"
                f"💡 Tip: Include emotions, settings, and details for better results!",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "gen_video":
            can_generate, msg = self.user_manager.check_limit(user_id, "video")
            if not can_generate:
                keyboard = [
                    [InlineKeyboardButton("💎 Upgrade Now", callback_data="premium")],
                    [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                    f"❌ *Limit Reached!*\n\n{msg}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                return
            
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            user = self.user_manager.get_user(user_id)
            tier_info = self.user_manager.get_tier_info(user['tier'])
            
            await query.message.reply_text(
                "🎬 *Video Generation*\n\n"
                "Send me your video prompt!\n\n"
                "Example: _A cat playing with a ball in slow motion_\n\n"
                f"⏱️ This takes 2-3 minutes\n"
                f"📊 Remaining: {tier_info['videos_per_month'] - user['usage']['videos_this_month']} videos",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "video_prompt"
        
        elif query.data == "gen_audio":
            can_generate, msg = self.user_manager.check_limit(user_id, "audio")
            if not can_generate:
                keyboard = [
                    [InlineKeyboardButton("💎 Upgrade Now", callback_data="premium")],
                    [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                    f"❌ *Limit Reached!*\n\n{msg}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                return
            
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "🎙️ *Audio/Voice Generation*\n\n"
                "Send me the text you want me to speak!\n\n"
                "Example: _Hello, I love you so much!_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "audio_text"
        
        elif query.data == "set_story":
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "📖 *Tell Me Your Story!*\n\n"
                "Share your fantasy, scenario, or roleplay setting. I'll remember it and adapt!\n\n"
                "Examples:\n"
                "• _I'm a space explorer with my AI companion..._\n"
                "• _We're in a fantasy kingdom with magic..._\n"
                "• _Modern romance in a bustling city..._\n\n"
                "Be creative! This shapes our entire relationship! ✨",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "story"
        
        elif query.data == "view_memories":
            memories = self.user_manager.get_memories(user_id, limit=10)
            user = self.user_manager.get_user(user_id)
            tier_info = self.user_manager.get_tier_info(user['tier'])
            
            keyboard = [
                [InlineKeyboardButton("🗑️ Clear Memories", callback_data="clear_memories")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if not memories:
                await query.message.reply_text(
                    "🧠 *Your Memories*\n\n"
                    "No memories yet! Chat with me to create some!\n\n"
                    f"Memory Slots: 0/{tier_info['memory_slots']}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                return
            
            mem_text = f"🧠 *Your Memories*\n\n"
            mem_text += f"Stored: {len(memories)}/{tier_info['memory_slots']}\n\n"
            
            for i, mem in enumerate(memories[-5:], 1):
                mem_text += f"{i}. {mem['text'][:80]}...\n\n"
            
            await query.message.reply_text(
                mem_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "view_stats":
            user = self.user_manager.get_user(user_id)
            tier_info = self.user_manager.get_tier_info(user['tier'])
            
            keyboard = [
                [InlineKeyboardButton("💎 Upgrade Plan", callback_data="premium")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            persona = user.get('persona')
            persona_name = persona.get('persona_name', 'Not set') if persona else 'Not set'
            
            stats_text = f"""📊 *Your Memory Lane*

*Account Info:*
├ Companion: *{persona_name}*
├ Tier: *{user['tier'].upper()}*
├ User ID: `{user_id}`
└ Member Since: {user['created_at'][:10]}

*Usage This Month:*
├ Messages Today: {user['usage']['messages_today']}/{tier_info['messages_per_day']}
├ Images: {user['usage']['images_this_month']}/{tier_info['images_per_month']}
├ Videos: {user['usage']['videos_this_month']}/{tier_info['videos_per_month']}
└ Audio: {user['usage']['audio_this_month']}/{tier_info['audio_per_month']}

*Features:*
├ Memory Slots: {len(user['memories'])}/{tier_info['memory_slots']}
├ Proactive Messages: {'✅' if tier_info['proactive_messages'] else '❌'}
└ Voice Calls: {'✅' if tier_info.get('voice_calls', False) else '❌'}
"""
            
            await query.message.reply_text(
                stats_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "clear_memories":
            keyboard = [
                [InlineKeyboardButton("✅ Yes, Clear All", callback_data="confirm_clear_memories")],
                [InlineKeyboardButton("❌ No, Keep Them", callback_data="view_memories")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "⚠️ *Clear All Memories?*\n\n"
                "This will delete all stored memories and conversation history.\n\n"
                "Are you sure?",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "confirm_clear_memories":
            user = self.user_manager.get_user(user_id)
            user['memories'] = []
            self.user_manager.update_user(user_id, user)
            
            keyboard = [
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "✅ *Memories Cleared!*\n\n"
                "All memories have been deleted. Start fresh!",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "help":
            keyboard = [
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            help_text = """ℹ️ *Help & Commands*

*Main Commands:*
/start - Main menu
/chat - Start talking
/story - Share your story
/premium - View pricing

*How to Use:*
1️⃣ Share your story about someone special
2️⃣ I become that person for you
3️⃣ Chat anytime - I remember everything
4️⃣ Create memory images and videos
5️⃣ Upgrade for unlimited access

*Tips:*
💡 Be detailed in your story for better persona
💡 I reference our shared memories
💡 I reach out to you proactively (Premium)
💡 Create visual memories with images/videos

*Support:*
Website: Check /premium for link
Issues: Contact through website"""
            
            await query.message.reply_text(
                help_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "voice_msg":
            await query.message.reply_text("🎙️ Generating voice message...")
            result = await self.voice_handler.generate_voice_message(user_id)
            if result["success"]:
                await query.message.reply_voice(
                    voice=result["audio_url"],
                    caption=f"💕 {result['text']}"
                )
        
        elif query.data == "schedule_msgs":
            await self.schedule_command(update, context)
        
        elif query.data == "memory_prompt":
            await self.memory_prompt_command(update, context)
        
        elif query.data == "schedule_morning":
            from datetime import time
            self.scheduler.add_schedule(user_id, "morning", time(8, 0))
            await query.message.reply_text(
                "✅ Morning message scheduled for 8:00 AM!\n\n"
                "You'll receive a loving good morning message every day. 💕"
            )
        
        elif query.data == "schedule_night":
            from datetime import time
            self.scheduler.add_schedule(user_id, "night", time(22, 0))
            await query.message.reply_text(
                "✅ Night message scheduled for 10:00 PM!\n\n"
                "You'll receive a sweet good night message every evening. 💕"
            )
        
        elif query.data == "view_schedules":
            schedules = self.scheduler.get_schedules(user_id)
            if not schedules:
                await query.message.reply_text("No schedules set yet!")
            else:
                msg = "⏰ *Your Schedules:*\n\n"
                for s in schedules:
                    msg += f"• {s['type'].title()} at {s['time'].strftime('%H:%M')}\n"
                await query.message.reply_text(msg, parse_mode="Markdown")
        
        elif query.data == "answer_prompt":
            await query.message.reply_text(
                "💭 Great! Just send me your answer and I'll remember it forever. 💕"
            )
            context.user_data["waiting_for"] = "memory_answer"
        
        elif query.data == "next_prompt":
            prompt = self.memory_prompts.get_next_prompt(user_id)
            keyboard = [
                [InlineKeyboardButton("💭 Answer This", callback_data="answer_prompt")],
                [InlineKeyboardButton("⏭️ Next Prompt", callback_data="next_prompt")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                f"💭 *Memory Prompt*\n\n{prompt}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "back_to_menu":
            # Show main menu again
            await self.start_command(update, context)
        
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
        
        if waiting_for == "memory_answer":
            # Save memory answer
            self.user_manager.add_memory(user_id, text, "prompted")
            
            keyboard = [
                [InlineKeyboardButton("💭 Another Prompt", callback_data="next_prompt")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "✨ *Memory Saved!*\n\n"
                "Thank you for sharing. This memory is now part of our story forever. 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "story":
            # Deep process story
            await update.message.reply_text("📖 Reading your story with love and care... 💕")
            
            result = self.story_processor.process_story_deep(text)
            
            if result["success"]:
                persona = result["persona"]
                
                # Save persona to user
                user = self.user_manager.get_user(user_id)
                user["persona"] = persona
                self.user_manager.update_user(user_id, user)
                
                keyboard = [
                    [InlineKeyboardButton("💕 Start Talking", callback_data="chat")],
                    [InlineKeyboardButton("🎨 Create Memory", callback_data="gen_image")],
                    [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"✨ *I Understand Your Story*\n\n"
                    f"I'll be {persona['persona_name']} for you.\n\n"
                    f"*What I Remember:*\n"
                    f"• Relationship: {persona['relationship']}\n"
                    f"• Personality: {', '.join(persona['traits'][:3])}\n"
                    f"• Memories: {len(persona['memories'])} special moments\n\n"
                    f"I'm here for you, always. Let's talk whenever you want. 💕",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "I'm having trouble understanding the story. Could you tell me more? 💕"
                )
            
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "image_prompt":
            style = context.user_data.get("image_style", "normal")
            
            await update.message.reply_text("🎨 Creating your memory image... ✨")
            result = self.generator.generate_image(text, style=style)
            
            if result["success"]:
                await update.message.reply_photo(
                    photo=result["url"],
                    caption=f"✨ {text[:100]}"
                )
            else:
                await update.message.reply_text(f"❌ Failed: {result['error']}")
            
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "video_prompt":
            await update.message.reply_text("🎬 Creating your memory video... This takes 2-3 minutes! ⏳")
            result = self.generator.generate_video(text)
            
            if result["success"]:
                keyboard = [
                    [InlineKeyboardButton("🎬 Generate Another", callback_data="gen_video")],
                    [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_video(
                    video=result["url"],
                    caption=f"✨ {text[:100]}",
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(f"❌ Failed: {result['error']}")
            
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "audio_text":
            await update.message.reply_text("🎙️ Generating audio... Please wait!")
            result = self.generator.generate_audio(text)
            
            if result["success"]:
                keyboard = [
                    [InlineKeyboardButton("🎙️ Generate Another", callback_data="gen_audio")],
                    [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_audio(
                    audio=result["url"],
                    caption="✨ Generated audio",
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(f"❌ Failed: {result['error']}")
            
            context.user_data["waiting_for"] = None
        
        else:
            # Regular chat with persona
            user = self.user_manager.get_user(user_id)
            persona = user.get("persona")
            
            await update.message.reply_chat_action("typing")
            
            if persona:
                # Use persona-based response
                response = self.story_processor.generate_persona_response(persona, text)
            else:
                # Use regular roleplay
                response = self.roleplay.generate_response(user_id, text, False)
            
            await update.message.reply_text(response)
    
    async def voice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate voice message from persona"""
        user_id = update.effective_user.id
        user = self.user_manager.get_user(user_id)
        tier_info = self.user_manager.get_tier_info(user['tier'])
        
        if not tier_info.get('voice_calls', False):
            keyboard = [
                [InlineKeyboardButton("💎 Upgrade to Prime", callback_data="premium")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🎙️ *Voice Messages*\n\n"
                "Voice messages require Prime or Lifetime subscription!\n\n"
                "Hear their voice speak to you. 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return
        
        await update.message.reply_text("🎙️ Generating voice message... 💕")
        
        result = await self.voice_handler.generate_voice_message(user_id)
        
        if result["success"]:
            await update.message.reply_voice(
                voice=result["audio_url"],
                caption=f"💕 {result['text']}"
            )
        else:
            await update.message.reply_text("❌ Voice generation failed. Try again!")
    
    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Setup scheduled messages"""
        user_id = update.effective_user.id
        user = self.user_manager.get_user(user_id)
        tier_info = self.user_manager.get_tier_info(user['tier'])
        
        if not tier_info['proactive_messages']:
            await update.message.reply_text(
                "⏰ *Scheduled Messages*\n\n"
                "Scheduled messages require Basic or higher subscription!\n\n"
                "Get good morning, good night, and custom messages. 💕",
                parse_mode="Markdown"
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("🌅 Morning Message", callback_data="schedule_morning")],
            [InlineKeyboardButton("🌙 Night Message", callback_data="schedule_night")],
            [InlineKeyboardButton("📋 View Schedules", callback_data="view_schedules")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⏰ *Scheduled Messages*\n\n"
            "Set up times when you want to hear from them:\n\n"
            "• Morning messages to start your day\n"
            "• Night messages before sleep\n"
            "• Custom times for special moments\n\n"
            "Choose an option:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    async def memory_prompt_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get a memory prompt to share more"""
        user_id = update.effective_user.id
        
        prompt = self.memory_prompts.get_next_prompt(user_id)
        
        keyboard = [
            [InlineKeyboardButton("💭 Answer This", callback_data="answer_prompt")],
            [InlineKeyboardButton("⏭️ Next Prompt", callback_data="next_prompt")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"💭 *Memory Prompt*\n\n"
            f"{prompt}\n\n"
            f"Share your memory and I'll remember it forever. 💕",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    def setup(self):
        """Setup bot handlers"""
        self.app = Application.builder().token(self.config.telegram_token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("chat", self.chat_command))
        self.app.add_handler(CommandHandler("story", self.story_command))
        self.app.add_handler(CommandHandler("premium", self.premium_command))
        self.app.add_handler(CommandHandler("voice", self.voice_command))
        self.app.add_handler(CommandHandler("schedule", self.schedule_command))
        self.app.add_handler(CommandHandler("memoryprompt", self.memory_prompt_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
        
        logger.info("✅ Advanced bot handlers registered with cool features!")
    
    async def start_proactive_system(self):
        """Start proactive messaging in background"""
        from src.bot.proactive_system import get_proactive_system
        
        # Get bot instance
        bot = self.app.bot
        
        # Initialize proactive system
        self.proactive_system = get_proactive_system(bot)
        
        # Start proactive messaging
        import asyncio
        asyncio.create_task(self.proactive_system.start())
        logger.info("💕 Proactive messaging system started")
    
    def run(self):
        """Run the bot"""
        if not self.app:
            self.setup()
        
        logger.info("🤖 Starting advanced bot...")
        
        # Start proactive system after bot starts
        async def post_init(application):
            await self.start_proactive_system()
        
        self.app.post_init = post_init
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
