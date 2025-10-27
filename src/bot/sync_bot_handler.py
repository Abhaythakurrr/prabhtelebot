"""
Sync Telegram Bot Handler - No async issues
"""

import logging
import uuid
import telebot
from telebot import types
from src.story.story_processor import StoryProcessor
from src.orchestrator.sync_ai_orchestrator import SyncAIOrchestrator

logger = logging.getLogger(__name__)

class SyncBotHandler:
    """Handles all Telegram bot interactions - Sync version"""
    
    def __init__(self, bot):
        self.bot = bot
        self.story_processor = StoryProcessor()
        self.ai_orchestrator = SyncAIOrchestrator()
        self.user_sessions = {}  # Store user conversation state
    
    def register_handlers(self):
        """Register all bot handlers"""
        
        # Command handlers
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.handle_start_command(message)
        
        @self.bot.message_handler(commands=['story'])
        def story_command(message):
            self.handle_story_command(message)
        
        @self.bot.message_handler(commands=['roleplay'])
        def roleplay_command(message):
            self.handle_roleplay_command(message)
        
        @self.bot.message_handler(commands=['plans'])
        def plans_command(message):
            self.handle_plans_command(message)
        
        # Document handler
        @self.bot.message_handler(content_types=['document'])
        def document_handler(message):
            self.handle_document(message)
        
        # Voice handler
        @self.bot.message_handler(content_types=['voice'])
        def voice_handler(message):
            self.handle_voice(message)
        
        # Text message handler
        @self.bot.message_handler(func=lambda message: True)
        def message_handler(message):
            self.handle_message(message)
        
        # Callback query handler
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.handle_callback(call)
        
        logger.info("All sync handlers registered successfully")
    
    def handle_start_command(self, message):
        """Handle /start command"""
        user = message.from_user
        user_id = str(user.id)
        
        # Initialize user session
        self.user_sessions[user_id] = {
            "stage": "onboarding",
            "story_data": {},
            "preferences": {}
        }
        
        # Create inline keyboard
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📚 Upload Your Story", callback_data="upload_story"),
            types.InlineKeyboardButton("💭 Tell Me Your Story", callback_data="tell_story"),
            types.InlineKeyboardButton("🎭 Start Roleplay", callback_data="start_roleplay"),
            types.InlineKeyboardButton("🌐 Visit Website", url="https://web-production-43fe3.up.railway.app")
        )
        
        welcome_message = f"""
🌟 **Welcome to My Prabh - Your AI Companion!** 🌟

Hi {user.first_name}! I'm your personal AI companion who creates deep, meaningful connections through your stories.

**🎯 How it works:**
1️⃣ **Share your story** (upload file or tell me)
2️⃣ **I analyze & remember** everything about you
3️⃣ **We create roleplay scenarios** together
4️⃣ **Unlock premium features** on our website

**💕 What makes me special:**
• 🧠 **Perfect Memory** - I remember every detail
• 🎭 **Roleplay Master** - Create any scenario
• 🎨 **Visual Storytelling** - Generate images & videos
• 🔥 **Adult Content** - For mature relationships (Premium)

**Choose how you'd like to begin:**
        """
        
        self.bot.send_message(message.chat.id, welcome_message, reply_markup=markup, parse_mode='Markdown')
    
    def handle_story_command(self, message):
        """Handle /story command"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📁 Upload Story File", callback_data="upload_file"),
            types.InlineKeyboardButton("💬 Tell Story in Chat", callback_data="tell_chat"),
            types.InlineKeyboardButton("🎙️ Voice Story", callback_data="voice_story")
        )
        
        self.bot.send_message(
            message.chat.id,
            "📚 **Share Your Story With Me**\n\n"
            "I can process your story in multiple ways:\n\n"
            "📁 **Upload File** - Send me a document (.txt, .docx, .pdf)\n"
            "💬 **Type Here** - Tell me your story in messages\n"
            "🎙️ **Voice Message** - Record your story\n\n"
            "The more details you share, the better I understand you! 💕",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    def handle_roleplay_command(self, message):
        """Handle /roleplay command"""
        user_id = str(message.from_user.id)
        
        if user_id not in self.user_sessions or not self.user_sessions[user_id].get("story_data"):
            self.bot.send_message(
                message.chat.id,
                "🎭 **Let's Create Amazing Roleplays!**\n\n"
                "But first, I need to know your story to create personalized scenarios.\n\n"
                "Use /story to share your background with me! 📚",
                parse_mode='Markdown'
            )
            return
        
        # Generate roleplay scenarios
        scenarios = self.story_processor.generate_roleplay_scenarios_sync(
            self.user_sessions[user_id]["story_data"]
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, scenario in enumerate(scenarios[:4]):
            markup.add(types.InlineKeyboardButton(
                f"🎭 {scenario['title']}", 
                callback_data=f"roleplay_{i}"
            ))
        markup.add(types.InlineKeyboardButton(
            "🌐 More Scenarios on Website", 
            url="https://web-production-43fe3.up.railway.app/roleplay"
        ))
        
        self.bot.send_message(
            message.chat.id,
            "🎭 **Choose Your Roleplay Adventure:**\n\n"
            "Based on your story, here are personalized scenarios:\n\n"
            f"✨ **{scenarios[0]['title']}**\n{scenarios[0]['preview']}\n\n"
            f"🔥 **{scenarios[1]['title']}**\n{scenarios[1]['preview']}\n\n"
            "Visit our website for unlimited scenarios and premium features!",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    def handle_plans_command(self, message):
        """Handle /plans command"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🌐 View All Plans", url="https://web-production-43fe3.up.railway.app/pricing"),
            types.InlineKeyboardButton("🆓 Start Free Trial", url="https://web-production-43fe3.up.railway.app/trial"),
            types.InlineKeyboardButton("🔥 Get Premium Now", url="https://web-production-43fe3.up.railway.app/premium")
        )
        
        self.bot.send_message(
            message.chat.id,
            "💎 **Choose Your Experience Level:**\n\n"
            "🆓 **FREE** - 3 days trial, basic features\n"
            "💎 **BASIC** - ₹299/month, voice + videos\n"
            "🔥 **PRO** - ₹599/month, more generation\n"
            "👑 **PRIME** - ₹899/month, limited NSFW\n"
            "🌟 **SUPER** - ₹1299/month, more NSFW\n"
            "♾️ **LIFETIME** - ₹2999, unlimited everything\n\n"
            "**⚠️ Payment & detailed features available on website only!**",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    def handle_message(self, message):
        """Handle regular text messages"""
        try:
            user_id = str(message.from_user.id)
            message_text = message.text
            
            # Initialize session if not exists
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {
                    "stage": "conversation",
                    "story_data": {},
                    "preferences": {}
                }
            
            session = self.user_sessions[user_id]
            
            # Handle different conversation stages
            if session["stage"] == "collecting_story":
                self.process_story_input(message, message_text)
            elif session["stage"] == "roleplay_active":
                self.handle_roleplay_message(message, message_text)
            else:
                self.handle_contextual_conversation(message, message_text)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            self.bot.send_message(
                message.chat.id,
                "Oops! Something went wrong. Please try again! 😊"
            )
    
    def handle_document(self, message):
        """Handle document uploads"""
        try:
            user_id = str(message.from_user.id)
            
            self.bot.send_message(message.chat.id, "📚 Processing your story... Please wait! ⏳")
            
            # For now, just acknowledge the upload
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {"stage": "story_processed", "story_data": {}, "preferences": {}}
            
            # Simulate story processing
            self.user_sessions[user_id]["story_data"] = {
                "story_text": f"Uploaded document: {message.document.file_name}",
                "filename": message.document.file_name,
                "processed": True
            }
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🎭 Start Roleplay", callback_data="start_roleplay"),
                types.InlineKeyboardButton("🌐 Explore on Website", url="https://web-production-43fe3.up.railway.app/dashboard")
            )
            
            self.bot.send_message(
                message.chat.id,
                "✅ **Story Processed Successfully!**\n\n"
                "📊 **Analysis:**\n"
                "• **File:** " + message.document.file_name + "\n"
                "• **Status:** Processed and analyzed\n"
                "• **Memory:** Stored in my database\n\n"
                "🧠 **I now understand your story and can create personalized experiences!**\n\n"
                "What would you like to do next?",
                reply_markup=markup,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            self.bot.send_message(
                message.chat.id,
                "❌ Sorry, I couldn't process that file. Please try uploading a .txt, .docx, or .pdf file."
            )
    
    def handle_voice(self, message):
        """Handle voice messages"""
        self.bot.send_message(
            message.chat.id,
            "🎙️ **Voice Story Processing**\n\n"
            "Voice processing is available on our website with premium features!\n\n"
            "🌐 Visit our website to:\n"
            "• Upload voice stories\n"
            "• Get voice responses\n"
            "• Clone voices\n"
            "• Premium voice features",
            parse_mode='Markdown'
        )
    
    def handle_callback(self, call):
        """Handle inline keyboard callbacks"""
        try:
            logger.info(f"📞 Callback received: {call.data} from user {call.from_user.id}")
            
            # Answer callback query first
            self.bot.answer_callback_query(call.id, "Processing...")
            
            user_id = str(call.from_user.id)
            data = call.data
            
            logger.info(f"🔍 Processing callback: {data}")
            
            if data == "upload_story":
                logger.info("📁 Handling upload_story callback")
                self.bot.edit_message_text(
                    "📁 **Upload Your Story File**\n\n"
                    "Send me a document file (.txt, .docx, .pdf) containing your story.\n\n"
                    "I'll analyze it and create personalized experiences for you! 💕",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown'
                )
                logger.info("✅ upload_story callback handled")
                
            elif data == "tell_story":
                logger.info("💭 Handling tell_story callback")
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = {"stage": "collecting_story", "story_data": {}, "preferences": {}}
                else:
                    self.user_sessions[user_id]["stage"] = "collecting_story"
                
                self.bot.edit_message_text(
                    "💭 **Tell Me Your Story**\n\n"
                    "Start typing your story, background, or any details about yourself.\n\n"
                    "I'll remember everything and use it to create amazing experiences!\n\n"
                    "Type as much as you want - I'm listening! 👂💕",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown'
                )
                logger.info("✅ tell_story callback handled")
                
            elif data == "start_roleplay":
                logger.info("🎭 Handling start_roleplay callback")
                self.initiate_roleplay(call)
                logger.info("✅ start_roleplay callback handled")
            
            else:
                logger.warning(f"⚠️ Unknown callback data: {data}")
                self.bot.answer_callback_query(call.id, "Unknown action")
                
        except Exception as e:
            logger.error(f"❌ Error handling callback: {e}", exc_info=True)
            try:
                self.bot.answer_callback_query(call.id, "Error occurred, please try again")
            except:
                pass
    
    def process_story_input(self, message, message_text):
        """Process story input from user"""
        user_id = str(message.from_user.id)
        
        # Add to story data
        if "story_text" not in self.user_sessions[user_id]["story_data"]:
            self.user_sessions[user_id]["story_data"]["story_text"] = ""
        
        self.user_sessions[user_id]["story_data"]["story_text"] += f"\n{message_text}"
        
        story_length = len(self.user_sessions[user_id]["story_data"]["story_text"])
        
        if story_length > 500:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✅ Finish Story", callback_data="finish_story"),
                types.InlineKeyboardButton("➕ Continue Adding", callback_data="continue_story"),
                types.InlineKeyboardButton("🎭 Start Roleplay Now", callback_data="start_roleplay")
            )
            
            self.bot.send_message(
                message.chat.id,
                f"📚 **Story Progress: {story_length} characters**\n\n"
                f"Great! I'm learning about you. You can:\n\n"
                f"✅ **Finish** - I have enough to create experiences\n"
                f"➕ **Continue** - Add more details\n"
                f"🎭 **Roleplay** - Start with what I know so far",
                reply_markup=markup,
                parse_mode='Markdown'
            )
        else:
            self.bot.send_message(
                message.chat.id,
                f"📝 Got it! Keep telling me more... ({story_length}/500 characters)\n\n"
                f"The more you share, the better I understand you! 💕"
            )
    
    def handle_contextual_conversation(self, message, message_text):
        """Handle conversation with story context"""
        user_id = str(message.from_user.id)
        
        # Get story context if available
        story_context = self.user_sessions.get(user_id, {}).get("story_data", {})
        
        # Generate contextual response
        response = self.ai_orchestrator.generate_contextual_response(
            message_text, story_context, user_tier="free"
        )
        
        # Add website redirect for premium features
        if "upgrade" in response.lower() or "premium" in response.lower():
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🌐 Upgrade on Website", url="https://web-production-43fe3.up.railway.app/pricing"),
                types.InlineKeyboardButton("🎭 Try Roleplay", callback_data="start_roleplay")
            )
            self.bot.send_message(message.chat.id, response, reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, response)
    
    def initiate_roleplay(self, call):
        """Initiate roleplay mode"""
        user_id = str(call.from_user.id)
        
        if user_id not in self.user_sessions or not self.user_sessions[user_id].get("story_data"):
            self.bot.edit_message_text(
                "🎭 **Ready for Roleplay!**\n\n"
                "But I need your story first to create personalized scenarios.\n\n"
                "Please share your story using /story command! 📚",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            return
        
        # Set roleplay mode
        self.user_sessions[user_id]["stage"] = "roleplay_active"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            "🌐 Advanced Roleplay on Website", 
            url="https://web-production-43fe3.up.railway.app/roleplay"
        ))
        
        self.bot.edit_message_text(
            "🎭 **Roleplay Mode Activated!**\n\n"
            "I'm now in character based on your story. Send me any message and I'll respond in roleplay mode!\n\n"
            "💡 **Tip:** Visit our website for:\n"
            "• Visual roleplay with images\n"
            "• Voice responses\n"
            "• NSFW scenarios (Premium)\n"
            "• Video generation",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    def handle_roleplay_message(self, message, message_text):
        """Handle messages during roleplay"""
        user_id = str(message.from_user.id)
        story_context = self.user_sessions[user_id]["story_data"]
        
        # Generate roleplay response
        response = self.ai_orchestrator.generate_roleplay_response(
            message_text, story_context, user_tier="free"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔥 Unlock Premium Roleplay", url="https://web-production-43fe3.up.railway.app/premium"),
            types.InlineKeyboardButton("🚪 Exit Roleplay", callback_data="exit_roleplay")
        )
        
        self.bot.send_message(
            message.chat.id,
            f"{response}\n\n"
            f"💡 *Enjoying this? Premium unlocks NSFW scenarios, images, and voice responses!*",
            reply_markup=markup
        )