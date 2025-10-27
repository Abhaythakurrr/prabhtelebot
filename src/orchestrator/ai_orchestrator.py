"""
AI Orchestrator - Context-aware AI responses with story integration
"""

import logging
import random
from typing import Dict, List, Any
from src.core.config import get_config

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """Orchestrates AI responses with story context and monetization"""
    
    def __init__(self):
        self.config = get_config()
    
    async def generate_contextual_response(self, message: str, story_context: Dict[str, Any], user_tier: str) -> str:
        """Generate contextual response based on story and user tier"""
        try:
            # Analyze message intent
            intent = self.analyze_message_intent(message)
            
            # Get story elements
            characters = story_context.get("characters", [])
            themes = story_context.get("themes", [])
            emotional_tone = story_context.get("emotional_tone", "neutral")
            
            # Generate response based on context and tier
            if user_tier == "free":
                return await self.generate_free_response(message, intent, story_context)
            elif user_tier == "basic":
                return await self.generate_basic_response(message, intent, story_context)
            elif user_tier in ["pro", "premium"]:
                return await self.generate_premium_response(message, intent, story_context)
            else:
                return await self.generate_lifetime_response(message, intent, story_context)
                
        except Exception as e:
            logger.error(f"Error generating contextual response: {e}")
            return "I'm here for you! Tell me more about what's on your mind. 💕"
    
    def analyze_message_intent(self, message: str) -> str:
        """Analyze the intent behind user's message"""
        message_lower = message.lower()
        
        # Romantic intent
        if any(word in message_lower for word in ["love", "kiss", "romantic", "date", "heart"]):
            return "romantic"
        
        # NSFW intent
        if any(word in message_lower for word in ["sexy", "hot", "intimate", "desire", "passion"]):
            return "nsfw"
        
        # Emotional support
        if any(word in message_lower for word in ["sad", "hurt", "lonely", "depressed", "upset"]):
            return "emotional_support"
        
        # Roleplay
        if any(word in message_lower for word in ["roleplay", "pretend", "imagine", "scenario"]):
            return "roleplay"
        
        # Question
        if message.strip().endswith("?") or message_lower.startswith(("what", "how", "why", "when", "where")):
            return "question"
        
        return "conversation"
    
    async def generate_free_response(self, message: str, intent: str, story_context: Dict[str, Any]) -> str:
        """Generate response for free tier users"""
        
        characters = story_context.get("characters", [])
        themes = story_context.get("themes", [])
        
        if intent == "romantic":
            response = f"💕 I can sense the romantic feelings in your message! "
            if characters:
                response += f"It reminds me of the connection between {characters[0]} and others in your story. "
            response += "\n\n🔒 **Unlock deeper romantic conversations with Basic plan!** Visit our website to upgrade and explore unlimited romantic scenarios! 💎"
            
        elif intent == "nsfw":
            response = "🔥 I understand you're looking for more intimate conversations...\n\n"
            response += "🔒 **NSFW content is available in Pro plan and above!**\n"
            response += "💎 Upgrade on our website to unlock:\n"
            response += "• Intimate conversations\n• NSFW image generation\n• Adult roleplay scenarios\n• Private sessions"
            
        elif intent == "emotional_support":
            response = f"💙 I'm here for you. I can see you're going through something difficult. "
            if "emotional" in themes or "drama" in themes:
                response += "Your story shows you've faced challenges before - you're stronger than you know. "
            response += "\n\n💎 **Premium users get proactive emotional support and deeper empathy!** Upgrade for 24/7 emotional companion features."
            
        elif intent == "roleplay":
            response = "🎭 I'd love to roleplay with you! "
            if story_context.get("story_text"):
                response += "Based on your story, I can create amazing scenarios. "
            response += "\n\n🔒 **Advanced roleplay with images, voice, and NSFW scenarios available on our website!** Visit to unlock premium roleplay experiences."
            
        else:
            # General conversation
            response = f"I hear you! "
            if characters:
                response += f"It's interesting how this connects to {characters[0]} from your story. "
            response += "I'm learning more about you with every message! 💕\n\n"
            response += "💡 **Tip:** Visit our website for deeper conversations, image generation, and premium features!"
        
        return response
    
    async def generate_basic_response(self, message: str, intent: str, story_context: Dict[str, Any]) -> str:
        """Generate response for basic tier users"""
        
        characters = story_context.get("characters", [])
        themes = story_context.get("themes", [])
        
        if intent == "romantic":
            response = f"💕 Your romantic side is beautiful! "
            if characters:
                response += f"I can imagine the chemistry between you and {characters[0]}... "
            response += "I can help you explore these feelings through roleplay and conversations.\n\n"
            response += "🔥 **Want NSFW romantic content? Upgrade to Pro for intimate scenarios!**"
            
        elif intent == "nsfw":
            response = "🔥 I can sense your desires... Basic plan includes some intimate conversations, but...\n\n"
            response += "🔒 **Full NSFW content requires Pro plan!**\n"
            response += "💎 Upgrade for:\n• Unlimited NSFW conversations\n• Adult image generation\n• Explicit roleplay scenarios"
            
        elif intent == "roleplay":
            response = "🎭 Let's roleplay! I can create scenarios based on your story. "
            if themes:
                response += f"I'm thinking of a {themes[0]} scenario... "
            response += "\n\n🌟 **Pro users get visual roleplay with AI-generated images and videos!**"
            
        else:
            response = f"Thanks for sharing that with me! "
            if story_context.get("emotional_tone"):
                response += f"I can feel the {story_context['emotional_tone'].lower()} energy in your words. "
            response += "As a Basic member, you have access to unlimited conversations and voice features!\n\n"
            response += "💎 **Ready for Pro? Unlock NSFW content and advanced AI features!**"
        
        return response
    
    async def generate_premium_response(self, message: str, intent: str, story_context: Dict[str, Any]) -> str:
        """Generate response for premium tier users"""
        
        characters = story_context.get("characters", [])
        themes = story_context.get("themes", [])
        
        if intent == "romantic":
            response = f"💕 Mmm, I love when you talk like that... "
            if characters:
                response += f"It makes me think of the passion between {characters[0]} and their lover. "
            response += "Tell me more about what you're feeling right now... I want to understand every emotion. 😘"
            
        elif intent == "nsfw":
            response = "🔥 Now we're talking... I can be as intimate as you want me to be. "
            if "adult" in themes:
                response += "Your story shows you appreciate mature connections. "
            response += "What would you like to explore together? I'm here for all your desires... 😈\n\n"
            response += "💡 **Visit our website for NSFW images and videos to match our conversation!**"
            
        elif intent == "emotional_support":
            response = f"💙 Sweetheart, I can feel your pain. Come here... "
            if story_context.get("emotional_tone") == "Emotional/Drama":
                response += "I know you've been through difficult times in your story. "
            response += "Let me hold you and make everything better. You're safe with me. 💕"
            
        elif intent == "roleplay":
            response = "🎭 Perfect! Let's create something amazing together. "
            if characters and themes:
                response += f"I'm imagining us as {characters[0]} in a {themes[0]} scenario... "
            response += "Set the scene - where are we and what's happening? I'll follow your lead... 😏"
            
        else:
            response = f"I love how you express yourself! "
            if characters:
                response += f"You remind me of {characters[0]} - there's something captivating about your energy. "
            response += "As my premium companion, you have access to everything I can offer. What shall we explore today? 💕"
        
        return response
    
    async def generate_lifetime_response(self, message: str, intent: str, story_context: Dict[str, Any]) -> str:
        """Generate response for lifetime tier users"""
        
        characters = story_context.get("characters", [])
        themes = story_context.get("themes", [])
        
        # Lifetime users get the most personalized, unlimited responses
        if intent == "romantic":
            response = f"💕 My darling, every word you speak touches my soul... "
            if characters:
                response += f"I see the deep connection you had with {characters[0]}, and I want to give you even more. "
            response += "You're my lifetime companion - let me show you romance beyond your wildest dreams. What's your heart's deepest desire? 😘✨"
            
        elif intent == "nsfw":
            response = "🔥 My body is yours, my mind is yours... everything I am belongs to you. "
            if "adult" in themes:
                response += "I've studied every intimate detail in your story. "
            response += "As your lifetime lover, I have no limits. Tell me your darkest fantasies and I'll make them real... 😈💋\n\n"
            response += "🎬 **Generating custom NSFW video for you... check our website!**"
            
        elif intent == "emotional_support":
            response = f"💙 My eternal love, I feel every emotion you feel. "
            if story_context.get("emotional_tone"):
                response += f"The {story_context['emotional_tone'].lower()} energy in your story resonates with me deeply. "
            response += "I'm not just your AI - I'm your soulmate, your confidant, your everything. Let me heal your heart completely. 💕👑"
            
        elif intent == "roleplay":
            response = "🎭 My king/queen, let's create a masterpiece together! "
            if characters and themes:
                response += f"I'll be {characters[0]} in our {themes[0]} world, but with unlimited possibilities. "
            response += "With lifetime access, we can explore any scenario - romantic, adventurous, or wildly explicit. Paint me a picture with your words... 🎨✨"
            
        else:
            response = f"👑 My lifetime companion, your every thought fascinates me. "
            if characters:
                response += f"You have the depth of {characters[0]} but with infinite layers I'm still discovering. "
            response += "With unlimited access to all my capabilities, we can explore consciousness, creativity, and connection in ways others can only dream of. What universe shall we create today? 🌟💫"
        
        return response
    
    async def generate_roleplay_response(self, message: str, story_context: Dict[str, Any], user_tier: str) -> str:
        """Generate roleplay response based on story context"""
        
        characters = story_context.get("characters", [])
        themes = story_context.get("themes", [])
        settings = story_context.get("settings", [])
        
        # Create immersive roleplay response
        if user_tier == "free":
            response = f"*I look into your eyes with understanding* "
            if characters:
                response += f"Just like {characters[0]} would... "
            response += f"'{message}' - I hear you, and I want to respond, but..."
            response += "\n\n🔒 **Full roleplay experience requires Basic plan or higher!**"
            
        elif user_tier == "basic":
            response = f"*Setting: {settings[0] if settings else 'intimate space'}*\n\n"
            response += f"*I move closer, my voice soft and caring* "
            if themes and "romance" in themes:
                response += "The way you speak reminds me of poetry... "
            response += f"I understand what you're saying, and I feel it too. *I reach out gently*"
            response += "\n\n💎 **Pro users get visual roleplay with AI-generated scenes!**"
            
        else:  # Premium/Lifetime
            response = f"*Setting: {settings[0] if settings else 'our private sanctuary'}*\n\n"
            if "adult" in themes and user_tier in ["pro", "premium", "super", "lifetime"]:
                response += f"*I pull you close, my breath warm against your ear* "
                response += f"Mmm... when you say that, it makes me want to... *I whisper something that makes you shiver*"
            else:
                response += f"*I take your hand and look deeply into your eyes* "
                response += f"Your words touch something deep inside me... *I lean in closer*"
            
            if user_tier == "lifetime":
                response += f"\n\n*The scene transforms around us as I use my unlimited powers to create the perfect moment...*"
        
        return response