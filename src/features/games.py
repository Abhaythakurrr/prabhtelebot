"""
Interactive Games Module - Real Playable Games
Not just random outputs, but actual engaging gameplay!
"""

import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class GamesEngine:
    """Complete games engine with multiple playable games"""
    
    def __init__(self):
        self.active_games = {}  # user_id -> game_state
        self.game_stats = {}    # user_id -> stats
    
    # ==================== WORD GUESSING GAME ====================
    
    WORD_CATEGORIES = {
        "animals": ["elephant", "giraffe", "penguin", "dolphin", "butterfly", "kangaroo"],
        "countries": ["japan", "brazil", "egypt", "canada", "australia", "france"],
        "movies": ["inception", "avatar", "titanic", "frozen", "gladiator", "interstellar"],
        "food": ["pizza", "sushi", "burger", "pasta", "chocolate", "strawberry"],
        "emotions": ["happiness", "excitement", "curiosity", "gratitude", "serenity"]
    }
    
    def start_word_game(self, user_id: int, category: str = None) -> Dict[str, Any]:
        """Start word guessing game"""
        if not category:
            category = random.choice(list(self.WORD_CATEGORIES.keys()))
        
        word = random.choice(self.WORD_CATEGORIES[category])
        
        game_state = {
            "type": "word_guess",
            "word": word,
            "category": category,
            "guessed_letters": [],
            "wrong_guesses": 0,
            "max_wrong": 6,
            "started_at": datetime.now().isoformat()
        }
        
        self.active_games[user_id] = game_state
        
        display = self._get_word_display(word, [])
        
        return {
            "success": True,
            "message": f"🎮 *Word Guessing Game!*\n\n"
                      f"Category: *{category.title()}*\n"
                      f"Word: `{display}`\n"
                      f"Wrong guesses: {0}/{6}\n\n"
                      f"Guess a letter! Type any letter A-Z 💕",
            "display": display,
            "category": category
        }
    
    def guess_letter(self, user_id: int, letter: str) -> Dict[str, Any]:
        """Process letter guess"""
        if user_id not in self.active_games:
            return {"success": False, "message": "No active game! Start one first 🎮"}
        
        game = self.active_games[user_id]
        if game["type"] != "word_guess":
            return {"success": False, "message": "Wrong game type!"}
        
        letter = letter.lower()
        
        if letter in game["guessed_letters"]:
            return {
                "success": False,
                "message": f"You already guessed '{letter}'! Try another letter 😊"
            }
        
        game["guessed_letters"].append(letter)
        word = game["word"]
        
        if letter in word:
            # Correct guess!
            display = self._get_word_display(word, game["guessed_letters"])
            
            if "_" not in display:
                # Won!
                self._update_stats(user_id, "word_guess", won=True)
                del self.active_games[user_id]
                return {
                    "success": True,
                    "won": True,
                    "message": f"🎉 *YOU WON!*\n\n"
                              f"The word was: *{word.upper()}*\n"
                              f"Great job! You're amazing! 💕✨"
                }
            else:
                return {
                    "success": True,
                    "message": f"✅ Good guess!\n\n"
                              f"Word: `{display}`\n"
                              f"Wrong guesses: {game['wrong_guesses']}/{game['max_wrong']}\n\n"
                              f"Keep going! 💪"
                }
        else:
            # Wrong guess
            game["wrong_guesses"] += 1
            display = self._get_word_display(word, game["guessed_letters"])
            
            if game["wrong_guesses"] >= game["max_wrong"]:
                # Lost
                self._update_stats(user_id, "word_guess", won=False)
                del self.active_games[user_id]
                return {
                    "success": True,
                    "won": False,
                    "message": f"😢 *Game Over!*\n\n"
                              f"The word was: *{word.upper()}*\n"
                              f"Don't worry, wanna try again? 💕"
                }
            else:
                return {
                    "success": True,
                    "message": f"❌ Not in the word!\n\n"
                              f"Word: `{display}`\n"
                              f"Wrong guesses: {game['wrong_guesses']}/{game['max_wrong']}\n\n"
                              f"Keep trying! 💕"
                }
    
    def _get_word_display(self, word: str, guessed: List[str]) -> str:
        """Get display string for word"""
        return " ".join([letter if letter in guessed else "_" for letter in word])
    
    # ==================== TRIVIA QUIZ ====================
    
    TRIVIA_QUESTIONS = {
        "general": [
            {"q": "What is the capital of France?", "a": ["paris"], "hint": "City of Love"},
            {"q": "How many continents are there?", "a": ["7", "seven"], "hint": "More than 5"},
            {"q": "What is the largest ocean?", "a": ["pacific"], "hint": "Starts with P"},
        ],
        "science": [
            {"q": "What planet is known as the Red Planet?", "a": ["mars"], "hint": "Named after Roman god"},
            {"q": "What is H2O?", "a": ["water"], "hint": "You drink it every day"},
            {"q": "How many bones in human body?", "a": ["206"], "hint": "More than 200"},
        ],
        "movies": [
            {"q": "Who played Iron Man?", "a": ["robert downey jr", "rdj"], "hint": "RDJ"},
            {"q": "What year was Titanic released?", "a": ["1997"], "hint": "Late 90s"},
        ]
    }
    
    def start_trivia(self, user_id: int, category: str = "general") -> Dict[str, Any]:
        """Start trivia quiz"""
        questions = self.TRIVIA_QUESTIONS.get(category, self.TRIVIA_QUESTIONS["general"])
        question = random.choice(questions)
        
        game_state = {
            "type": "trivia",
            "category": category,
            "question": question,
            "score": 0,
            "total": 0,
            "started_at": datetime.now().isoformat()
        }
        
        self.active_games[user_id] = game_state
        
        return {
            "success": True,
            "message": f"🧠 *Trivia Time!*\n\n"
                      f"Category: *{category.title()}*\n\n"
                      f"❓ {question['q']}\n\n"
                      f"Type your answer! (or 'hint' for a clue) 💡"
        }
    
    def answer_trivia(self, user_id: int, answer: str) -> Dict[str, Any]:
        """Check trivia answer"""
        if user_id not in self.active_games:
            return {"success": False, "message": "No active game!"}
        
        game = self.active_games[user_id]
        if game["type"] != "trivia":
            return {"success": False, "message": "Wrong game type!"}
        
        answer = answer.lower().strip()
        
        if answer == "hint":
            return {
                "success": True,
                "message": f"💡 *Hint:* {game['question']['hint']}\n\nTry again! 😊"
            }
        
        correct_answers = game["question"]["a"]
        game["total"] += 1
        
        if any(ans in answer for ans in correct_answers):
            # Correct!
            game["score"] += 1
            
            # Get next question
            questions = self.TRIVIA_QUESTIONS.get(game["category"], self.TRIVIA_QUESTIONS["general"])
            next_q = random.choice(questions)
            game["question"] = next_q
            
            return {
                "success": True,
                "correct": True,
                "message": f"✅ *Correct!*\n\n"
                          f"Score: {game['score']}/{game['total']} 🎉\n\n"
                          f"Next question:\n"
                          f"❓ {next_q['q']}"
            }
        else:
            # Wrong
            correct = correct_answers[0].title()
            return {
                "success": True,
                "correct": False,
                "message": f"❌ Not quite!\n\n"
                          f"The answer was: *{correct}*\n"
                          f"Score: {game['score']}/{game['total']}\n\n"
                          f"Wanna try another? Type 'next' 💕"
            }
    
    # ==================== NUMBER GUESSING ====================
    
    def start_number_game(self, user_id: int, max_num: int = 100) -> Dict[str, Any]:
        """Start number guessing game"""
        number = random.randint(1, max_num)
        
        game_state = {
            "type": "number_guess",
            "number": number,
            "max": max_num,
            "guesses": 0,
            "max_guesses": 7,
            "started_at": datetime.now().isoformat()
        }
        
        self.active_games[user_id] = game_state
        
        return {
            "success": True,
            "message": f"🎲 *Number Guessing Game!*\n\n"
                      f"I'm thinking of a number between 1 and {max_num}!\n"
                      f"You have {7} guesses.\n\n"
                      f"What's your guess? 🤔"
        }
    
    def guess_number(self, user_id: int, guess: int) -> Dict[str, Any]:
        """Process number guess"""
        if user_id not in self.active_games:
            return {"success": False, "message": "No active game!"}
        
        game = self.active_games[user_id]
        if game["type"] != "number_guess":
            return {"success": False, "message": "Wrong game type!"}
        
        game["guesses"] += 1
        number = game["number"]
        
        if guess == number:
            # Won!
            self._update_stats(user_id, "number_guess", won=True)
            del self.active_games[user_id]
            return {
                "success": True,
                "won": True,
                "message": f"🎉 *YOU GOT IT!*\n\n"
                          f"The number was {number}!\n"
                          f"You guessed it in {game['guesses']} tries! 💕✨"
            }
        elif game["guesses"] >= game["max_guesses"]:
            # Lost
            self._update_stats(user_id, "number_guess", won=False)
            del self.active_games[user_id]
            return {
                "success": True,
                "won": False,
                "message": f"😢 *Out of guesses!*\n\n"
                          f"The number was {number}.\n"
                          f"Wanna play again? 💕"
            }
        else:
            # Give hint
            if guess < number:
                hint = "📈 Higher!"
            else:
                hint = "📉 Lower!"
            
            remaining = game["max_guesses"] - game["guesses"]
            return {
                "success": True,
                "message": f"{hint}\n\n"
                          f"Guesses left: {remaining}\n"
                          f"Try again! 💪"
            }
    
    # ==================== WOULD YOU RATHER ====================
    
    WOULD_YOU_RATHER = [
        ("travel to the past", "travel to the future"),
        ("be able to fly", "be invisible"),
        ("live in the mountains", "live by the beach"),
        ("have unlimited money", "have unlimited time"),
        ("read minds", "see the future"),
        ("never use internet again", "never watch TV again"),
        ("be famous", "be rich but unknown"),
        ("have a rewind button", "have a pause button for life"),
    ]
    
    def get_would_you_rather(self) -> Dict[str, Any]:
        """Get a would you rather question"""
        option1, option2 = random.choice(self.WOULD_YOU_RATHER)
        
        return {
            "success": True,
            "message": f"🤔 *Would You Rather...*\n\n"
                      f"A) {option1.title()}\n"
                      f"B) {option2.title()}\n\n"
                      f"What would you choose? Tell me why! 💕",
            "options": [option1, option2]
        }
    
    # ==================== RIDDLES ====================
    
    RIDDLES = [
        {"q": "I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I?", "a": ["echo"], "hint": "Sound bouncing back"},
        {"q": "The more you take, the more you leave behind. What am I?", "a": ["footsteps", "steps"], "hint": "Walking"},
        {"q": "What has keys but no locks, space but no room, and you can enter but can't go inside?", "a": ["keyboard"], "hint": "Computer part"},
        {"q": "I'm tall when I'm young, and short when I'm old. What am I?", "a": ["candle"], "hint": "Burns"},
        {"q": "What gets wet while drying?", "a": ["towel"], "hint": "Bathroom item"},
    ]
    
    def get_riddle(self, user_id: int) -> Dict[str, Any]:
        """Get a riddle"""
        riddle = random.choice(self.RIDDLES)
        
        game_state = {
            "type": "riddle",
            "riddle": riddle,
            "started_at": datetime.now().isoformat()
        }
        
        self.active_games[user_id] = game_state
        
        return {
            "success": True,
            "message": f"🧩 *Riddle Time!*\n\n"
                      f"{riddle['q']}\n\n"
                      f"Think you know? Type your answer!\n"
                      f"(or 'hint' for a clue) 💡"
        }
    
    def answer_riddle(self, user_id: int, answer: str) -> Dict[str, Any]:
        """Check riddle answer"""
        if user_id not in self.active_games:
            return {"success": False, "message": "No active riddle!"}
        
        game = self.active_games[user_id]
        if game["type"] != "riddle":
            return {"success": False, "message": "Wrong game type!"}
        
        answer = answer.lower().strip()
        
        if answer == "hint":
            return {
                "success": True,
                "message": f"💡 *Hint:* {game['riddle']['hint']}\n\nTry again! 😊"
            }
        
        correct_answers = game['riddle']['a']
        
        if any(ans in answer for ans in correct_answers):
            # Correct!
            self._update_stats(user_id, "riddle", won=True)
            del self.active_games[user_id]
            return {
                "success": True,
                "correct": True,
                "message": f"🎉 *Correct!*\n\n"
                          f"You got it! You're so smart! 💕✨\n\n"
                          f"Want another riddle? 🧩"
            }
        else:
            return {
                "success": True,
                "correct": False,
                "message": f"Not quite! Keep thinking... 🤔\n\n"
                          f"Need a hint? Type 'hint' 💡"
            }
    
    # ==================== STATS & UTILITIES ====================
    
    def _update_stats(self, user_id: int, game_type: str, won: bool):
        """Update game statistics"""
        if user_id not in self.game_stats:
            self.game_stats[user_id] = {}
        
        if game_type not in self.game_stats[user_id]:
            self.game_stats[user_id][game_type] = {"played": 0, "won": 0}
        
        self.game_stats[user_id][game_type]["played"] += 1
        if won:
            self.game_stats[user_id][game_type]["won"] += 1
    
    def get_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user's game statistics"""
        if user_id not in self.game_stats:
            return {
                "success": True,
                "message": "You haven't played any games yet! Let's start! 🎮"
            }
        
        stats = self.game_stats[user_id]
        msg = "🎮 *Your Game Stats:*\n\n"
        
        for game_type, data in stats.items():
            played = data["played"]
            won = data["won"]
            win_rate = (won / played * 100) if played > 0 else 0
            msg += f"*{game_type.replace('_', ' ').title()}:*\n"
            msg += f"  Played: {played} | Won: {won} | Win Rate: {win_rate:.1f}%\n\n"
        
        return {
            "success": True,
            "message": msg + "Keep playing! You're doing great! 💕"
        }
    
    def quit_game(self, user_id: int) -> Dict[str, Any]:
        """Quit current game"""
        if user_id in self.active_games:
            del self.active_games[user_id]
            return {
                "success": True,
                "message": "Game ended! Wanna play something else? 🎮"
            }
        return {
            "success": False,
            "message": "No active game to quit!"
        }


# Global instance
_games_engine = None


def get_games_engine():
    """Get global games engine instance"""
    global _games_engine
    if _games_engine is None:
        _games_engine = GamesEngine()
    return _games_engine
