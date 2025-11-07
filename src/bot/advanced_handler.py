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
from src.features.games import get_games_engine
from src.features.language_support import get_language_support
from src.features.mode_engine import get_mode_manager
from src.features.roleplay_story_engine import get_roleplay_story_engine
from src.features.dreamlife_engine import get_dreamlife_engine
from src.features.luci_engine import get_luci_engine

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
        self.games_engine = get_games_engine()
        self.language_support = get_language_support()
        self.mode_manager = get_mode_manager()
        self.roleplay_story = get_roleplay_story_engine()
        self.dreamlife = get_dreamlife_engine()
        self.luci = get_luci_engine()
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
        
        # Get user's current language
        current_lang = self.language_support.get_language(user_id)
        lang_emoji = {"english": "🇬🇧", "hinglish": "🇮🇳", "punjabi": "🇮🇳"}
        
        keyboard = [
            [InlineKeyboardButton("💕 Talk to Me", callback_data="chat")],
            [InlineKeyboardButton("🚀 Advanced Modes", callback_data="advanced_modes_menu")],
            [InlineKeyboardButton("🎮 Fun & Games", callback_data="fun_menu"),
             InlineKeyboardButton("🧠 Smart Tools", callback_data="smart_menu")],
            [InlineKeyboardButton("⏰ Reminders", callback_data="reminders_menu"),
             InlineKeyboardButton("💪 Daily Challenge", callback_data="daily_challenge")],
            [InlineKeyboardButton("🎨 Create Image", callback_data="gen_image"),
             InlineKeyboardButton("🎬 Create Video", callback_data="gen_video")],
            [InlineKeyboardButton("📖 Share Story", callback_data="set_story"),
             InlineKeyboardButton("🧠 Memories", callback_data="view_memories")],
            [InlineKeyboardButton(f"{lang_emoji.get(current_lang, '🌐')} Language", callback_data="language_menu"),
             InlineKeyboardButton("📊 My Account", callback_data="view_stats")],
            [InlineKeyboardButton("💎 Upgrade", callback_data="premium"),
             InlineKeyboardButton("ℹ️ Help", callback_data="help")]
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
        
        elif query.data == "advanced_modes_menu":
            # Check current mode
            current_mode = self.mode_manager.get_current_mode(str(user_id))
            mode_status = f"Active: *{current_mode.upper()}*" if current_mode else "No active mode"
            
            keyboard = [
                [InlineKeyboardButton("🎭 Roleplay Stories", callback_data="mode_roleplay")],
                [InlineKeyboardButton("🌟 Dream Life Mode", callback_data="mode_dreamlife")],
                [InlineKeyboardButton("⚡ Luci Mode (Intense)", callback_data="mode_luci")],
            ]
            
            if current_mode:
                keyboard.append([InlineKeyboardButton("📊 Mode Status", callback_data="mode_status")])
                keyboard.append([InlineKeyboardButton("🚪 Exit Mode", callback_data="mode_exit")])
            
            keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                f"🚀 *Advanced Modes*\n\n"
                f"{mode_status}\n\n"
                f"*Choose Your Experience:*\n\n"
                f"🎭 *Roleplay Stories*\n"
                f"Interactive narratives in thriller, horror, romantic, and dreamy genres\n\n"
                f"🌟 *Dream Life Mode*\n"
                f"Live your alternate life and achieve your dreams through simulation\n\n"
                f"⚡ *Luci Mode*\n"
                f"Brutal transformation mentor using dark psychology\n"
                f"⚠️ WARNING: Intense and challenging",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "mode_roleplay":
            # Show roleplay genre selection
            from src.features.roleplay_story_engine import RoleplayStoryEngine
            genres = RoleplayStoryEngine.GENRES
            
            keyboard = []
            for genre_key, genre_info in genres.items():
                keyboard.append([InlineKeyboardButton(
                    f"{genre_info['emoji']} {genre_info['name']}", 
                    callback_data=f"roleplay_start_{genre_key}"
                )])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="advanced_modes_menu")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "🎭 *Roleplay Stories*\n\n"
                "Choose your genre:\n\n"
                + "\n".join([f"{info['emoji']} *{info['name']}*: {info['description']}" 
                            for info in genres.values()]),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("roleplay_start_"):
            genre = query.data.replace("roleplay_start_", "")
            
            # Activate roleplay mode
            self.mode_manager.activate_mode(str(user_id), "roleplay")
            
            # Start story
            result = self.roleplay_story.start_story(str(user_id), genre)
            
            if result["success"]:
                # Format choices
                choices_text = "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(result["choices"])])
                
                keyboard = [
                    [InlineKeyboardButton("1️⃣", callback_data="roleplay_choice_0"),
                     InlineKeyboardButton("2️⃣", callback_data="roleplay_choice_1"),
                     InlineKeyboardButton("3️⃣", callback_data="roleplay_choice_2")],
                    [InlineKeyboardButton("🚪 Exit Story", callback_data="mode_exit")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.reply_text(
                    f"🎭 *{result['genre'].upper()} Story - Scene {result['scene_number']}*\n\n"
                    f"{result['scene']}\n\n"
                    f"*What do you do?*\n{choices_text}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await query.message.reply_text(f"Error: {result.get('error', 'Unknown error')}")
        
        elif query.data.startswith("roleplay_choice_"):
            choice_idx = int(query.data.replace("roleplay_choice_", ""))
            
            # Process choice
            result = self.roleplay_story.process_choice(str(user_id), choice_idx)
            
            if result["success"]:
                choices_text = "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(result["choices"])])
                
                keyboard = [
                    [InlineKeyboardButton("1️⃣", callback_data="roleplay_choice_0"),
                     InlineKeyboardButton("2️⃣", callback_data="roleplay_choice_1"),
                     InlineKeyboardButton("3️⃣", callback_data="roleplay_choice_2")],
                    [InlineKeyboardButton("🚪 Exit Story", callback_data="mode_exit")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.reply_text(
                    f"🎭 *Scene {result['scene_number']}*\n\n"
                    f"{result['scene']}\n\n"
                    f"*What do you do?*\n{choices_text}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await query.message.reply_text(f"Error: {result.get('error', 'Unknown error')}")
        
        elif query.data == "mode_dreamlife":
            keyboard = [
                [InlineKeyboardButton("✨ Start Dream Life", callback_data="dreamlife_start")],
                [InlineKeyboardButton("🔙 Back", callback_data="advanced_modes_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "🌟 *Dream Life Mode*\n\n"
                "Live your alternate life and achieve your dreams!\n\n"
                "*How it works:*\n"
                "1. Tell me your dream/goal\n"
                "2. I'll create a personalized life simulation\n"
                "3. Make choices and take actions\n"
                "4. Watch your dream become reality\n\n"
                "Ready to start?",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "dreamlife_start":
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="advanced_modes_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "🌟 *Tell Me Your Dream*\n\n"
                "What do you want to achieve in life?\n\n"
                "*Examples:*\n"
                "• Become a successful entrepreneur\n"
                "• Get fit and run a marathon\n"
                "• Learn to play guitar professionally\n"
                "• Build wealth and financial freedom\n"
                "• Find love and build a family\n\n"
                "Tell me your dream in detail:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "dream_description"
        
        elif query.data == "mode_luci":
            keyboard = [
                [InlineKeyboardButton("⚠️ I Understand, Activate Luci", callback_data="luci_confirm")],
                [InlineKeyboardButton("🔙 Back", callback_data="advanced_modes_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                self.luci._get_activation_warning(),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "luci_confirm":
            # Show focus area selection
            from src.features.luci_engine import LuciEngine
            focus_areas = LuciEngine.FOCUS_AREAS
            
            keyboard = []
            for area_key, area_info in focus_areas.items():
                keyboard.append([InlineKeyboardButton(
                    f"{area_info['emoji']} {area_info['name']}", 
                    callback_data=f"luci_start_{area_key}"
                )])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="advanced_modes_menu")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "⚡ *Luci Mode - Choose Your Focus*\n\n"
                + "\n".join([f"{info['emoji']} *{info['name']}*\n{info['description']}" 
                            for info in focus_areas.values()]),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("luci_start_"):
            focus_area = query.data.replace("luci_start_", "")
            
            # Activate Luci mode
            self.mode_manager.activate_mode(str(user_id), "luci")
            result = self.luci.activate_luci(str(user_id), focus_area)
            
            if result["success"]:
                keyboard = [
                    [InlineKeyboardButton("💪 Respond to Challenge", callback_data="luci_respond")],
                    [InlineKeyboardButton("🚪 Exit Luci", callback_data="mode_exit")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                challenge = result["first_challenge"]
                await query.message.reply_text(
                    f"⚡ *Luci Mode Activated*\n"
                    f"Focus: {result['focus_area'].upper()}\n"
                    f"Intensity: {result['intensity']}/10\n\n"
                    f"*Assessment:*\n{result['assessment']['assessment']}\n\n"
                    f"*Your First Challenge:*\n{challenge['challenge']}\n\n"
                    f"*Action Required:* {challenge['action_required']}\n"
                    f"*Deadline:* {challenge['deadline']}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await query.message.reply_text(f"Error: {result.get('error', 'Unknown error')}")
        
        elif query.data == "luci_respond":
            keyboard = [
                [InlineKeyboardButton("❌ Cancel", callback_data="mode_status")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                "⚡ *Report Your Progress*\n\n"
                "Tell me what you did. Be honest.\n\n"
                "Luci doesn't accept excuses.",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            context.user_data["waiting_for"] = "luci_response"
        
        elif query.data == "mode_status":
            current_mode = self.mode_manager.get_current_mode(str(user_id))
            
            if not current_mode:
                await query.message.reply_text("No active mode.")
                return
            
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="advanced_modes_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if current_mode == "roleplay":
                progress = self.roleplay_story.get_story_progress(str(user_id))
                if progress["has_story"]:
                    await query.message.reply_text(
                        f"🎭 *Roleplay Story Status*\n\n"
                        f"Genre: {progress['genre_emoji']} {progress['genre_name']}\n"
                        f"Scene: {progress['scene_number']}\n"
                        f"Choices Made: {progress['choices_made']}",
                        reply_markup=reply_markup,
                        parse_mode="Markdown"
                    )
            
            elif current_mode == "dreamlife":
                state = self.dreamlife.get_dream_state(str(user_id))
                if state:
                    await query.message.reply_text(
                        f"🌟 *Dream Life Status*\n\n"
                        f"Dream: {state['dream_description']}\n"
                        f"Progress: {state['progress_percentage']}%\n"
                        f"Milestone: {state['current_milestone']+1}/{len(state['milestones'])}\n"
                        f"Achievements: {len(state['achievements'])}",
                        reply_markup=reply_markup,
                        parse_mode="Markdown"
                    )
            
            elif current_mode == "luci":
                tracking = self.luci.track_transformation(str(user_id))
                if tracking["active"]:
                    await query.message.reply_text(
                        f"⚡ *Luci Mode Status*\n\n"
                        f"Focus: {tracking['focus_emoji']} {tracking['focus_name']}\n"
                        f"Intensity: {tracking['intensity_level']}/10\n"
                        f"Transformation Score: {tracking['transformation_score']}/100\n"
                        f"Challenges Completed: {tracking['challenges_completed']}\n"
                        f"Breakthroughs: {tracking['breakthrough_count']}",
                        reply_markup=reply_markup,
                        parse_mode="Markdown"
                    )
        
        elif query.data.startswith("dream_action_"):
            action_idx = int(query.data.replace("dream_action_", ""))
            
            # Get current scenario
            state = self.dreamlife.get_dream_state(str(user_id))
            if state and state.get("current_scenario"):
                action = state["current_scenario"]["actions"][action_idx]
                
                # Process action
                await query.message.reply_text("🌟 *Processing your action...*")
                result = self.dreamlife.process_action(str(user_id), action)
                
                if result["success"]:
                    if result.get("dream_completed"):
                        keyboard = [
                            [InlineKeyboardButton("🎉 Start New Dream", callback_data="dreamlife_start")],
                            [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_menu")]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        await query.message.reply_text(
                            f"🎉 *DREAM ACHIEVED!*\n\n"
                            f"{result['consequence']}\n\n"
                            f"You did it! Your dream is now reality!\n"
                            f"Final Progress: {result['progress']}%",
                            reply_markup=reply_markup,
                            parse_mode="Markdown"
                        )
                    else:
                        scenario = result["next_scenario"]
                        actions_text = "\n".join([f"{i+1}. {action}" for i, action in enumerate(scenario["actions"])])
                        
                        milestone_text = ""
                        if result.get("milestone_completed"):
                            milestone_text = "\n\n✅ *Milestone Completed!*\n"
                        
                        keyboard = [
                            [InlineKeyboardButton("1️⃣", callback_data="dream_action_0"),
                             InlineKeyboardButton("2️⃣", callback_data="dream_action_1"),
                             InlineKeyboardButton("3️⃣", callback_data="dream_action_2")],
                            [InlineKeyboardButton("📊 Progress", callback_data="mode_status")],
                            [InlineKeyboardButton("🚪 Exit", callback_data="mode_exit")]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        await query.message.reply_text(
                            f"🌟 *Consequence*\n\n"
                            f"{result['consequence']}"
                            f"{milestone_text}\n"
                            f"Progress: {result['progress']}%\n\n"
                            f"*Next Scenario:*\n{scenario['scenario']}\n\n"
                            f"*What do you do?*\n{actions_text}",
                            reply_markup=reply_markup,
                            parse_mode="Markdown"
                        )
                else:
                    await query.message.reply_text(f"Error: {result.get('error', 'Unknown error')}")
        
        elif query.data == "mode_exit":
            current_mode = self.mode_manager.get_current_mode(str(user_id))
            if current_mode:
                self.mode_manager.deactivate_mode(str(user_id))
                await query.message.reply_text(
                    f"✅ Exited {current_mode} mode.\n\n"
                    "Your progress has been saved."
                )
            else:
                await query.message.reply_text("No active mode to exit.")
        
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
                [InlineKeyboardButton("⭕ Tic-Tac-Toe", callback_data="game_tictactoe"),
                 InlineKeyboardButton("🎮 Word Guess", callback_data="game_word")],
                [InlineKeyboardButton("🧠 Trivia Quiz", callback_data="game_trivia"),
                 InlineKeyboardButton("🎲 Number Guess", callback_data="game_number")],
                [InlineKeyboardButton("🧩 Riddles", callback_data="game_riddle"),
                 InlineKeyboardButton("🤔 Would You Rather", callback_data="game_wyr")],
                [InlineKeyboardButton("😄 Tell Joke", callback_data="tell_joke"),
                 InlineKeyboardButton("✨ Motivate Me", callback_data="motivate")],
                [InlineKeyboardButton("📊 Game Stats", callback_data="game_stats"),
                 InlineKeyboardButton("❌ Quit Game", callback_data="quit_game")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Check if user has active game
            active_game = self.games_engine.active_games.get(user_id)
            if active_game:
                game_type = active_game['type'].replace('_', ' ').title()
                msg = f"🎮 *Fun & Games*\n\nYou have an active {game_type} game!\nContinue playing or start a new one! 😊"
            else:
                msg = "🎮 *Fun & Games*\n\nLet's play! Choose a game below! 😊"
            
            await query.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
        
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
            keyboard = [
                [InlineKeyboardButton("💊 Health", callback_data="reminder_cat_health"),
                 InlineKeyboardButton("💼 Work", callback_data="reminder_cat_work")],
                [InlineKeyboardButton("💕 Personal", callback_data="reminder_cat_personal"),
                 InlineKeyboardButton("⏰ General", callback_data="reminder_cat_general")],
                [InlineKeyboardButton("❌ Cancel", callback_data="reminders_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "⏰ *Set a Reminder*\n\n"
                "First, choose a category:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("reminder_cat_"):
            category = query.data.replace("reminder_cat_", "")
            context.user_data["reminder_category"] = category
            context.user_data["waiting_for"] = "reminder"
            
            keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="reminders_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            cat_names = {"health": "💊 Health", "work": "💼 Work", "personal": "💕 Personal", "general": "⏰ General"}
            
            await query.message.reply_text(
                f"⏰ *{cat_names.get(category, 'Reminder')}*\n\n"
                "Tell me what to remind you about and when!\n\n"
                "Examples:\n"
                "• _Take medicine in 2 hours_\n"
                "• _Meeting tomorrow at 3pm_\n"
                "• _Call mom in 30 minutes_\n\n"
                "For recurring: Add 'daily', 'weekly', or 'monthly'\n"
                "• _Take vitamins daily_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data == "view_reminders":
            by_category = self.cool_features.get_reminders_by_category(user_id)
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="reminders_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if not by_category:
                await query.message.reply_text(
                    "📋 *Your Reminders*\n\nNo active reminders! Set one with /remind 💕",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                msg = "📋 *Your Reminders*\n\n"
                
                cat_names = {"health": "💊 Health", "work": "💼 Work", "personal": "💕 Personal", "general": "⏰ General"}
                
                for category, reminders in by_category.items():
                    msg += f"*{cat_names.get(category, category.title())}*\n"
                    for r in reminders:
                        time = datetime.fromisoformat(r["time"])
                        recurring_badge = " 🔄" if r.get("recurring") else ""
                        msg += f"• {r['text']}{recurring_badge}\n"
                        msg += f"  ⏰ {time.strftime('%b %d, %I:%M %p')}\n"
                    msg += "\n"
                
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
        
        # ==================== GAME HANDLERS ====================
        
        elif query.data == "game_word":
            result = self.games_engine.start_word_game(user_id)
            await query.message.reply_text(result["message"], parse_mode="Markdown")
            context.user_data["waiting_for"] = "game_move"
        
        elif query.data == "game_trivia":
            result = self.games_engine.start_trivia(user_id)
            await query.message.reply_text(result["message"], parse_mode="Markdown")
            context.user_data["waiting_for"] = "game_move"
        
        elif query.data == "game_number":
            result = self.games_engine.start_number_game(user_id)
            await query.message.reply_text(result["message"], parse_mode="Markdown")
            context.user_data["waiting_for"] = "game_move"
        
        elif query.data == "game_riddle":
            result = self.games_engine.get_riddle(user_id)
            await query.message.reply_text(result["message"], parse_mode="Markdown")
            context.user_data["waiting_for"] = "game_move"
        
        elif query.data == "game_tictactoe":
            result = self.games_engine.start_tictactoe(user_id)
            await query.message.reply_text(result["message"], parse_mode="Markdown")
            context.user_data["waiting_for"] = "game_move"
        
        elif query.data == "game_wyr":
            result = self.games_engine.get_would_you_rather()
            await query.message.reply_text(result["message"], parse_mode="Markdown")
        
        elif query.data == "game_stats":
            result = self.games_engine.get_stats(user_id)
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="fun_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(result["message"], reply_markup=reply_markup, parse_mode="Markdown")
        
        elif query.data == "quit_game":
            result = self.games_engine.quit_game(user_id)
            context.user_data["waiting_for"] = None
            keyboard = [[InlineKeyboardButton("🎮 Play Again", callback_data="fun_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(result["message"], reply_markup=reply_markup)
        
        # ==================== LANGUAGE SUPPORT ====================
        
        elif query.data == "language_menu":
            current_lang = self.language_support.get_language(user_id)
            keyboard = [
                [InlineKeyboardButton("🇬🇧 English" + (" ✓" if current_lang == "english" else ""), 
                                    callback_data="lang_english")],
                [InlineKeyboardButton("🇮🇳 Hinglish (Hindi + English)" + (" ✓" if current_lang == "hinglish" else ""), 
                                    callback_data="lang_hinglish")],
                [InlineKeyboardButton("🇮🇳 Punjabi (Roman)" + (" ✓" if current_lang == "punjabi" else ""), 
                                    callback_data="lang_punjabi")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "🌐 *Choose Your Language*\n\n"
                "Select the language you want me to speak in! 💕\n\n"
                "मैं हिंग्लिश में भी बात कर सकती हूँ!\n"
                "Main Punjabi vich vi gal kar sakdi aan!",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif query.data.startswith("lang_"):
            language = query.data.replace("lang_", "")
            result = self.language_support.set_language(user_id, language)
            
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                result["message"],
                reply_markup=reply_markup
            )
        
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
        
        # Create payment order with correct parameters
        order_result = self.payment.create_order(str(user_id), tier, price)
        
        if order_result.get("success"):
            order_id = order_result["order_id"]
            key_id = order_result["key_id"]
            
            # Create payment link
            payment_link = f"{self.config.website_url}/payment?order_id={order_id}&user_id={user_id}&tier={tier}&amount={price}&key_id={key_id}"
            
            keyboard = [[InlineKeyboardButton("💳 Pay Now", url=payment_link)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await message.reply_text(
                f"💎 *{tier.upper()} Subscription*\n\n"
                f"Amount: ₹{price}\n"
                f"Order ID: `{order_id}`\n\n"
                "Click below to complete payment securely via Razorpay:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            error_msg = order_result.get("error", "Unknown error")
            await message.reply_text(
                f"❌ Payment system error!\n\n"
                f"Error: {error_msg}\n\n"
                "Please try again later or contact support."
            )
    
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
        
        elif waiting_for == "dream_description":
            # Extract dream and create simulation
            await update.message.reply_text("🌟 *Analyzing Your Dream...*\n\nGive me a moment...")
            
            dream = self.dreamlife.extract_dream(text)
            result = self.dreamlife.create_simulation(str(user_id), dream)
            
            if result["success"]:
                self.mode_manager.activate_mode(str(user_id), "dreamlife")
                
                scenario = result["first_scenario"]
                actions_text = "\n".join([f"{i+1}. {action}" for i, action in enumerate(scenario["actions"])])
                
                keyboard = [
                    [InlineKeyboardButton("1️⃣", callback_data="dream_action_0"),
                     InlineKeyboardButton("2️⃣", callback_data="dream_action_1"),
                     InlineKeyboardButton("3️⃣", callback_data="dream_action_2")],
                    [InlineKeyboardButton("📊 Progress", callback_data="mode_status")],
                    [InlineKeyboardButton("🚪 Exit", callback_data="mode_exit")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"🌟 *Your Dream Life Begins*\n\n"
                    f"Dream: {result['dream']}\n"
                    f"Milestones: {result['milestones_count']}\n\n"
                    f"*Your First Scenario:*\n{scenario['scenario']}\n\n"
                    f"*What do you do?*\n{actions_text}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(f"Error: {result.get('error', 'Unknown error')}")
            
            context.user_data["waiting_for"] = None
        
        elif waiting_for == "luci_response":
            # Process Luci response
            await update.message.reply_text("⚡ *Luci is judging...*")
            
            result = self.luci.process_response(str(user_id), text)
            
            if result["success"]:
                keyboard = [
                    [InlineKeyboardButton("💪 Next Challenge", callback_data="luci_respond")],
                    [InlineKeyboardButton("📊 Status", callback_data="mode_status")],
                    [InlineKeyboardButton("🚪 Exit", callback_data="mode_exit")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                score_emoji = "📈" if result["score_change"] > 0 else "📉"
                breakthrough_text = f"\n\n🔥 *BREAKTHROUGH!*\n{result['breakthrough']}" if result.get("breakthrough") else ""
                
                await update.message.reply_text(
                    f"⚡ *Luci's Feedback*\n\n"
                    f"{result['feedback']}\n\n"
                    f"{score_emoji} Score Change: {result['score_change']:+d}\n"
                    f"💯 Transformation Score: {result['transformation_score']}/100\n"
                    f"🔥 Intensity: {result['intensity']}/10"
                    f"{breakthrough_text}\n\n"
                    f"*Next Challenge:*\n{result['next_challenge']['challenge']}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            elif result.get("cooldown"):
                await update.message.reply_text(result["error"])
            elif result.get("daily_limit"):
                await update.message.reply_text(result["error"])
            else:
                await update.message.reply_text(f"Error: {result.get('error', 'Unknown error')}")
            
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
            # Parse reminder - extract what, when, and recurring from text
            import re
            
            # Check for recurring
            recurring = None
            if "daily" in text.lower():
                recurring = "daily"
                text = text.lower().replace("daily", "").strip()
            elif "weekly" in text.lower():
                recurring = "weekly"
                text = text.lower().replace("weekly", "").strip()
            elif "monthly" in text.lower():
                recurring = "monthly"
                text = text.lower().replace("monthly", "").strip()
            
            # Try to find time indicators
            time_patterns = [
                r'in (\d+) (second|minute|hour|day|week)s?',
                r'after (\d+) (second|minute|hour|day|week)s?',
                r'(tomorrow)',
                r'(\d+) (second|minute|hour|day|week)s? from now'
            ]
            
            when_text = "in 1 hour"  # default
            reminder_text = text.lower()
            
            # Remove common reminder phrases
            reminder_text = re.sub(r'^remind me to\s+', '', reminder_text)
            reminder_text = re.sub(r'^remind me\s+', '', reminder_text)
            reminder_text = re.sub(r'^to\s+', '', reminder_text)
            
            # Extract time and remove it from reminder text
            for pattern in time_patterns:
                match = re.search(pattern, reminder_text)
                if match:
                    when_text = match.group(0)
                    # Remove the time part from reminder text
                    reminder_text = reminder_text.replace(match.group(0), '').strip()
                    break
            
            # Clean up any remaining artifacts
            reminder_text = reminder_text.strip()
            
            # Get category from context
            category = context.user_data.get("reminder_category", "general")
            
            result = self.cool_features.set_reminder(user_id, reminder_text, when_text, category, recurring)
            if result["success"]:
                await update.message.reply_text(result["message"])
            else:
                await update.message.reply_text("I'll try to remember that! 💕")
            
            context.user_data["waiting_for"] = None
            context.user_data["reminder_category"] = None
        
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
        
        elif waiting_for == "game_move":
            # Handle game moves
            if user_id not in self.games_engine.active_games:
                await update.message.reply_text("No active game! Start one from the menu 🎮")
                context.user_data["waiting_for"] = None
                return
            
            game = self.games_engine.active_games[user_id]
            game_type = game["type"]
            
            if game_type == "word_guess":
                # Word guessing - expect a letter
                if len(text) == 1 and text.isalpha():
                    result = self.games_engine.guess_letter(user_id, text)
                    await update.message.reply_text(result["message"], parse_mode="Markdown")
                    
                    if result.get("won") is not None:
                        # Game ended
                        context.user_data["waiting_for"] = None
                        keyboard = [[InlineKeyboardButton("🎮 Play Again", callback_data="fun_menu")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await update.message.reply_text("Wanna play again? 😊", reply_markup=reply_markup)
                else:
                    await update.message.reply_text("Please send a single letter A-Z! 😊")
            
            elif game_type == "trivia":
                result = self.games_engine.answer_trivia(user_id, text)
                await update.message.reply_text(result["message"], parse_mode="Markdown")
            
            elif game_type == "number_guess":
                try:
                    guess = int(text)
                    result = self.games_engine.guess_number(user_id, guess)
                    await update.message.reply_text(result["message"], parse_mode="Markdown")
                    
                    if result.get("won") is not None:
                        context.user_data["waiting_for"] = None
                        keyboard = [[InlineKeyboardButton("🎮 Play Again", callback_data="fun_menu")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await update.message.reply_text("Wanna play again? 😊", reply_markup=reply_markup)
                except ValueError:
                    await update.message.reply_text("Please send a number! 😊")
            
            elif game_type == "riddle":
                result = self.games_engine.answer_riddle(user_id, text)
                await update.message.reply_text(result["message"], parse_mode="Markdown")
                
                if result.get("correct"):
                    context.user_data["waiting_for"] = None
                    keyboard = [[InlineKeyboardButton("🧩 Another Riddle", callback_data="game_riddle")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text("Want another riddle? 🧩", reply_markup=reply_markup)
            
            elif game_type == "tictactoe":
                try:
                    position = int(text)
                    result = self.games_engine.make_tictactoe_move(user_id, position)
                    await update.message.reply_text(result["message"], parse_mode="Markdown")
                    
                    if result.get("won") is not None:
                        context.user_data["waiting_for"] = None
                        keyboard = [[InlineKeyboardButton("⭕ Play Again", callback_data="game_tictactoe")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await update.message.reply_text("Wanna play again? 😊", reply_markup=reply_markup)
                except ValueError:
                    await update.message.reply_text("Please send a number 1-9! 😊")
        
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
        
        # Start proactive messaging and track tasks
        import asyncio
        self.proactive_system._task = asyncio.create_task(self.proactive_system.start())
        self._reminder_task = asyncio.create_task(self.check_reminders_loop())
        logger.info("💕 Proactive messaging system started")
    
    async def check_reminders_loop(self):
        """Check for due reminders every minute"""
        import asyncio
        
        try:
            while True:
                try:
                    # Check all users for due reminders
                    for user_id in list(self.cool_features.reminders.keys()):
                        due_reminders = self.cool_features.check_due_reminders(user_id)
                        
                        for reminder in due_reminders:
                            try:
                                # Generate personalized reminder message
                                reminder_text = reminder['text']
                                
                                # Get user persona for more personal touch
                                user = self.user_manager.get_user(user_id)
                                persona = user.get('persona')
                                persona_name = persona.get('persona_name', 'Prabh') if persona else 'Prabh'
                                
                                # Generate heartfelt, natural reminder using AI
                                try:
                                    prompt = f"""You are {persona_name}, a caring companion reminding someone to: {reminder_text}

Generate a warm, caring reminder message that:
- Sounds natural and heartfelt (not robotic)
- Shows genuine care and concern
- Is 1-2 sentences
- Includes appropriate emoji (💕 😊 ✨)
- Feels like a real person who cares

Examples:
- "Hey love! Time to have dinner. I don't want you skipping meals, okay? 💕"
- "Don't forget to drink water! Your body needs it and I need you healthy 😊"
- "It's time! Go have dinner now. I'm here making sure you take care of yourself 💕"

Generate a similar caring reminder for: {reminder_text}"""

                                    messages = [
                                        {"role": "system", "content": prompt},
                                        {"role": "user", "content": f"Generate caring reminder for: {reminder_text}"}
                                    ]
                                    
                                    model = self.roleplay.bytez.model("openai/gpt-4o-mini")
                                    result = model.run(messages)
                                    
                                    if hasattr(result, 'output') and result.output:
                                        message = result.output.get('content', '')
                                    elif isinstance(result, dict):
                                        message = result.get('content', '')
                                    else:
                                        message = str(result)
                                    
                                    # Fallback if AI fails
                                    if not message or len(message) < 10:
                                        raise Exception("AI response too short")
                                        
                                except Exception as ai_error:
                                    logger.debug(f"AI reminder generation failed: {ai_error}")
                                    # Fallback to template messages
                                    personal_messages = [
                                        f"Hey love! Time to {reminder_text}. I don't want you forgetting, okay? 💕",
                                        f"Don't forget to {reminder_text}! I'm here making sure you take care of yourself 😊",
                                        f"It's time! {reminder_text.capitalize()}. Your health matters to me 💕",
                                        f"Hey you! Time to {reminder_text}. I'm watching out for you 😊✨",
                                        f"Reminder with love: {reminder_text}! Take care of yourself for me 💕"
                                    ]
                                    import random
                                    message = random.choice(personal_messages)
                                
                                # Send text reminder
                                await self.app.bot.send_message(
                                    chat_id=user_id,
                                    text=message
                                )
                                
                                # Try to send voice reminder (if audio generation available)
                                try:
                                    # Make voice message natural and caring
                                    voice_messages = [
                                        f"Hey! It's time to {reminder_text}. I'm here reminding you because I care about you.",
                                        f"Don't forget to {reminder_text}! Your health matters to me.",
                                        f"Time to {reminder_text}! I'm watching out for you, always.",
                                        f"Hey love, {reminder_text} now, okay? Take care of yourself for me."
                                    ]
                                    import random
                                    voice_text = random.choice(voice_messages)
                                    
                                    audio_result = self.generator.generate_audio(voice_text, audio_type="speech")
                                    
                                    if audio_result["success"]:
                                        await self.app.bot.send_voice(
                                            chat_id=user_id,
                                            voice=audio_result["url"],
                                            caption="🎙️ With love 💕"
                                        )
                                except Exception as voice_error:
                                    logger.debug(f"Voice reminder skipped: {voice_error}")
                                
                            except Exception as e:
                                logger.error(f"Failed to send reminder to {user_id}: {e}")
                
                    # Check every 30 seconds
                    await asyncio.sleep(30)
                except asyncio.CancelledError:
                    logger.info("Reminder check loop cancelled")
                    break
                except Exception as e:
                    logger.error(f"Reminder check error: {e}")
                    await asyncio.sleep(60)
        finally:
            logger.info("Reminder check loop ended")
    
    def run(self):
        """Run the bot"""
        if not self.app:
            self.setup()
        
        logger.info("🤖 Starting advanced bot...")
        
        # Railway-specific: Clear webhook and start proactive system
        async def post_init(application):
            await self.clear_webhook_on_startup(application)
            await self.start_proactive_system()
        
        # Add graceful shutdown handler
        async def post_shutdown(application):
            logger.info("Shutting down background tasks...")
            # Cancel reminder task
            if hasattr(self, '_reminder_task') and not self._reminder_task.done():
                self._reminder_task.cancel()
                try:
                    await self._reminder_task
                except asyncio.CancelledError:
                    pass
            # Stop proactive system
            if hasattr(self, 'proactive_system'):
                await self.proactive_system.stop()
            logger.info("Background tasks stopped")
        
        self.app.post_init = post_init
        self.app.post_shutdown = post_shutdown
        
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
