"""
Telegram Bot Handler - Story Processing & Website Integration
"""

import logging
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from src.story.story_processor import StoryProcessor
from src.orchestrator.ai_orchestrator import AIOrchestrator

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    """Handles all Telegram bot interactions with story processing"""
    
    def __init__(self):
        self.story_processor = StoryProcessor()
        self.ai_orchestrator = AIOrchestrator()
        self.user_sessions = {}  # Store user conversation state
    
    def register_handlers(self, application: Application):
        """Register all bot handlers"""
        
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("story", self.story_command))
        application.add_handler(CommandHandler("roleplay", self.roleplay_command))
        application.add_handler(CommandHandler("plans", self.plans_command))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        logger.info("All handlers registered successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - Story-focused onboarding"""
        user = update.effective_user
        user_id = str(user.id)
        
        # Initialize user session
        self.user_sessions[user_id] = {
            "stage": "onboarding",
            "story_data": {},
            "preferences": {}
        }
        
        keyboard = [
            [InlineKeyboardButton("📚 Upload Your Story", callback_data="upload_story")],
            [InlineKeyboardButton("💭 Tell Me Your Story", callback_data="tell_story")],
            [InlineKeyboardButton("🎭 Start Roleplay", callback_data="start_roleplay")],
            [InlineKeyboardButton("🌐 Visit Website", url="https://your-railway-app.up.railway.app")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
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
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def story_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /story command"""
        keyboard = [
            [InlineKeyboardButton("📁 Upload Story File", callback_data="upload_file")],
            [InlineKeyboardButton("💬 Tell Story in Chat", callback_data="tell_chat")],
            [InlineKeyboardButton("🎙️ Voice Story", callback_data="voice_story")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📚 **Share Your Story With Me**\n\n"
            "I can process your story in multiple ways:\n\n"
            "📁 **Upload File** - Send me a document (.txt, .docx, .pdf)\n"
            "💬 **Type Here** - Tell me your story in messages\n"
            "🎙️ **Voice Message** - Record your story\n\n"
            "The more details you share, the better I understand you! 💕",
            reply_markup=reply_markup
        )
    
    async def roleplay_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /roleplay command"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.user_sessions or not self.user_sessions[user_id].get("story_data"):
            await update.message.reply_text(
                "🎭 **Let's Create Amazing Roleplays!**\n\n"
                "But first, I need to know your story to create personalized scenarios.\n\n"
                "Use /story to share your background with me! 📚"
            )
            return
        
        # Generate roleplay scenarios based on story
        scenarios = await self.story_processor.generate_roleplay_scenarios(
            self.user_sessions[user_id]["story_data"]
        )
        
        keyboard = []
        for i, scenario in enumerate(scenarios[:4]):  # Show top 4 scenarios
            keyboard.append([InlineKeyboardButton(
                f"🎭 {scenario['title']}", 
                callback_data=f"roleplay_{i}"
            )])
        
        keyboard.append([InlineKeyboardButton("🌐 More Scenarios on Website", url="https://your-railway-app.up.railway.app/roleplay")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎭 **Choose Your Roleplay Adventure:**\n\n"
            "Based on your story, here are personalized scenarios:\n\n"
            f"✨ **{scenarios[0]['title']}**\n{scenarios[0]['preview']}\n\n"
            f"🔥 **{scenarios[1]['title']}**\n{scenarios[1]['preview']}\n\n"
            "Visit our website for unlimited scenarios and premium features!",
            reply_markup=reply_markup
        )
    
    async def plans_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /plans command - Redirect to website"""
        keyboard = [
            [InlineKeyboardButton("🌐 View All Plans", url="https://your-railway-app.up.railway.app/pricing")],
            [InlineKeyboardButton("🆓 Start Free Trial", url="https://your-railway-app.up.railway.app/trial")],
            [InlineKeyboardButton("🔥 Get Premium Now", url="https://your-railway-app.up.railway.app/premium")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "💎 **Choose Your Experience Level:**\n\n"
            "🆓 **FREE** - 3 days trial, basic features\n"
            "💎 **BASIC** - ₹299/month, voice + videos\n"
            "🔥 **PRO** - ₹599/month, more generation\n"
            "👑 **PRIME** - ₹899/month, limited NSFW\n"
            "🌟 **SUPER** - ₹1299/month, more NSFW\n"
            "♾️ **LIFETIME** - ₹2999, unlimited everything\n\n"
            "**⚠️ Payment & detailed features available on website only!**",
            reply_markup=reply_markup
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages - Story processing"""
        try:
            user_id = str(update.effective_user.id)
            message_text = update.message.text
            
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
                # User is telling their story
                await self.process_story_input(update, message_text)
            
            elif session["stage"] == "roleplay_active":
                # User is in active roleplay
                await self.handle_roleplay_message(update, message_text)
            
            else:
                # Regular conversation with story context
                await self.handle_contextual_conversation(update, message_text)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Oops! Something went wrong. Please try again! 😊"
            )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads - Story files"""
        try:
            user_id = str(update.effective_user.id)
            document = update.message.document
            
            await update.message.reply_text("📚 Processing your story... Please wait! ⏳")
            
            # Download and process the document
            file = await context.bot.get_file(document.file_id)
            file_content = await self.story_processor.process_document(file, document.file_name)
            
            # Store story data
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {"stage": "story_processed", "story_data": {}, "preferences": {}}
            
            self.user_sessions[user_id]["story_data"] = file_content
            
            # Generate story analysis
            analysis = await self.story_processor.analyze_story(file_content)
            
            keyboard = [
                [InlineKeyboardButton("🎭 Start Roleplay", callback_data="start_roleplay")],
                [InlineKeyboardButton("🌐 Explore on Website", url="https://your-railway-app.up.railway.app/dashboard")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"✅ **Story Processed Successfully!**\n\n"
                f"📊 **Analysis:**\n"
                f"• **Characters:** {len(analysis.get('characters', []))}\n"
                f"• **Themes:** {', '.join(analysis.get('themes', [])[:3])}\n"
                f"• **Emotional Tone:** {analysis.get('emotional_tone', 'Mixed')}\n"
                f"• **Story Length:** {analysis.get('word_count', 0)} words\n\n"
                f"🧠 **I now understand your story and can create personalized experiences!**\n\n"
                f"What would you like to do next?",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            await update.message.reply_text(
                "❌ Sorry, I couldn't process that file. Please try uploading a .txt, .docx, or .pdf file."
            )
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages - Story narration"""
        await update.message.reply_text(
            "🎙️ **Voice Story Processing**\n\n"
            "Voice processing is available on our website with premium features!\n\n"
            "🌐 Visit our website to:\n"
            "• Upload voice stories\n"
            "• Get voice responses\n"
            "• Clone voices\n"
            "• Premium voice features"
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        data = query.data
        
        if data == "upload_story":
            await query.edit_message_text(
                "📁 **Upload Your Story File**\n\n"
                "Send me a document file (.txt, .docx, .pdf) containing your story.\n\n"
                "I'll analyze it and create personalized experiences for you! 💕"
            )
            
        elif data == "tell_story":
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {"stage": "collecting_story", "story_data": {}, "preferences": {}}
            else:
                self.user_sessions[user_id]["stage"] = "collecting_story"
            
            await query.edit_message_text(
                "💭 **Tell Me Your Story**\n\n"
                "Start typing your story, background, or any details about yourself.\n\n"
                "I'll remember everything and use it to create amazing experiences!\n\n"
                "Type as much as you want - I'm listening! 👂💕"
            )
            
        elif data == "start_roleplay":
            await self.initiate_roleplay(query)
            
        elif data.startswith("roleplay_"):
            scenario_id = int(data.split("_")[1])
            await self.start_specific_roleplay(query, scenario_id)
    
    async def process_story_input(self, update: Update, message_text: str):
        """Process story input from user"""
        user_id = str(update.effective_user.id)
        
        # Add to story data
        if "story_text" not in self.user_sessions[user_id]["story_data"]:
            self.user_sessions[user_id]["story_data"]["story_text"] = ""
        
        self.user_sessions[user_id]["story_data"]["story_text"] += f"\n{message_text}"
        
        # Analyze story so far
        story_length = len(self.user_sessions[user_id]["story_data"]["story_text"])
        
        if story_length > 500:  # Enough content to analyze
            keyboard = [
                [InlineKeyboardButton("✅ Finish Story", callback_data="finish_story")],
                [InlineKeyboardButton("➕ Continue Adding", callback_data="continue_story")],
                [InlineKeyboardButton("🎭 Start Roleplay Now", callback_data="start_roleplay")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"📚 **Story Progress: {story_length} characters**\n\n"
                f"Great! I'm learning about you. You can:\n\n"
                f"✅ **Finish** - I have enough to create experiences\n"
                f"➕ **Continue** - Add more details\n"
                f"🎭 **Roleplay** - Start with what I know so far",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                f"📝 Got it! Keep telling me more... ({story_length}/500 characters)\n\n"
                f"The more you share, the better I understand you! 💕"
            )
    
    async def handle_contextual_conversation(self, update: Update, message_text: str):
        """Handle conversation with story context"""
        user_id = str(update.effective_user.id)
        
        # Get story context if available
        story_context = self.user_sessions.get(user_id, {}).get("story_data", {})
        
        # Generate contextual response
        response = await self.ai_orchestrator.generate_contextual_response(
            message_text, story_context, user_tier="free"
        )
        
        # Add website redirect for premium features
        if "upgrade" in response.lower() or "premium" in response.lower():
            keyboard = [
                [InlineKeyboardButton("🌐 Upgrade on Website", url="https://your-railway-app.up.railway.app/pricing")],
                [InlineKeyboardButton("🎭 Try Roleplay", callback_data="start_roleplay")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(response, reply_markup=reply_markup)
        else:
            await update.message.reply_text(response)
    
    async def initiate_roleplay(self, query):
        """Initiate roleplay mode"""
        user_id = str(query.from_user.id)
        
        if user_id not in self.user_sessions or not self.user_sessions[user_id].get("story_data"):
            await query.edit_message_text(
                "🎭 **Ready for Roleplay!**\n\n"
                "But I need your story first to create personalized scenarios.\n\n"
                "Please share your story using /story command! 📚"
            )
            return
        
        # Set roleplay mode
        self.user_sessions[user_id]["stage"] = "roleplay_active"
        
        keyboard = [
            [InlineKeyboardButton("🌐 Advanced Roleplay on Website", url="https://your-railway-app.up.railway.app/roleplay")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🎭 **Roleplay Mode Activated!**\n\n"
            "I'm now in character based on your story. Send me any message and I'll respond in roleplay mode!\n\n"
            "💡 **Tip:** Visit our website for:\n"
            "• Visual roleplay with images\n"
            "• Voice responses\n"
            "• NSFW scenarios (Premium)\n"
            "• Video generation",
            reply_markup=reply_markup
        )
    
    async def handle_roleplay_message(self, update: Update, message_text: str):
        """Handle messages during roleplay"""
        user_id = str(update.effective_user.id)
        story_context = self.user_sessions[user_id]["story_data"]
        
        # Generate roleplay response
        response = await self.ai_orchestrator.generate_roleplay_response(
            message_text, story_context, user_tier="free"
        )
        
        # Add premium upsell
        keyboard = [
            [InlineKeyboardButton("🔥 Unlock Premium Roleplay", url="https://your-railway-app.up.railway.app/premium")],
            [InlineKeyboardButton("🚪 Exit Roleplay", callback_data="exit_roleplay")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"{response}\n\n"
            f"💡 *Enjoying this? Premium unlocks NSFW scenarios, images, and voice responses!*",
            reply_markup=reply_markup
        )