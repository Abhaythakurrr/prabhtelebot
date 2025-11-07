"""
Fast Response Orchestrator - Guarantees sub-3-second responses
Handles parallel AI + visual generation with fallback strategies
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from telegram import Bot

logger = logging.getLogger(__name__)


class FastResponseOrchestrator:
    """
    Orchestrates fast responses with visual content
    - Guarantees <3 second response time
    - Parallel AI + visual generation
    - Typing indicators for engagement
    - Fallback strategies for slow operations
    """
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.response_timeout = 3.0  # 3 second guarantee
        self.typing_interval = 5.0  # Refresh typing every 5 seconds
        
    async def handle_message(
        self, 
        user_id: int, 
        message: str,
        ai_generator,
        visual_engine=None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates fast response with optional visual content
        
        Args:
            user_id: Telegram user ID
            message: User's message
            ai_generator: AI generator instance
            visual_engine: Optional visual generation engine
            context: Additional context for generation
            
        Returns:
            Dict with 'text', 'visual_url', 'response_time'
        """
        start_time = datetime.now()
        
        # Start typing indicator immediately
        typing_task = asyncio.create_task(
            self._maintain_typing_indicator(user_id)
        )
        
        try:
            # Generate response with timeout
            result = await asyncio.wait_for(
                self._generate_with_visual(
                    user_id, message, ai_generator, visual_engine, context
                ),
                timeout=self.response_timeout
            )
            
            response_time = (datetime.now() - start_time).total_seconds()
            result['response_time'] = response_time
            
            logger.info(f"✅ Fast response delivered in {response_time:.2f}s")
            return result
            
        except asyncio.TimeoutError:
            # Timeout - send intermediate message
            logger.warning(f"⚠️ Response timeout, sending intermediate message")
            
            await self.bot.send_message(
                chat_id=user_id,
                text="Hold on, let me think about this... 💭"
            )
            
            # Continue processing in background
            result = await self._generate_with_visual(
                user_id, message, ai_generator, visual_engine, context
            )
            
            response_time = (datetime.now() - start_time).total_seconds()
            result['response_time'] = response_time
            result['intermediate_sent'] = True
            
            return result
            
        finally:
            # Stop typing indicator
            typing_task.cancel()
            try:
                await typing_task
            except asyncio.CancelledError:
                pass
    
    async def _maintain_typing_indicator(self, user_id: int):
        """Maintains typing indicator to keep user engaged"""
        try:
            while True:
                await self.bot.send_chat_action(
                    chat_id=user_id,
                    action="typing"
                )
                await asyncio.sleep(self.typing_interval)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.debug(f"Typing indicator error: {e}")
    
    async def _generate_with_visual(
        self,
        user_id: int,
        message: str,
        ai_generator,
        visual_engine,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generates text response + matching visual simultaneously
        Uses parallel processing for speed
        """
        # Prepare tasks
        tasks = []
        
        # AI text generation (required)
        text_task = asyncio.create_task(
            self._generate_text(message, ai_generator, context)
        )
        tasks.append(('text', text_task))
        
        # Visual generation (optional, parallel)
        if visual_engine and context and context.get('generate_visual'):
            visual_task = asyncio.create_task(
                self._generate_visual(message, visual_engine, context)
            )
            tasks.append(('visual', visual_task))
        
        # Wait for all tasks
        results = {}
        for task_name, task in tasks:
            try:
                results[task_name] = await task
            except Exception as e:
                logger.error(f"Error in {task_name} generation: {e}")
                results[task_name] = None
        
        return {
            'text': results.get('text', "I'm here! Let's talk 💕"),
            'visual_url': results.get('visual'),
            'intermediate_sent': False
        }
    
    async def _generate_text(
        self, 
        message: str, 
        ai_generator,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generates AI text response"""
        try:
            # Call AI generator
            if hasattr(ai_generator, 'generate_response'):
                response = await ai_generator.generate_response(message, context)
            else:
                # Fallback for sync generators
                response = ai_generator.generate(message)
            
            return response
            
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            return "I'm here! Let's talk 💕"
    
    async def _generate_visual(
        self,
        message: str,
        visual_engine,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """Generates matching visual (image or GIF)"""
        try:
            if hasattr(visual_engine, 'get_scene_visual'):
                scene_desc = context.get('scene_description', message)
                mood = context.get('mood', 'neutral')
                visual_url = await visual_engine.get_scene_visual(scene_desc, mood)
                return visual_url
            return None
            
        except Exception as e:
            logger.error(f"Visual generation error: {e}")
            return None
    
    async def send_response(
        self,
        user_id: int,
        text: str,
        visual_url: Optional[str] = None,
        parse_mode: str = "Markdown"
    ):
        """
        Sends response to user with optional visual
        """
        try:
            if visual_url:
                # Send photo with caption
                await self.bot.send_photo(
                    chat_id=user_id,
                    photo=visual_url,
                    caption=text,
                    parse_mode=parse_mode
                )
            else:
                # Send text only
                await self.bot.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode=parse_mode
                )
                
        except Exception as e:
            logger.error(f"Error sending response: {e}")
            # Fallback to plain text
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=text
                )
            except Exception as e2:
                logger.error(f"Fallback send also failed: {e2}")


# Global instance
_fast_response_orchestrator = None


def get_fast_response_orchestrator(bot: Bot = None):
    """Get global fast response orchestrator instance"""
    global _fast_response_orchestrator
    if _fast_response_orchestrator is None and bot:
        _fast_response_orchestrator = FastResponseOrchestrator(bot)
    return _fast_response_orchestrator
