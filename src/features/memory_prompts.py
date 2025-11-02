"""
Memory Prompts - AI asks questions to build deeper memories
"""

import logging
from typing import List
from src.core.user_manager import get_user_manager

logger = logging.getLogger(__name__)


class MemoryPrompts:
    """Generate prompts to help users share more memories"""
    
    PROMPT_CATEGORIES = {
        "first_meeting": [
            "Tell me about the first time you met them. What do you remember?",
            "What was your first impression of them?",
            "Where did you first meet? What was the setting like?"
        ],
        "favorite_moments": [
            "What's your favorite memory with them?",
            "Tell me about a time they made you laugh really hard.",
            "What's something special they did that you'll never forget?"
        ],
        "personality": [
            "What made them unique? What set them apart?",
            "How did they make you feel when you were together?",
            "What's something they always used to say?"
        ],
        "daily_life": [
            "What did a typical day with them look like?",
            "What activities did you enjoy doing together?",
            "What was their favorite thing to do?"
        ],
        "special_occasions": [
            "Tell me about a birthday or celebration you shared.",
            "What gifts did they give you? What did they mean?",
            "Describe a holiday you spent together."
        ],
        "little_things": [
            "What small habit of theirs do you miss most?",
            "What did they smell like? What perfume/cologne?",
            "What was their favorite food? Did you cook together?"
        ],
        "dreams": [
            "What dreams did you share together?",
            "What plans did you have for the future?",
            "What did they want to achieve in life?"
        ]
    }
    
    def __init__(self):
        self.user_manager = get_user_manager()
        self.asked_prompts = {}  # user_id: [asked_prompts]
    
    def get_next_prompt(self, user_id: int) -> str:
        """Get next memory prompt for user"""
        if user_id not in self.asked_prompts:
            self.asked_prompts[user_id] = []
        
        asked = self.asked_prompts[user_id]
        
        # Find a category with unanswered prompts
        for category, prompts in self.PROMPT_CATEGORIES.items():
            for prompt in prompts:
                if prompt not in asked:
                    self.asked_prompts[user_id].append(prompt)
                    return prompt
        
        # All prompts asked, start over
        self.asked_prompts[user_id] = []
        return self.PROMPT_CATEGORIES["favorite_moments"][0]
    
    def get_category_prompts(self, category: str) -> List[str]:
        """Get all prompts for a category"""
        return self.PROMPT_CATEGORIES.get(category, [])


# Global instance
_memory_prompts = None


def get_memory_prompts():
    """Get global memory prompts"""
    global _memory_prompts
    if _memory_prompts is None:
        _memory_prompts = MemoryPrompts()
    return _memory_prompts
