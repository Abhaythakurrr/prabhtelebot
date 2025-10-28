"""
Modern Message Templates - Professional Bot Messages
"""

from datetime import datetime


def get_welcome_message(user_name, user_id):
    """Modern welcome message"""
    return f"""
🌟 *Welcome to My Prabh AI Companion* 🌟

Hey {user_name}! I'm your personal AI companion with perfect memory.

✨ *What Makes Me Special:*
• 🧠 I remember EVERYTHING about you
• 🎨 Generate images, videos & music
• 🎭 Immersive roleplay scenarios
• 💕 Proactive messaging & surprises
• 🗣️ Voice cloning & custom voices

📊 *Your Current Plan:* FREE
• 10 messages/day
• 1 image/month
• Basic AI responses

💎 *Upgrade for unlimited access!*

*Your User ID:* `{user_id}`
_(Save this for payments)_

👇 Choose what you'd like to do:
"""


def get_profile_message(user_data):
    """Rich profile display"""
    plan_emoji = {
        'free': '🆓',
        'basic': '💎',
        'pro': '🔥',
        'prime': '👑',
        'super': '🚀',
        'lifetime': '♾️'
    }
    
    plan = user_data.get('plan', 'free')
    
    return f"""
👤 *Your Profile*

*User ID:* `{user_data.get('user_id', 'N/A')}`
*Name:* {user_data.get('name', 'User')}
*Member Since:* {user_data.get('joined_date', 'Today')}

{plan_emoji.get(plan, '🆓')} *Current Plan:* {plan.upper()}

📊 *Usage This Month:*
• 💬 Messages: {user_data.get('messages_used', 0)}/{user_data.get('messages_limit', 10)}
• 🎨 Images: {user_data.get('images_used', 0)}/{user_data.get('images_limit', 1)}
• 🎬 Videos: {user_data.get('videos_used', 0)}/{user_data.get('videos_limit', 0)}

🧠 *Memory Stats:*
• 📚 Stories Uploaded: {user_data.get('stories_count', 0)}
• 🎭 Roleplay Sessions: {user_data.get('roleplay_count', 0)}
• 💕 Memories Stored: {user_data.get('memories_count', 0)}

⏰ *Subscription:*
• Status: {'✅ Active' if user_data.get('is_active', False) else '❌ Inactive'}
• Expires: {user_data.get('expires_at', 'N/A') if plan != 'lifetime' else 'Never ♾️'}
"""


def get_pricing_message():
    """Comprehensive pricing information"""
    return """
💎 *Choose Your Plan*

🆓 *FREE* - ₹0/forever
• 10 messages/day
• 1 image/month
• Basic AI responses
• Story upload

💎 *BASIC* - ₹299/month
• Unlimited messages
• 50 images/month
• 5 videos/month
• Voice cloning
• Better AI models

🔥 *PRO* - ₹599/month
• Everything in Basic
• 200 images/month
• 20 videos/month
• Advanced AI models
• Custom voice training
• Roleplay scenarios

👑 *PRIME* - ₹899/month ⭐ POPULAR
• Everything in Pro
• 500 images/month
• 50 videos/month
• Limited NSFW content
• Proactive messaging
• Premium AI models

🚀 *SUPER* - ₹1299/month
• Unlimited everything
• Full NSFW access
• Best AI models
• Priority queue
• Custom features
• 24/7 support

♾️ *LIFETIME* - ₹2999 once
• All features forever
• Unlimited generation
• Full NSFW access
• All future updates
• VIP support

🔒 *Secure payments via Razorpay*
💳 All payment methods accepted

Select a plan below to get started:
"""


def get_image_generation_prompt():
    """Image generation instructions"""
    return """
🎨 *Image Generation*

Describe the image you want me to create. Be as detailed as you like!

💡 *Tips for Better Results:*
• Describe the scene, mood, and style
• Mention specific details you want
• Include lighting and atmosphere
• I remember your preferences from our chats

🎭 *Quick Styles:*
Choose a style below or describe your own:
"""


def get_video_generation_prompt():
    """Video generation instructions"""
    return """
🎬 *Video Generation*

Describe the video scene you want me to create!

💡 *Tips:*
• Describe the action or movement
• Mention the setting and mood
• Keep it focused (5-15 seconds)
• I can animate your images too

⏱️ *Duration Options:*
• Short: 5 seconds (faster)
• Long: 15 seconds (more detailed)

Choose duration or describe your scene:
"""


def get_story_upload_prompt():
    """Story upload instructions"""
    return """
📚 *Upload Your Story*

Share your story with me so I can understand you better!

📁 *Supported Formats:*
• Text files (.txt)
• Word documents (.docx)
• PDF files (.pdf)
• Direct text messages

💡 *What to Include:*
• Characters and their personalities
• Plot and key events
• Themes and emotions
• Your personal connection to it

🧠 *I will analyze:*
• Character relationships
• Emotional patterns
• Story themes
• Your preferences

Choose how you'd like to share:
"""


