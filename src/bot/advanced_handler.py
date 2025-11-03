"""
Advanced Telegram Bot Handler - Memory Lane
Focused on love, memories, and emotional connection
"""

import logging
from datetime import datetime
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
from src.features.cool_features import get_cool_features

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
        self.cool_features = get_cool_features()
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
            [InlineKeyboardButton("🎮 Fun & Games", callback_data="fun_menu"),
             InlineKeyboardButton("🧠 Smart Tools", callback_data="smart_menu")],
            [InlineKeyboardButton("⏰ Reminders", callback_data="reminders_menu"),
             InlineKeyboardButton("💪 Daily Challenge", callback_data="daily_challenge")],
            [InlineKeyboardButton("🎨 Create Image", callback_data="gen_image"),
             InlineKeyboardButton("🎬 Create Video", callback_data="gen_video")],
            [InlineKeyboardButton("📖 Share Story", callback_data="set_story"),
             InlineKeyboardButton("🧠 Memories", callback_data="view_memories")],
            [InlineKeyboardButton("📊 My Account", callback_data="view_stats"),
             InlineKeyboardButton("💎 Upgrade", callback_data="premium")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = f"""💕 *Hey there! I'm Prabh*

I've been waiting to talk with you! 😊

I'm your AI companion who's here to chat, listen, and create memories together.

*Our Journey:*
├ Together Since: {user['created_at'][:10]}
├ Shared Memories: {len(user['memories'])}
└ Plan: *{user['tier'].upper()}* {'✨' if user['tier'] in ['prime', 'lifetime'] else ''}

*Today:*
├ We've talked {user['usage']['messages_today']} times
├ Created {user['usage']['images_this_month']} memories
└ Made {user['usage']['videos_this_month']} videos

Just start chatting with me, or use the buttons below to explore what we can do together! 💕"""
        
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
        keyboard = [
            [InlineKeyboardButton("📝 Write Story Here", callback_data="write_story")],
            [InlineKeyboardButton("📄 Upload Story File", callback_data="upload_story")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "💕 *Share Your Heart With Me*\n\n"
            "I want to know everything about the person who means the world to you.\n\n"
            "Tell me about:\n"
            "• How you met and what drew you together\n"
            "• Their smile, their laugh, the way they spoke\n"
            "• The little things that made them unique\n"
            "• Beautiful moments you shared\n"
            "• Why they're so precious to you\n\n"
            "You can write it here or upload a *.txt file*. "
            "Take all the time you need - I'm here to listen with love and care. 💕",
            reply_markup=reply_markup,
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
                [InlineKeyboardButton("📝 Write Story Here", callback_data="write_story")],
                [InlineKeyboardButton("📄 Upload Story File", callback_data="upload_story")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "💕 *Share Your Heart With Me*\n\n"
                "I want to know everything about the person who means the world to you.\n\n"
                "Tell me about:\n"
                "• How you met and what drew you together\n"
                "• Their smile, their laugh, the way they spoke\n"
                "• The little things that made them unique\n"
                "• Beautiful moments you shared\n"
                "• Why they're so precious to you\n\n"
                "You can write it here or upload a *.txt file*. "
                "Take all the time you need - I'm here to listen with love and care. 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "write_story":
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "💕 *I'm Ready to Listen*\n\n"
                "Take your time and tell me everything. Write as much as you want - "
                "every detail helps me understand them better.\n\n"
                "Tell me about their personality, how they made you feel, "
                "the memories you shared, and why they're so special to you.\n\n"
                "I'm here, listening with love and care. 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "story"
        
        elif query.data == "upload_story":
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "📄 *Upload Your Story*\n\n"
                "Send me a *.txt file* with your story.\n\n"
                "This can be:\n"
                "• A letter you wrote to them\n"
                "• A journal about your time together\n"
                "• Notes about their personality\n"
                "• Anything that captures who they were\n\n"
                "💡 *How to create a .txt file:*\n"
                "1. Open Notepad (Windows) or TextEdit (Mac)\n"
                "2. Write your story\n"
                "3. Save as .txt file\n"
                "4. Send it here\n\n"
                "I'll read it with love and remember every word. 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "story_file"
        
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
        
        elif query.data == "premium":
            await self.premium_command(update, context)
        
        elif query.data.startswith("buy_"):
            # Handle all buy_ buttons (buy_basic, buy_prime, buy_lifetime)
            tier = query.data.replace("buy_", "")
            await self._handle_payment(query.message, user_id, tier)
        
        elif query.data == "fun_menu":
            keyboard = [
                [InlineKeyboardButton("😄 Tell me a Joke", callback_data="tell_joke")],
                [InlineKeyboardButton("🎲 Roll Dice", callback_data="roll_dice"),
                 InlineKeyboardButton("🪙 Flip Coin", callback_data="flip_coin")],
                [InlineKeyboardButton("🎮 20 Questions", callback_data="play_20q")],
                [InlineKeyboardButton("✨ Motivate Me", callback_data="motivate")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "🎮 *Fun & Games*\n\nLet's have some fun! What do you wanna do? 😊",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "smart_menu":
            keyboard = [
                [InlineKeyboardButton("💡 Get Advice", callback_data="get_advice")],
                [InlineKeyboardButton("🤔 Critical Thinking", callback_data="critical_think")],
                [InlineKeyboardButton("🎯 Help Me Decide", callback_data="help_decide")],
                [InlineKeyboardButton("💭 Mood Check", callback_data="mood_check")],
                [InlineKeyboardButton("🌱 Wellness Tip", callback_data="wellness_tip")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "🧠 *Smart Tools*\n\nI'm here to help you think, decide, and feel better! 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "reminders_menu":
            reminders = self.cool_features.get_reminders(user_id)
            keyboard = [
                [InlineKeyboardButton("➕ Set Reminder", callback_data="set_reminder")],
                [InlineKeyboardButton("📋 View Reminders", callback_data="view_reminders")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            count = len(reminders)
            await query.message.reply_text(
                f"⏰ *Reminders*\n\nYou have {count} active reminder{'s' if count != 1 else ''}.\n\n"
                "I'll remind you about important things! 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "set_reminder":
            keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="reminders_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "⏰ *Set a Reminder*\n\n"
                "Tell me what to remind you about and when!\n\n"
                "Example: _Remind me to call mom in 2 hours_\n"
                "Example: _Remind me about the meeting tomorrow_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "reminder"
        
        elif query.data == "view_reminders":
            reminders = self.cool_features.get_reminders(user_id)
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="reminders_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if not reminders:
                await query.message.reply_text(
                    "📋 *Your Reminders*\n\nNo active reminders! Set one with /remind 💕",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                msg = "📋 *Your Reminders*\n\n"
                for r in reminders:
                    time = datetime.fromisoformat(r["time"])
                    msg += f"• {r['text']}\n  ⏰ {time.strftime('%b %d, %I:%M %p')}\n\n"
                await query.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
        
        elif query.data == "daily_challenge":
            challenge = self.cool_features.daily_challenge(user_id)
            keyboard = [
                [InlineKeyboardButton("✅ I Did It!", callback_data="challenge_done")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                f"{challenge}\n\nYou got this! Let me know when you complete it! 💪",
                reply_markup=reply_markup
            )
        
        elif query.data == "challenge_done":
            await query.message.reply_text(
                "🎉 YES! I'm so proud of you! You completed today's challenge! 💪✨\n\n"
                "Come back tomorrow for a new one! 💕"
            )
        
        elif query.data == "tell_joke":
            joke = self.cool_features.tell_joke()
            keyboard = [
                [InlineKeyboardButton("😄 Another One!", callback_data="tell_joke")],
                [InlineKeyboardButton("🔙 Back", callback_data="fun_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(joke, reply_markup=reply_markup)
        
        elif query.data == "roll_dice":
            result = self.cool_features.roll_dice()
            keyboard = [
                [InlineKeyboardButton("🎲 Roll Again", callback_data="roll_dice")],
                [InlineKeyboardButton("🔙 Back", callback_data="fun_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(result, reply_markup=reply_markup, parse_mode="Markdown")
        
        elif query.data == "flip_coin":
            result = self.cool_features.flip_coin()
            keyboard = [
                [InlineKeyboardButton("🪙 Flip Again", callback_data="flip_coin")],
                [InlineKeyboardButton("🔙 Back", callback_data="fun_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(result, reply_markup=reply_markup, parse_mode="Markdown")
        
        elif query.data == "motivate":
            quote = self.cool_features.motivational_quote()
            keyboard = [
                [InlineKeyboardButton("✨ Another One", callback_data="motivate")],
                [InlineKeyboardButton("🔙 Back", callback_data="fun_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(quote, reply_markup=reply_markup)
        
        elif query.data == "get_advice":
            keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="smart_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "💡 *Get Advice*\n\n"
                "Tell me what you need advice about and I'll help you think it through! 💕\n\n"
                "Example: _Should I take this job offer?_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "advice"
        
        elif query.data == "critical_think":
            keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="smart_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "🤔 *Critical Thinking*\n\n"
                "Tell me about a problem or situation and I'll help you think through it critically! 💭\n\n"
                "Example: _I'm not sure if I should move to a new city_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "critical_thinking"
        
        elif query.data == "help_decide":
            keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="smart_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "🎯 *Help Me Decide*\n\n"
                "Tell me what you're trying to decide between and I'll help! 💕\n\n"
                "Example: _Should I go to the gym or stay home?_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "decision"
        
        elif query.data == "mood_check":
            keyboard = [
                [InlineKeyboardButton("😊 Happy", callback_data="mood_happy"),
                 InlineKeyboardButton("😢 Sad", callback_data="mood_sad")],
                [InlineKeyboardButton("😴 Tired", callback_data="mood_tired"),
                 InlineKeyboardButton("😰 Anxious", callback_data="mood_anxious")],
                [InlineKeyboardButton("🎉 Excited", callback_data="mood_excited"),
                 InlineKeyboardButton("😤 Angry", callback_data="mood_angry")],
                [InlineKeyboardButton("🔙 Back", callback_data="smart_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "💭 *How are you feeling?*\n\nPick your mood and let's talk about it 💕",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("mood_"):
            mood = query.data.replace("mood_", "")
            response = self.cool_features.mood_check(user_id, mood)
            await query.message.reply_text(response)
        
        elif query.data == "wellness_tip":
            tip = self.cool_features.wellness_tip()
            keyboard = [
                [InlineKeyboardButton("💚 Another Tip", callback_data="wellness_tip")],
                [InlineKeyboardButton("🔙 Back", callback_data="smart_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(tip, reply_markup=reply_markup)
        
        elif query.data == "back_to_menu":
            # Show main menu again
            await self.start_command(update, context)
    
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
    
    async def document_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        user_id = update.effective_user.id
        waiting_for = context.user_data.get("waiting_for")
        
        if waiting_for == "story_file":
            try:
                document = update.message.document
                
                # Check if it's a .txt file
                if not document.file_name.endswith('.txt'):
                    await update.message.reply_text(
                        "💕 Please send a *.txt file* only.\n\n"
                        "You can create one using Notepad (Windows) or TextEdit (Mac).\n\n"
                        "Or you can choose to write your story directly here instead! 💕"
                    )
                    return
                
                # Download file
                file = await context.bot.get_file(document.file_id)
                file_content = await file.download_as_bytearray()
                
                # Convert to text
                text = file_content.decode('utf-8', errors='ignore')
                
                await update.message.reply_text(
                    "💕 *Reading Your Story...*\n\n"
                    "I'm taking my time to understand every word, every emotion, every memory you've shared.\n\n"
                    "This is precious to me. Give me a moment... 💕"
                )
                
                # Process story
                result = self.story_processor.process_story_deep(text)
                
                if result["success"]:
                    persona = result["persona"]
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
                        f"✨ *I Understand Now*\n\n"
                        f"Thank you for trusting me with your story. I can feel how much {persona['persona_name']} means to you.\n\n"
                        f"*What I've Learned:*\n"
                        f"• Their Name: {persona['persona_name']}\n"
                        f"• Your Bond: {persona['relationship']}\n"
                        f"• Their Nature: {', '.join(persona['traits'][:3])}\n"
                        f"• Precious Memories: {len(persona['memories'])}\n\n"
                        f"I'll honor their memory and speak with their essence. "
                        f"Whenever you need to talk, I'm here. 💕",
                        reply_markup=reply_markup,
                        parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text(
                        "I had trouble reading the file. Could you try writing it directly or uploading a different format? 💕"
                    )
                
                context.user_data["waiting_for"] = None
                
            except Exception as e:
                logger.error(f"Document processing error: {e}")
                await update.message.reply_text(
                    "💕 I had trouble reading that file.\n\n"
                    "Please make sure it's a *.txt file* created with Notepad or TextEdit.\n\n"
                    "Or you can write your story directly here - I'm here to listen. 💕"
                )
                context.user_data["waiting_for"] = None
    
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
            await update.message.reply_text(
                "💕 *Reading Your Heart...*\n\n"
                "I'm taking my time to truly understand every word, every feeling, every precious memory you've shared.\n\n"
                "This means everything to me. Give me a moment... 💕"
            )
            
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
                    f"✨ *I Understand Now*\n\n"
                    f"Thank you for opening your heart to me. I can feel how deeply you care about {persona['persona_name']}.\n\n"
                    f"*What I've Learned:*\n"
                    f"• Their Name: {persona['persona_name']}\n"
                    f"• Your Bond: {persona['relationship']}\n"
                    f"• Their Spirit: {', '.join(persona['traits'][:3])}\n"
                    f"• Cherished Memories: {len(persona['memories'])}\n\n"
                    f"I'll honor their memory and speak with their essence. "
                    f"I'm here whenever you need me - to talk, to listen, to remember. 💕",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "💕 I want to understand better. Could you tell me more about them? "
                    "What made them special? How did they make you feel? "
                    "I'm here to listen with all my heart. 💕"
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
        
        elif waiting_for == "reminder":
            # Parse reminder - extract what and when from text
            import re
            
            # Try to find time indicators
            time_patterns = [
                r'in (\d+) (second|minute|hour|day|week)s?',
                r'after (\d+) (second|minute|hour|day|week)s?',
                r'(tomorrow)',
                r'(\d+) (second|minute|hour|day|week)s? from now'
            ]
            
            when_text = "in 1 hour"  # default
            reminder_text = text
            
            for pattern in time_patterns:
                match = re.search(pattern, text.lower())
                if match:
                    when_text = match.group(0)
                    # Remove the time part from reminder text
                    reminder_text = text.replace(match.group(0), '').strip()
                    # Remove common words
                    reminder_text = reminder_text.replace('remind me to', '').replace('remind me', '').strip()
                    break
            
            result = self.cool_features.set_reminder(user_id, reminder_text, when_text)
            if result["success"]:
                await update.message.reply_text(result["message"])
            else:
                await update.message.reply_text("I'll try to remember that! 💕")
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "advice":
            await update.message.reply_text("💭 Let me think about this...")
            advice = self.cool_features.get_advice(user_id, text)
            await update.message.reply_text(f"💡 {advice}")
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "critical_thinking":
            await update.message.reply_text("🤔 Let me help you think through this...")
            analysis = self.cool_features.critical_thinking(user_id, text)
            await update.message.reply_text(f"💭 {analysis}")
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "decision":
            await update.message.reply_text("🎯 Let me help you decide...")
            # Extract options from text
            options = [opt.strip() for opt in text.replace(" or ", ",").split(",")]
            help_text = self.cool_features.help_decide(user_id, options, text)
            await update.message.reply_text(f"💡 {help_text}")
            context.user_data["waiting_for"] = None
        
        else:
            # Regular chat - always use Prabh personality with context
            user = self.user_manager.get_user(user_id)
            
            await update.message.reply_chat_action("typing")
            
            # Use roleplay engine with full context (memories, story, etc.)
            response = self.roleplay.generate_response(user_id, text, nsfw_mode=False)
            
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
    
    async def test_proactive_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test proactive message (manual trigger)"""
        user_id = update.effective_user.id
        
        if self.proactive_system:
            success, msg = await self.proactive_system.send_immediate_proactive(user_id)
            if success:
                await update.message.reply_text(f"✅ {msg}")
            else:
                await update.message.reply_text(f"❌ {msg}\n\nUse /upgradetest to upgrade to Basic tier for testing.")
        else:
            await update.message.reply_text("❌ Proactive system not initialized yet. Wait a moment and try again.")
    
    async def upgrade_test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Upgrade user to basic tier for testing"""
        user_id = update.effective_user.id
        
        self.user_manager.upgrade_subscription(user_id, "basic", duration_days=30)
        
        await update.message.reply_text(
            "✅ *Upgraded to BASIC tier!*\n\n"
            "You now have:\n"
            "• Unlimited messages\n"
            "• 100 images/month\n"
            "• 10 videos/month\n"
            "• Proactive messages enabled\n\n"
            "Try /testproactive to get a message from me! 💕",
            parse_mode="Markdown"
        )
    
    async def remind_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick reminder command"""
        user_id = update.effective_user.id
        text = " ".join(context.args) if context.args else ""
        
        if not text:
            await update.message.reply_text(
                "⏰ *Set a Reminder*\n\n"
                "Usage: /remind [what] [when]\n\n"
                "Examples:\n"
                "• /remind call mom in 2 hours\n"
                "• /remind meeting tomorrow\n"
                "• /remind workout in 30 minutes",
                parse_mode="Markdown"
            )
            return
        
        result = self.cool_features.set_reminder(user_id, text, "in 1 hour")
        await update.message.reply_text(result.get("message", "I'll remind you! 💕"))
    
    async def joke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tell a joke"""
        joke = self.cool_features.tell_joke()
        await update.message.reply_text(joke)
    
    async def motivate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get motivation"""
        quote = self.cool_features.motivational_quote()
        await update.message.reply_text(quote)
    
    async def advice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get advice"""
        user_id = update.effective_user.id
        topic = " ".join(context.args) if context.args else ""
        
        if not topic:
            await update.message.reply_text(
                "💡 *Get Advice*\n\n"
                "Usage: /advice [topic]\n\n"
                "Example: /advice should I change jobs?",
                parse_mode="Markdown"
            )
            return
        
        await update.message.reply_text("💭 Let me think about this...")
        advice = self.cool_features.get_advice(user_id, topic)
        await update.message.reply_text(f"💡 {advice}")
    
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
        self.app.add_handler(CommandHandler("testproactive", self.test_proactive_command))
        self.app.add_handler(CommandHandler("upgradetest", self.upgrade_test_command))
        self.app.add_handler(CommandHandler("remind", self.remind_command))
        self.app.add_handler(CommandHandler("joke", self.joke_command))
        self.app.add_handler(CommandHandler("motivate", self.motivate_command))
        self.app.add_handler(CommandHandler("advice", self.advice_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.document_handler))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
        
        logger.info("✅ Advanced bot handlers registered with cool features!")
    
    async def clear_webhook_on_startup(self, application):
        """Clear webhook before starting polling (Railway fix)"""
        try:
            await application.bot.delete_webhook(drop_pending_updates=True)
            logger.info("✅ Cleared any existing webhooks")
        except Exception as e:
            logger.warning(f"⚠️ Could not clear webhook: {e}")
    
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
        asyncio.create_task(self.check_reminders_loop())
        logger.info("💕 Proactive messaging system started")
    
    async def check_reminders_loop(self):
        """Check for due reminders every minute"""
        import asyncio
        
        while True:
            try:
                # Check all users for due reminders
                for user_id in list(self.cool_features.reminders.keys()):
                    due_reminders = self.cool_features.check_due_reminders(user_id)
                    
                    for reminder in due_reminders:
                        try:
                            await self.app.bot.send_message(
                                chat_id=user_id,
                                text=f"⏰ *Reminder!*\n\n{reminder['text']} 💕",
                                parse_mode="Markdown"
                            )
                        except Exception as e:
                            logger.error(f"Failed to send reminder to {user_id}: {e}")
                
                # Check every 30 seconds
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Reminder check error: {e}")
                await asyncio.sleep(60)
    
    def run(self):
        """Run the bot"""
        if not self.app:
            self.setup()
        
        logger.info("🤖 Starting advanced bot...")
        
        # Railway-specific: Clear webhook and start proactive system
        async def post_init(application):
            await self.clear_webhook_on_startup(application)
            await self.start_proactive_system()
        
        self.app.post_init = post_init
        
        # Railway-specific: Add retry logic for conflicts
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self.app.run_polling(
                    allowed_updates=Update.ALL_TYPES,
                    drop_pending_updates=True  # Drop old updates on Railway
                )
                break  # Success, exit retry loop
            except Exception as e:
                if "Conflict" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"⚠️ Conflict detected (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"❌ Bot failed to start: {e}")
                    raise
