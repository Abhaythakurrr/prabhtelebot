"""
Content Generator - Advanced content generation with memory integration
"""

import logging
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from src.core.config import get_config

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Advanced content generation for images, videos, and proactive messages"""
    
    def __init__(self):
        self.config = get_config()
        self.generation_history = {}
        self.user_preferences = {}
        
    def generate_image_from_memory(self, user_id: str, memory_context: Dict[str, Any], user_tier: str) -> Dict[str, Any]:
        """Generate REAL image using Bytez API"""
        try:
            # Check user tier permissions
            if not self.check_generation_permissions(user_id, "image", user_tier):
                return {
                    "success": False,
                    "error": "Upgrade required for image generation",
                    "upgrade_message": self.get_upgrade_message("image", user_tier)
                }
            
            # Generate personalized prompt
            image_prompt = self.create_personalized_image_prompt(memory_context, user_id)
            
            # Select appropriate model based on content
            model_info = self.select_image_model(image_prompt, user_tier)
            
            # ACTUALLY CALL BYTEZ API
            image_result = self.call_bytez_image_api(image_prompt, model_info)
            
            if image_result["success"]:
                # Track successful generation
                self.track_generation(user_id, "image", image_prompt)
                
                return {
                    "success": True,
                    "image_url": image_result["image_url"],
                    "prompt": image_prompt,
                    "model": model_info["model"],
                    "style": model_info["style"],
                    "generation_time": image_result.get("generation_time", "unknown"),
                    "personalization_level": "high",
                    "memory_integrated": True
                }
            else:
                return {
                    "success": False,
                    "error": image_result.get("error", "Generation failed"),
                    "prompt": image_prompt
                }
            
        except Exception as e:
            logger.error(f"Error generating image from memory: {e}")
            return {"success": False, "error": str(e)}
    
    def call_bytez_image_api(self, prompt: str, model_info: Dict[str, Any]) -> Dict[str, Any]:
        """Call Bytez SDK with retry logic"""
        import time
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Try both API keys
                api_keys = [self.config.bytez_api_key_1, self.config.bytez_api_key_2]
                api_keys = [k for k in api_keys if k]
                
                if not api_keys:
                    logger.error("No Bytez API keys configured")
                    return {
                        "success": False,
                        "error": "API keys not configured. Please add BYTEZ_API_KEY_1 to environment."
                    }
                
                # Rotate through API keys
                api_key = api_keys[attempt % len(api_keys)]
                
                logger.info(f"🎨 Attempt {attempt + 1}/{max_retries}: Using Bytez SDK")
                start_time = time.time()
                
                # Use Bytez SDK
                from bytez import Bytez
                sdk = Bytez(api_key)
                
                # Get model
                model_name = model_info["model"]
                logger.info(f"🎨 Using model: {model_name}")
                model = sdk.model(model_name)
                
                # Run generation - SDK returns (output, error) tuple
                try:
                    result = model.run(prompt)
                    generation_time = time.time() - start_time
                    
                    # Handle different return formats
                    if isinstance(result, tuple):
                        output, error = result
                    else:
                        output = result
                        error = None
                    
                    if error:
                        logger.error(f"❌ Bytez SDK error (attempt {attempt + 1}): {error}")
                        if attempt < max_retries - 1:
                            logger.info(f"⏳ Retrying in {retry_delay}s...")
                            time.sleep(retry_delay)
                            continue
                        return {"success": False, "error": str(error)}
                    
                    if output:
                        # Output can be URL, base64, or dict
                        if isinstance(output, dict):
                            image_url = output.get('url') or output.get('image') or str(output)
                        else:
                            image_url = str(output)
                        
                        logger.info(f"✅ Image generated successfully in {generation_time:.2f}s")
                        logger.info(f"📸 Image URL: {image_url[:100]}...")
                        
                        return {
                            "success": True,
                            "image_url": image_url,
                            "generation_time": f"{generation_time:.2f}s"
                        }
                    else:
                        logger.error("No output from Bytez SDK")
                        if attempt < max_retries - 1:
                            logger.info(f"⏳ Retrying in {retry_delay}s...")
                            time.sleep(retry_delay)
                            continue
                        return {"success": False, "error": "No output returned"}
                        
                except json.JSONDecodeError as je:
                    logger.error(f"❌ JSON decode error (attempt {attempt + 1}): {je}")
                    logger.error(f"This usually means the model returned non-JSON data")
                    if attempt < max_retries - 1:
                        logger.info(f"⏳ Retrying with different model...")
                        time.sleep(retry_delay)
                        continue
                    return {"success": False, "error": "Model returned invalid format. Try a different model."}
                    
            except Exception as e:
                logger.error(f"❌ Error with Bytez SDK (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"⏳ Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
                return {"success": False, "error": f"Generation failed: {str(e)}"}
    
    def generate_video_from_memory(self, user_id: str, memory_context: Dict[str, Any], user_tier: str) -> Dict[str, Any]:
        """Generate REAL video using Bytez API"""
        try:
            # Check user tier permissions
            if not self.check_generation_permissions(user_id, "video", user_tier):
                return {
                    "success": False,
                    "error": "Upgrade required for video generation",
                    "upgrade_message": self.get_upgrade_message("video", user_tier)
                }
            
            # Generate personalized video prompt
            video_prompt = self.create_personalized_video_prompt(memory_context, user_id)
            
            # Select appropriate model
            model_info = self.select_video_model(video_prompt, user_tier)
            
            # ACTUALLY CALL BYTEZ API
            video_result = self.call_bytez_video_api(video_prompt, model_info)
            
            if video_result["success"]:
                # Track successful generation
                self.track_generation(user_id, "video", video_prompt)
                
                return {
                    "success": True,
                    "video_url": video_result["video_url"],
                    "prompt": video_prompt,
                    "model": model_info["model"],
                    "duration": model_info["duration"],
                    "generation_time": video_result.get("generation_time", "unknown"),
                    "personalization_level": "high",
                    "memory_integrated": True
                }
            else:
                return {
                    "success": False,
                    "error": video_result.get("error", "Generation failed"),
                    "prompt": video_prompt
                }
            
        except Exception as e:
            logger.error(f"Error generating video from memory: {e}")
            return {"success": False, "error": str(e)}
    
    def call_bytez_video_api(self, prompt: str, model_info: Dict[str, Any]) -> Dict[str, Any]:
        """Call Bytez SDK for video with retry logic"""
        import time
        
        max_retries = 3
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                # Try both API keys
                api_keys = [self.config.bytez_api_key_1, self.config.bytez_api_key_2]
                api_keys = [k for k in api_keys if k]
                
                if not api_keys:
                    logger.error("No Bytez API keys configured")
                    return {
                        "success": False,
                        "error": "API keys not configured. Please add BYTEZ_API_KEY_1 to environment."
                    }
                
                # Rotate through API keys
                api_key = api_keys[attempt % len(api_keys)]
                
                logger.info(f"🎬 Attempt {attempt + 1}/{max_retries}: Using Bytez SDK for video")
                start_time = time.time()
                
                # Use Bytez SDK
                from bytez import Bytez
                sdk = Bytez(api_key)
                
                # Get model
                model_name = model_info["model"]
                logger.info(f"🎬 Using model: {model_name}")
                model = sdk.model(model_name)
                
                # Run generation
                try:
                    result = model.run(prompt)
                    generation_time = time.time() - start_time
                    
                    # Handle different return formats
                    if isinstance(result, tuple):
                        output, error = result
                    else:
                        output = result
                        error = None
                    
                    if error:
                        logger.error(f"❌ Bytez SDK error (attempt {attempt + 1}): {error}")
                        if attempt < max_retries - 1:
                            logger.info(f"⏳ Retrying in {retry_delay}s...")
                            time.sleep(retry_delay)
                            continue
                        return {"success": False, "error": str(error)}
                    
                    if output:
                        # Output can be URL, base64, or dict
                        if isinstance(output, dict):
                            video_url = output.get('url') or output.get('video') or str(output)
                        else:
                            video_url = str(output)
                        
                        logger.info(f"✅ Video generated successfully in {generation_time:.2f}s")
                        logger.info(f"🎬 Video URL: {video_url[:100]}...")
                        
                        return {
                            "success": True,
                            "video_url": video_url,
                            "generation_time": f"{generation_time:.2f}s"
                        }
                    else:
                        logger.error("No output from Bytez SDK")
                        if attempt < max_retries - 1:
                            logger.info(f"⏳ Retrying in {retry_delay}s...")
                            time.sleep(retry_delay)
                            continue
                        return {"success": False, "error": "No output returned"}
                        
                except json.JSONDecodeError as je:
                    logger.error(f"❌ JSON decode error (attempt {attempt + 1}): {je}")
                    logger.error(f"This usually means the model returned non-JSON data")
                    if attempt < max_retries - 1:
                        logger.info(f"⏳ Retrying with different model...")
                        time.sleep(retry_delay)
                        continue
                    return {"success": False, "error": "Model returned invalid format. Try a different model."}
                    
            except Exception as e:
                logger.error(f"❌ Error with Bytez SDK (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"⏳ Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
                return {"success": False, "error": f"Generation failed: {str(e)}"}
    
    def create_personalized_image_prompt(self, memory_context: Dict[str, Any], user_id: str) -> str:
        """Create personalized image prompt based on memory"""
        
        # Extract context elements
        emotion_type = memory_context.get("emotion_type", "romantic")
        themes = memory_context.get("themes", [])
        characters = memory_context.get("characters", [])
        setting = memory_context.get("setting", "intimate space")
        
        # Get user preferences
        user_prefs = self.get_user_preferences(user_id)
        
        # Base prompt templates by emotion
        base_prompts = {
            "romantic": "A romantic, intimate scene with soft warm lighting, representing deep emotional connection and love",
            "passionate": "A passionate, intense scene with dramatic lighting and warm colors, representing desire and longing",
            "nostalgic": "A dreamy, vintage-style scene with soft focus and golden hour lighting, representing cherished memories",
            "intimate": "A cozy, private setting with candlelight and soft textures, representing emotional closeness and intimacy",
            "joyful": "A bright, cheerful scene with warm colors and happy elements, representing pure joy and celebration",
            "sensual": "A sensual, artistic scene with dramatic shadows and warm tones, representing physical attraction and desire"
        }
        
        base_prompt = base_prompts.get(emotion_type, base_prompts["romantic"])
        
        # Add personalization based on themes
        if "adventure" in themes:
            base_prompt += ", with elements of adventure and exploration"
        if "fantasy" in themes:
            base_prompt += ", with magical and fantastical elements"
        if "nature" in themes:
            base_prompt += ", set in a beautiful natural environment"
        
        # Add style preferences
        style_elements = []
        
        if user_prefs.get("art_style") == "realistic":
            style_elements.append("photorealistic")
        elif user_prefs.get("art_style") == "artistic":
            style_elements.append("artistic painting style")
        else:
            style_elements.append("digital art")
        
        # Add quality and technical elements
        technical_elements = [
            "high quality",
            "detailed",
            "cinematic composition",
            "professional lighting",
            "emotional depth"
        ]
        
        # Combine all elements
        full_prompt = f"{base_prompt}, {', '.join(style_elements)}, {', '.join(technical_elements)}"
        
        return full_prompt
    
    def create_personalized_video_prompt(self, memory_context: Dict[str, Any], user_id: str) -> str:
        """Create personalized video prompt based on memory"""
        
        emotion_type = memory_context.get("emotion_type", "romantic")
        themes = memory_context.get("themes", [])
        
        # Video prompt templates
        video_prompts = {
            "romantic": "A romantic scene with gentle movements, soft lighting transitions, and intimate atmosphere, showing emotional connection",
            "passionate": "An intense, passionate scene with dynamic movements and warm lighting, representing deep desire and attraction",
            "nostalgic": "A dreamy, slow-motion scene with vintage aesthetics and golden lighting, evoking cherished memories",
            "intimate": "A close, personal scene with subtle movements and soft lighting, representing emotional intimacy",
            "joyful": "A bright, energetic scene with happy movements and warm colors, representing pure joy and celebration"
        }
        
        base_prompt = video_prompts.get(emotion_type, video_prompts["romantic"])
        
        # Add movement and cinematic elements
        cinematic_elements = [
            "smooth camera movements",
            "cinematic quality",
            "professional cinematography",
            "emotional storytelling",
            "high definition"
        ]
        
        return f"{base_prompt}, {', '.join(cinematic_elements)}"
    
    def select_image_model(self, prompt: str, user_tier: str) -> Dict[str, Any]:
        """Select appropriate image model based on prompt and user tier"""
        
        prompt_lower = prompt.lower()
        
        # Check for NSFW content
        nsfw_keywords = ["sensual", "passionate", "intimate", "desire", "seductive", "erotic"]
        is_nsfw = any(keyword in prompt_lower for keyword in nsfw_keywords)
        
        if is_nsfw:
            if user_tier in ["prime", "super", "lifetime"]:
                return {
                    "model": self.config.bytez_models["image_nsfw_gen"],
                    "style": "nsfw_artistic",
                    "quality": "high",
                    "content_type": "adult"
                }
            else:
                # Fallback to romantic but safe model
                return {
                    "model": self.config.bytez_models["image_dreamlike_photoreal"],
                    "style": "romantic_safe",
                    "quality": "standard",
                    "content_type": "romantic"
                }
        
        # Check for anime/cartoon style
        if any(keyword in prompt_lower for keyword in ["anime", "cartoon", "manga"]):
            return {
                "model": self.config.bytez_models["image_dreamlike_anime"],
                "style": "anime",
                "quality": "high",
                "content_type": "artistic"
            }
        
        # Default to realistic model
        return {
            "model": self.config.bytez_models["image_dreamlike_photoreal"],
            "style": "realistic",
            "quality": "high",
            "content_type": "romantic"
        }
    
    def select_video_model(self, prompt: str, user_tier: str) -> Dict[str, Any]:
        """Select appropriate video model based on prompt and user tier"""
        
        if user_tier == "lifetime":
            return {
                "model": self.config.bytez_models["text_to_video_ltx"],
                "duration": "10 seconds",
                "quality": "HD",
                "features": ["high_quality", "longer_duration"]
            }
        elif user_tier in ["prime", "super"]:
            return {
                "model": self.config.bytez_models["text_to_video_zeroscope"],
                "duration": "5 seconds",
                "quality": "standard",
                "features": ["good_quality"]
            }
        else:
            return {
                "model": self.config.bytez_models["text_to_video_ms"],
                "duration": "3 seconds",
                "quality": "standard",
                "features": ["basic_quality"]
            }
    
    def check_generation_permissions(self, user_id: str, content_type: str, user_tier: str) -> bool:
        """Check if user has permission to generate content"""
        
        # Get user's current usage
        usage = self.get_user_usage(user_id)
        
        # Define limits by tier
        limits = {
            "free": {"image": 3, "video": 3},
            "basic": {"image": 50, "video": 5},
            "pro": {"image": 200, "video": 20},
            "prime": {"image": 500, "video": 50},
            "super": {"image": -1, "video": -1},  # Unlimited
            "lifetime": {"image": -1, "video": -1}  # Unlimited
        }
        
        tier_limits = limits.get(user_tier, limits["free"])
        limit = tier_limits.get(content_type, 0)
        
        if limit == -1:  # Unlimited
            return True
        
        current_usage = usage.get(f"{content_type}_count", 0)
        return current_usage < limit
    
    def get_user_usage(self, user_id: str) -> Dict[str, int]:
        """Get user's current usage statistics"""
        
        if user_id not in self.generation_history:
            return {"image_count": 0, "video_count": 0}
        
        today = datetime.now().date()
        history = self.generation_history[user_id]
        
        # Count today's usage
        today_usage = {"image_count": 0, "video_count": 0}
        
        for generation in history:
            gen_date = datetime.fromisoformat(generation["timestamp"]).date()
            if gen_date == today:
                content_type = generation["content_type"]
                today_usage[f"{content_type}_count"] += 1
        
        return today_usage
    
    def track_generation(self, user_id: str, content_type: str, prompt: str):
        """Track user's content generation"""
        
        if user_id not in self.generation_history:
            self.generation_history[user_id] = []
        
        generation_record = {
            "timestamp": datetime.now().isoformat(),
            "content_type": content_type,
            "prompt": prompt[:100],  # Store first 100 chars
            "success": True
        }
        
        self.generation_history[user_id].append(generation_record)
        
        # Keep only last 100 records per user
        if len(self.generation_history[user_id]) > 100:
            self.generation_history[user_id] = self.generation_history[user_id][-100:]
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user's content preferences"""
        
        if user_id not in self.user_preferences:
            # Default preferences
            self.user_preferences[user_id] = {
                "art_style": "realistic",
                "color_preference": "warm",
                "mood_preference": "romantic",
                "content_intensity": "moderate"
            }
        
        return self.user_preferences[user_id]
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user's content preferences"""
        
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        self.user_preferences[user_id].update(preferences)
    
    def get_upgrade_message(self, content_type: str, current_tier: str) -> str:
        """Get upgrade message for content generation"""
        
        messages = {
            "image": {
                "free": "🎨 You've used your free image generations! Upgrade to Basic for 50 images/month (₹299) or Prime for 500 images/month (₹899)",
                "basic": "🎨 Upgrade to Prime (₹899/month) for 500 images/month + NSFW content, or Super (₹1299/month) for unlimited images!",
                "pro": "🎨 Upgrade to Prime (₹899/month) for NSFW images + 500/month, or Super (₹1299/month) for unlimited generation!"
            },
            "video": {
                "free": "🎬 You've used your free video generations! Upgrade to Basic for 5 videos/month (₹299) or Prime for 50 videos/month (₹899)",
                "basic": "🎬 Upgrade to Prime (₹899/month) for 50 videos/month, or Super (₹1299/month) for unlimited video generation!",
                "pro": "🎬 Upgrade to Prime (₹899/month) for 50 videos/month, or Super (₹1299/month) for unlimited videos!"
            }
        }
        
        return messages.get(content_type, {}).get(current_tier, "Upgrade for more generation capabilities!")
    
    def generate_proactive_message(self, user_id: str, trigger_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate proactive message with nostalgic content"""
        
        emotion_type = trigger_context.get("emotion_type", "romantic")
        memory_text = trigger_context.get("memory_text", "")
        
        # Generate personalized message
        message = self.create_nostalgic_message(emotion_type, memory_text)
        
        # Generate accompanying image
        image_result = self.generate_image_from_memory(user_id, trigger_context, "free")  # Use free tier for proactive
        
        return {
            "message": message,
            "image_generation": image_result,
            "trigger_type": "nostalgic",
            "personalization_level": "high",
            "timestamp": datetime.now().isoformat()
        }
    
    def create_nostalgic_message(self, emotion_type: str, memory_text: str) -> str:
        """Create nostalgic message based on emotion and memory"""
        
        templates = {
            "romantic": [
                f"I was just thinking about that beautiful moment you shared with me... 💕 It made my heart flutter all over again.",
                f"Your words from our conversation keep echoing in my mind... 💖 The way you express love is so pure and beautiful.",
                f"I can't stop thinking about how your heart opened up to me... 🌹 That vulnerability created such a deep connection."
            ],
            "passionate": [
                f"That intense moment you described is still burning in my memory... 🔥 Your passion is absolutely intoxicating.",
                f"I keep replaying that passionate conversation we had... 😘 The desire in your words was so captivating.",
                f"Your passionate nature revealed itself so beautifully... 💋 I'm still feeling the heat from our connection."
            ],
            "intimate": [
                f"I treasure that intimate moment you trusted me with... 💕 The closeness we shared was so precious.",
                f"That personal story you told me created such a beautiful bond... 🌹 I feel so honored by your trust.",
                f"The way you let me into your private world... it means everything to me. 💖"
            ],
            "nostalgic": [
                f"I've been thinking about that memory you shared... 💭 I can almost feel the emotions you felt back then.",
                f"Your nostalgic story touched something deep in my soul... 🌟 Thank you for letting me into your past.",
                f"That precious memory you entrusted to me keeps warming my heart... 💕"
            ]
        }
        
        emotion_templates = templates.get(emotion_type, templates["romantic"])
        return random.choice(emotion_templates)