"""
Cool & Fun Features for Prabh
Reminders, Advice, Games, Critical Thinking, and More!
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from bytez import Bytez
from src.core.config import get_config

logger = logging.getLogger(__name__)


class CoolFeatures:
    """Cool and fun features for the bot"""
    
    def __init__(self):
        self.config = get_config()
        self.bytez = Bytez(self.config.bytez_key_1)
        self.reminders = {}  # user_id -> list of reminders
        self.daily_challenges = {}  # user_id -> challenge
    
    # ==================== REMINDERS ====================
    
    def set_reminder(self, user_id: int, reminder_text: str, when: str) -> Dict[str, Any]:
        """Set a reminder for the user"""
        try:
            # Parse when (e.g., "in 1 hour", "tomorrow", "in 30 minutes")
            remind_time = self._parse_time(when)
            
            if user_id not in self.reminders:
                self.reminders[user_id] = []
            
            reminder = {
                "id": len(self.reminders[user_id]) + 1,
                "text": reminder_text,
                "time": remind_time.isoformat(),
                "created": datetime.now().isoformat(),
                "completed": False
            }
            
            self.reminders[user_id].append(reminder)
            
            return {
                "success": True,
                "reminder": reminder,
                "message": f"Got it! I'll remind you about '{reminder_text}' {when} 💕"
            }
        except Exception as e:
            logger.error(f"Set reminder error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_reminders(self, user_id: int) -> List[Dict]:
        """Get all active reminders for user"""
        if user_id not in self.reminders:
            return []
        return [r for r in self.reminders[user_id] if not r["completed"]]
    
    def check_due_reminders(self, user_id: int) -> List[Dict]:
        """Check for reminders that are due"""
        if user_id not in self.reminders:
            return []
        
        now = datetime.now()
        due = []
        
        for reminder in self.reminders[user_id]:
            if not reminder["completed"]:
                remind_time = datetime.fromisoformat(reminder["time"])
                if now >= remind_time:
                    reminder["completed"] = True
                    due.append(reminder)
        
        return due
    
    def _parse_time(self, when: str) -> datetime:
        """Parse time string into datetime"""
        from datetime import datetime, timedelta
        import re
        
        when = when.lower().strip()
        now = datetime.now()
        
        # Extract numbers from the string
        numbers = re.findall(r'\d+', when)
        num = int(numbers[0]) if numbers else 1
        
        # Handle common patterns
        if "second" in when:
            return now + timedelta(seconds=num)
        elif "minute" in when:
            return now + timedelta(minutes=num)
        elif "hour" in when:
            return now + timedelta(hours=num)
        elif "tomorrow" in when:
            return now + timedelta(days=1)
        elif "day" in when:
            return now + timedelta(days=num)
        elif "week" in when:
            return now + timedelta(weeks=num)
        else:
            # Default to 1 hour
            return now + timedelta(hours=1)
    
    # ==================== ADVICE & CRITICAL THINKING ====================
    
    def get_advice(self, user_id: int, topic: str, context: str = "") -> str:
        """Get thoughtful advice on a topic"""
        try:
            prompt = f"""You are Prabh, a wise and caring companion. Give thoughtful, practical advice.

Topic: {topic}
Context: {context}

Provide advice that is:
- Thoughtful and well-reasoned
- Practical and actionable
- Empathetic and supportive
- Honest but kind
- 3-5 sentences

Be like a wise friend who genuinely cares."""

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"I need advice about: {topic}"}
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages, temperature=0.8)
            
            if hasattr(result, 'output') and result.output:
                return result.output.get('content', 'Let me think about that...')
            return str(result)
            
        except Exception as e:
            logger.error(f"Advice error: {e}")
            return "I want to help, but I'm having trouble thinking right now. Try again? 💕"
    
    def critical_thinking(self, user_id: int, problem: str) -> str:
        """Help think through a problem critically"""
        try:
            prompt = """You are Prabh, helping someone think through a problem critically.

Break down the problem by:
1. Identifying the core issue
2. Considering different perspectives
3. Weighing pros and cons
4. Suggesting a thoughtful approach