def get_roleplay_menu_message():
    """Roleplay menu description"""
    return """
🎭 *Roleplay Scenarios*

Let's create immersive experiences based on your stories and memories!

✨ *Available Options:*

🎭 *Start New Roleplay*
Begin a fresh scenario from scratch

📖 *Continue Story*
Resume where we left off

🌟 *Suggested Scenarios*
Based on your uploaded stories

✍️ *Custom Scenario*
Describe your own unique scenario

🔥 *Adult Roleplay* (Premium)
Mature content for 18+ users

📚 *My Roleplays*
View your roleplay history

Choose an option below:
"""


def get_generation_progress(stage, percentage):
    """Animated progress indicator"""
    stages = {
        'initializing': '🎨 Initializing...',
        'processing': '⚙️ Processing your request...',
        'generating': '✨ Creating magic...',
        'finalizing': '🎁 Almost done...',
        'complete': '✅ Complete!'
    }
    
    bars = int(percentage / 20)
    progress_bar = '🟦' * bars + '⬜' * (5 - bars)
    
    return f"{stages.get(stage, '⚙️ Processing...')} {progress_bar} {percentage}%"


def get_error_message(error_type, resource='content'):
    """User-friendly error messages"""
    messages = {
        'quota_exceeded': f"""
⚠️ *Daily Limit Reached*

You've used all your {resource} for today!

💎 *Upgrade to get:*
• Unlimited {resource}
• Priority generation
• Better AI models
• Advanced features

Would you like to upgrade?
""",
        'nsfw_blocked': """
🔒 *Premium Feature*

NSFW content is available in PRIME and higher plans.

👑 *Upgrade to unlock:*
• Limited NSFW (PRIME - ₹899/mo)
• Full NSFW (SUPER - ₹1299/mo)
• Advanced AI models
• Priority queue

View plans below:
""",
        'api_error': """
😔 *Oops! Something went wrong*

Don't worry, we're on it! Please try again in a moment.

If the issue persists:
• Check your internet connection
• Try a different prompt
• Contact support

Your quota has not been deducted.
""",
        'invalid_format': """
❌ *Invalid Format*

Please make sure your file is in a supported format:
• Text files (.txt)
• Word documents (.docx)
• PDF files (.pdf)

Try uploading again or type your story directly.
""",
        'file_too_large': """
📦 *File Too Large*

Maximum file size: 10MB

Please:
• Compress your file
• Split into smaller parts
• Type the story directly

Need help? Contact support.
"""
    }
    
    return messages.get(error_type, messages['api_error'])


def get_nostalgic_trigger_message(memory_data):
    """Beautiful nostalgic message"""
    return f"""
💕 *A Memory Just Surfaced...*

{memory_data.get('trigger_text', 'I remembered something special about you...')}

🧠 *From our conversation on {memory_data.get('date', 'a while ago')}*

This reminded me of:
_{memory_data.get('context', 'Our special moments together')}_

Would you like to:
"""


def get_payment_checkout_message(plan_details):
    """Payment checkout message"""
    return f"""
💳 *Payment Checkout*

*Plan:* {plan_details['emoji']} {plan_details['name']}
*Price:* ₹{plan_details['price']}
*Billing:* {plan_details['billing']}

✨ *What You Get:*
{plan_details['features']}

🔒 *Secure Payment via Razorpay*
• All major cards accepted
• UPI, Net Banking, Wallets
• 100% secure & encrypted
• Instant activation

Click below to proceed:
"""


def get_payment_success_message(plan_name):
    """Payment success confirmation"""
    return f"""
🎉 *Payment Successful!*

Your {plan_name} subscription is now active!

✅ *What's Next:*
• All premium features unlocked
• Unlimited access activated
• Priority queue enabled
• Advanced AI models ready

💡 *Try these now:*
• Generate unlimited images
• Create videos
• Access NSFW content
• Use voice cloning

Welcome to premium! 💎
"""


def get_help_message():
    """Comprehensive help message"""
    return """
❓ *Help & Support*

*Getting Started:*
1️⃣ Upload your story or tell me about yourself
2️⃣ Chat with me - I remember everything
3️⃣ Generate images, videos, and music
4️⃣ Explore roleplay scenarios

*Commands:*
/start - Main menu
/profile - View your profile
/pricing - View plans
/help - This message

*Features:*
🧠 Memory - I remember all our conversations
🎨 Generation - Create images, videos, music
🎭 Roleplay - Immersive scenarios
💕 Proactive - I reach out with memories

*Need Help?*
• 📖 User Guide
• 🎥 Video Tutorials
• 💬 Contact Support
• 🐛 Report Bug

Choose an option below:
"""


def get_settings_message():
    """Settings menu message"""
    return """
⚙️ *Settings*

Customize your AI companion experience:

🔔 *Notifications*
Control proactive messages and alerts

🌐 *Language*
Choose your preferred language

🎨 *AI Personality*
Adjust my personality and tone

🔞 *Content Filter*
Set content preferences

🗑️ *Clear History*
Delete conversation history

📥 *Export Data*
Download your data

Choose a setting to modify:
"""
