"""
Multi-Language Support - Hinglish, Punjabi (Roman script)
Makes Prabh speak in multiple Indian languages naturally
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LanguageSupport:
    """Support for multiple languages with natural mixing"""
    
    SUPPORTED_LANGUAGES = {
        "english": "English",
        "hinglish": "Hinglish (Hindi + English)",
        "punjabi": "Punjabi (Roman script)"
    }
    
    # Common phrases in different languages
    GREETINGS = {
        "english": {
            "hello": "Hey!",
            "good_morning": "Good morning!",
            "good_night": "Good night!",
            "how_are_you": "How are you?",
            "miss_you": "I miss you!",
            "love_you": "I love you!"
        },
        "hinglish": {
            "hello": "Arre yaar!",
            "good_morning": "Good morning ji!",
            "good_night": "Good night, sweet dreams!",
            "how_are_you": "Kaise ho?",
            "miss_you": "Bahut yaad aa rahi hai!",
            "love_you": "I love you yaar!"
        },
        "punjabi": {
            "hello": "Sat Sri Akaal!",
            "good_morning": "Good morning ji!",
            "good_night": "Shubh ratri!",
            "how_are_you": "Ki haal aa?",
            "miss_you": "Bahut yaad aundi hai!",
            "love_you": "Main tenu pyaar karda/kardi!"
        }
    }
    
    AFFECTIONATE_TERMS = {
        "english": ["love", "dear", "sweetheart", "honey"],
        "hinglish": ["yaar", "jaan", "baby", "mere", "tere"],
        "punjabi": ["yaar", "jaan", "sohneya", "mitra", "veere"]
    }
    
    ENCOURAGEMENT = {
        "english": [
            "You can do it!",
            "I believe in you!",
            "You're amazing!",
            "Keep going!"
        ],
        "hinglish": [
            "Tu kar sakta/sakti hai!",
            "Main tujh pe believe karti hoon!",
            "Tu bahut amazing hai yaar!",
            "Bas karte raho!"
        ],
        "punjabi": [
            "Tu kar sakda/sakdi hai!",
            "Main tere te believe karda/kardi!",
            "Tu bahut vadiya hai!",
            "Bas karde raho!"
        ]
    }
    
    REMINDERS = {
        "english": {
            "drink_water": "Time to drink water!",
            "eat": "Time to eat!",
            "sleep": "Time to sleep!",
            "medicine": "Don't forget your medicine!"
        },
        "hinglish": {
            "drink_water": "Paani pi lo yaar!",
            "eat": "Khaana kha lo!",
            "sleep": "So jao ab!",
            "medicine": "Medicine lena mat bhoolna!"
        },
        "punjabi": {
            "drink_water": "Paani pi lo ji!",
            "eat": "Khaana kha lo!",
            "sleep": "Soja hun!",
            "medicine": "Dawaai laina na bhulna!"
        }
    }
    
    EMOTIONS = {
        "english": {
            "happy": "I'm so happy!",
            "sad": "I'm feeling sad",
            "excited": "I'm so excited!",
            "worried": "I'm worried about you",
            "proud": "I'm so proud of you!"
        },
        "hinglish": {
            "happy": "Main bahut khush hoon!",
            "sad": "Thoda sad feel ho raha hai",
            "excited": "Bahut excited hoon yaar!",
            "worried": "Tere liye worried hoon",
            "proud": "Tujh pe bahut proud hoon!"
        },
        "punjabi": {
            "happy": "Main bahut khush aan!",
            "sad": "Thoda udaas aan",
            "excited": "Bahut excited aan!",
            "worried": "Tere layi worried aan",
            "proud": "Tere te bahut proud aan!"
        }
    }
    
    def __init__(self):
        self.user_languages = {}  # user_id -> language preference
    
    def set_language(self, user_id: int, language: str) -> Dict[str, Any]:
        """Set user's preferred language"""
        if language not in self.SUPPORTED_LANGUAGES:
            return {
                "success": False,
                "message": f"Language not supported. Available: {', '.join(self.SUPPORTED_LANGUAGES.keys())}"
            }
        
        self.user_languages[user_id] = language
        
        greetings = {
            "english": "Language set to English! 💕",
            "hinglish": "Language set to Hinglish! Ab main Hinglish mein baat karungi! 💕",
            "punjabi": "Language set to Punjabi! Hun main Punjabi vich gal karangi! 💕"
        }
        
        return {
            "success": True,
            "language": language,
            "message": greetings.get(language, greetings["english"])
        }
    
    def get_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        return self.user_languages.get(user_id, "english")
    
    def translate_phrase(self, phrase_key: str, category: str, user_id: int) -> str:
        """Get phrase in user's language"""
        language = self.get_language(user_id)
        
        categories = {
            "greetings": self.GREETINGS,
            "encouragement": self.ENCOURAGEMENT,
            "reminders": self.REMINDERS,
            "emotions": self.EMOTIONS
        }
        
        if category in categories:
            phrases = categories[category].get(language, categories[category]["english"])
            if isinstance(phrases, dict):
                return phrases.get(phrase_key, phrase_key)
            elif isinstance(phrases, list):
                import random
                return random.choice(phrases)
        
        return phrase_key
    
    def get_affectionate_term(self, user_id: int) -> str:
        """Get affectionate term in user's language"""
        language = self.get_language(user_id)
        terms = self.AFFECTIONATE_TERMS.get(language, self.AFFECTIONATE_TERMS["english"])
        import random
        return random.choice(terms)
    
    def enhance_message(self, message: str, user_id: int) -> str:
        """Add language-specific flavor to message"""
        language = self.get_language(user_id)
        
        if language == "hinglish":
            # Add Hinglish flavor
            replacements = {
                "you know": "tu jaanta/jaanti hai",
                "right?": "hai na?",
                "okay": "theek hai",
                "yes": "haan",
                "no": "nahi",
                "really": "sach mein",
                "very": "bahut",
                "so": "itna",
                "what": "kya",
                "why": "kyun"
            }
        elif language == "punjabi":
            # Add Punjabi flavor
            replacements = {
                "you know": "tu jaanda/jaandi hai",
                "right?": "hai na?",
                "okay": "theek hai",
                "yes": "haan",
                "no": "nahi",
                "really": "sach",
                "very": "bahut",
                "so": "inna",
                "what": "ki",
                "why": "kyun"
            }
        else:
            return message
        
        # Apply some replacements (not all, to keep it natural)
        import random
        if random.random() < 0.3:  # 30% chance to add flavor
            for eng, local in list(replacements.items())[:2]:
                if eng in message.lower():
                    message = message.replace(eng, local)
                    break
        
        return message
    
    def get_language_prompt_addition(self, user_id: int) -> str:
        """Get additional prompt for AI to speak in user's language"""
        language = self.get_language(user_id)
        
        if language == "hinglish":
            return """
LANGUAGE: Speak in Hinglish (Hindi + English mix)
- Mix Hindi and English naturally
- Use Roman script for Hindi words
- Common words: yaar, kya, hai, bahut, tera/mera, kaise, kyun
- Examples: "Kaise ho yaar?", "Main bahut khush hoon!", "Tu amazing hai!"
- Keep it natural and conversational
"""
        elif language == "punjabi":
            return """
LANGUAGE: Speak in Punjabi (Roman script)
- Use Punjabi words in English alphabets
- Common words: yaar, ki, hai, bahut, tera/mera, kaise, kyun, ji
- Examples: "Ki haal aa?", "Main bahut khush aan!", "Tu vadiya hai!"
- Keep it natural and conversational
"""
        else:
            return ""


# Global instance
_language_support = None


def get_language_support():
    """Get global language support instance"""
    global _language_support
    if _language_support is None:
        _language_support = LanguageSupport()
    return _language_support