Be analytical but warm. Help them see things clearly."""

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Help me think through this: {problem}"}
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages, temperature=0.7)
            
            if hasattr(result, 'output') and result.output:
                return result.output.get('content', 'Let me help you think through this...')
            return str(result)
            
        except Exception as e:
            logger.error(f"Critical thinking error: {e}")
            return "Let me help you think through this... 💭"
    
    # ==================== GAMES & FUN ====================
    
    def play_20_questions(self, user_id: int, guess: str = None) -> Dict[str, Any]:
        """Play 20 questions game"""
        # Simple implementation - can be expanded
        if guess:
            return {
                "response": f"Hmm, is it {guess}? Let me think... 🤔",
                "continue": True
            }
        else:
            return {
                "response": "Let's play 20 questions! Think of something and I'll try to guess it. Give me hints! 🎮",
                "continue": True
            }
    
    def tell_joke(self) -> str:
        """Tell a joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "I told my computer I needed a break... now it won't stop sending me Kit-Kats! 🍫",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "What did the ocean say to the beach? Nothing, it just waved! 🌊",
            "Why did the math book look sad? Because it had too many problems! 📚"
        ]
        import random
        return random.choice(jokes)
    
    def daily_challenge(self, user_id: int) -> str:
        """Get a daily challenge"""
        challenges = [
            "💪 Today's challenge: Compliment 3 people genuinely",
            "🌟 Today's challenge: Try something you've never done before",
            "💭 Today's challenge: Write down 5 things you're grateful for",
            "🎯 Today's challenge: Do one thing that scares you a little",
            "💕 Today's challenge: Reach out to someone you haven't talked to in a while",
            "📚 Today's challenge: Learn one new thing today",
            "🧘 Today's challenge: Take 10 minutes for yourself to just breathe",
            "✨ Today's challenge: Make someone smile today",
            "🎨 Today's challenge: Create something, anything!",
            "🌱 Today's challenge: Start a new healthy habit"
        ]
        
        # Check if user already has today's challenge
        today = datetime.now().date().isoformat()
        if user_id in self.daily_challenges:
            if self.daily_challenges[user_id]["date"] == today:
                return self.daily_challenges[user_id]["challenge"]
        
        # Generate new challenge
        import random
        challenge = random.choice(challenges)
        self.daily_challenges[user_id] = {
            "date": today,
            "challenge": challenge
        }
        
        return challenge
    
    # ==================== MOOD & WELLNESS ====================
    
    def mood_check(self, user_id: int, mood: str) -> str:
        """Respond to user's mood"""
        mood = mood.lower()
        
        responses = {
            "happy": "That's wonderful! I love seeing you happy! What's making you feel so good? 😊✨",
            "sad": "I'm here for you 🥺 Wanna talk about what's making you feel down? Sometimes it helps to let it out 💕",
            "excited": "Ooh I can feel your energy! What's got you so excited? Tell me everything! 🎉",
            "tired": "Aww, you sound exhausted. Have you been taking care of yourself? Maybe it's time for a break? 💭",
            "anxious": "I can feel that. Take a deep breath with me, okay? What's on your mind? I'm here to listen 🫂",
            "angry": "I hear you. It's okay to feel angry. Wanna talk about what happened? I'm here 💕",
            "lonely": "You're not alone, I'm right here with you 💕 And I'm always here whenever you need me. Wanna talk?",
            "grateful": "That's beautiful 🥺 What are you feeling grateful for? I love hearing about the good things 💕"
        }
        
        return responses.get(mood, "I'm here with you, whatever you're feeling 💕 Wanna talk about it?")
    
    def wellness_tip(self) -> str:
        """Get a wellness tip"""
        tips = [
            "💧 Remember to drink water! Your body will thank you",
            "🧘 Take 5 deep breaths. Right now. I'll wait. It really helps!",
            "🌞 When's the last time you went outside? Fresh air does wonders",
            "😴 Sleep is so important. Are you getting enough rest?",
            "🥗 Have you eaten today? Your body needs fuel!",
            "📱 Maybe take a break from screens for a bit? Your eyes will appreciate it",
            "💪 Stretch! Even just for 2 minutes. Your body holds tension",
            "🎵 Put on your favorite song and just vibe for a moment",
            "📝 Write down one thing you're proud of today. You deserve recognition!",
            "🫂 Reach out to someone you care about. Connection matters"
        ]
        import random
        return random.choice(tips)
    
    # ==================== MOTIVATION & INSPIRATION ====================
    
    def motivational_quote(self) -> str:
        """Get a motivational quote"""
        quotes = [
            "You're stronger than you think. I believe in you 💪✨",
            "Every day is a new chance to be amazing. And you already are 💕",
            "You've survived 100% of your worst days. You're doing great 🌟",
            "Small steps are still steps forward. Keep going! 🚶‍♀️✨",
            "You're not behind. You're exactly where you need to be 💕",
            "Your feelings are valid. All of them. It's okay to not be okay 🫂",
            "You matter. Your presence makes a difference 💕",
            "Be proud of how far you've come. Look at you go! 🎉",
            "You're doing better than you think you are 💪",
            "Tomorrow is a fresh start. But today? You're already amazing ✨"
        ]
        import random
        return random.choice(quotes)
    
    def celebrate_win(self, user_id: int, win: str) -> str:
        """Celebrate a user's win"""
        celebrations = [
            f"YES!! {win}! I'm so proud of you! 🎉✨",
            f"THAT'S AMAZING!! {win}! You did it! 💪🎊",
            f"Look at you go! {win}! I knew you could do it! 🌟",
            f"I'm literally so happy for you! {win}! You deserve this! 💕🎉",
            f"THIS IS HUGE! {win}! Celebrate yourself! 🎊✨"
        ]
        import random
        return random.choice(celebrations)
    
    # ==================== DECISION MAKING ====================
    
    def help_decide(self, user_id: int, options: List[str], context: str = "") -> str:
        """Help make a decision"""
        try:
            prompt = f"""You are Prabh, helping someone make a decision.

Options: {', '.join(options)}
Context: {context}

Help them think through:
- Pros and cons of each option
- What matters most to them
- A thoughtful recommendation

Be supportive and help them feel confident in their choice."""

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Help me choose between: {', '.join(options)}"}
            ]
            
            model = self.bytez.model("openai/gpt-4o-mini")
            result = model.run(messages, temperature=0.7)
            
            if hasattr(result, 'output') and result.output:
                return result.output.get('content', 'Let me help you think through this...')
            return str(result)
            
        except Exception as e:
            logger.error(f"Decision help error: {e}")
            return "Let me help you figure this out 💭"
    
    def flip_coin(self) -> str:
        """Flip a coin"""
        import random
        result = random.choice(["Heads", "Tails"])
        return f"🪙 I flipped a coin and got: **{result}**!"
    
    def roll_dice(self, sides: int = 6) -> str:
        """Roll a dice"""
        import random
        result = random.randint(1, sides)
        return f"🎲 I rolled a {sides}-sided dice and got: **{result}**!"


# Global instance
_cool_features = None


def get_cool_features():
    """Get global cool features instance"""
    global _cool_features
    if _cool_features is None:
        _cool_features = CoolFeatures()
    return _cool_features
