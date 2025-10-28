"""
Modern Telegram Bot Keyboards - Professional UI/UX
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard():
    """Modern main menu with emoji icons"""
    keyboard = [
        [
            InlineKeyboardButton("💬 Chat with AI", callback_data="chat_start"),
            InlineKeyboardButton("🎨 Generate Image", callback_data="generate_image")
        ],
        [
            InlineKeyboardButton("🎬 Generate Video", callback_data="generate_video"),
            InlineKeyboardButton("🎵 Generate Music", callback_data="generate_music")
        ],
        [
            InlineKeyboardButton("📚 Upload Story", callback_data="upload_story"),
            InlineKeyboardButton("🎭 Roleplay Scenarios", callback_data="roleplay_menu")
        ],
        [
            InlineKeyboardButton("👤 My Profile", callback_data="profile"),
            InlineKeyboardButton("💎 Upgrade Plan", callback_data="pricing")
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_generation_menu():
    """Content generation options"""
    keyboard = [
        [
            InlineKeyboardButton("🖼️ Single Image", callback_data="gen_single_image"),
            InlineKeyboardButton("🎨 Image Series", callback_data="gen_image_series")
        ],
        [
            InlineKeyboardButton("🎬 Short Video (5s)", callback_data="gen_video_short"),
            InlineKeyboardButton("🎥 Long Video (15s)", callback_data="gen_video_long")
        ],
        [
            InlineKeyboardButton("🎵 Music Track", callback_data="gen_music"),
            InlineKeyboardButton("🗣️ Voice Message", callback_data="gen_voice")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_profile_menu():
    """User profile with stats"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Usage Stats", callback_data="stats"),
            InlineKeyboardButton("🧠 My Memories", callback_data="memories")
        ],
        [
            InlineKeyboardButton("📚 My Stories", callback_data="my_stories"),
            InlineKeyboardButton("🎭 My Roleplays", callback_data="my_roleplays")
        ],
        [
            InlineKeyboardButton("💎 Subscription", callback_data="subscription_info"),
            InlineKeyboardButton("💳 Payment History", callback_data="payment_history")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_pricing_keyboard():
    """Modern pricing with direct payment"""
    keyboard = [
        [
            InlineKeyboardButton("💎 BASIC - ₹299/mo", callback_data="buy_basic"),
            InlineKeyboardButton("🔥 PRO - ₹599/mo", callback_data="buy_pro")
        ],
        [
            InlineKeyboardButton("👑 PRIME - ₹899/mo", callback_data="buy_prime"),
            InlineKeyboardButton("🚀 SUPER - ₹1299/mo", callback_data="buy_super")
        ],
        [
            InlineKeyboardButton("♾️ LIFETIME - ₹2999", callback_data="buy_lifetime")
        ],
        [
            InlineKeyboardButton("📊 Compare Plans", url="https://yourwebsite.com/pricing"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_image_style_keyboard():
    """Image generation style selection"""
    keyboard = [
        [
            InlineKeyboardButton("🌹 Romantic", callback_data="style_romantic"),
            InlineKeyboardButton("🎨 Artistic", callback_data="style_artistic")
        ],
        [
            InlineKeyboardButton("✨ Fantasy", callback_data="style_fantasy"),
            InlineKeyboardButton("📸 Realistic", callback_data="style_realistic")
        ],
        [
            InlineKeyboardButton("🎭 Anime", callback_data="style_anime"),
            InlineKeyboardButton("🖼️ Portrait", callback_data="style_portrait")
        ],
        [
            InlineKeyboardButton("🔞 NSFW (Premium)", callback_data="style_nsfw"),
            InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_story_upload_keyboard():
    """Story upload options"""
    keyboard = [
        [
            InlineKeyboardButton("📁 Upload File", callback_data="upload_file"),
            InlineKeyboardButton("💬 Type Story", callback_data="type_story")
        ],
        [
            InlineKeyboardButton("🎙️ Voice Story", callback_data="voice_story"),
            InlineKeyboardButton("📚 My Stories", callback_data="my_stories")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_roleplay_menu():
    """Roleplay scenario selection"""
    keyboard = [
        [
            InlineKeyboardButton("🎭 Start New Roleplay", callback_data="roleplay_new"),
            InlineKeyboardButton("📖 Continue Story", callback_data="roleplay_continue")
        ],
        [
            InlineKeyboardButton("🌟 Suggested Scenarios", callback_data="roleplay_suggested"),
            InlineKeyboardButton("✍️ Custom Scenario", callback_data="roleplay_custom")
        ],
        [
            InlineKeyboardButton("🔥 Adult Roleplay (Premium)", callback_data="roleplay_nsfw"),
            InlineKeyboardButton("📚 My Roleplays", callback_data="my_roleplays")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings_keyboard():
    """Settings menu"""
    keyboard = [
        [
            InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications"),
            InlineKeyboardButton("🌐 Language", callback_data="settings_language")
        ],
        [
            InlineKeyboardButton("🎨 AI Personality", callback_data="settings_personality"),
            InlineKeyboardButton("🔞 Content Filter", callback_data="settings_filter")
        ],
        [
            InlineKeyboardButton("🗑️ Clear History", callback_data="settings_clear"),
            InlineKeyboardButton("📥 Export Data", callback_data="settings_export")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_help_keyboard():
    """Help and support menu"""
    keyboard = [
        [
            InlineKeyboardButton("📖 User Guide", callback_data="help_guide"),
            InlineKeyboardButton("🎥 Video Tutorials", callback_data="help_videos")
        ],
        [
            InlineKeyboardButton("💬 Contact Support", callback_data="help_support"),
            InlineKeyboardButton("🐛 Report Bug", callback_data="help_bug")
        ],
        [
            InlineKeyboardButton("🌐 Visit Website", url="https://yourwebsite.com"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(action):
    """Generic confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Proceed", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("❌ Cancel", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_payment_keyboard(plan_id, payment_url):
    """Payment checkout keyboard"""
    keyboard = [
        [InlineKeyboardButton("💳 Pay Now", url=payment_url)],
        [
            InlineKeyboardButton("📊 Compare Plans", callback_data="pricing"),
            InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_memory_action_keyboard(memory_id):
    """Actions for a specific memory"""
    keyboard = [
        [
            InlineKeyboardButton("💬 Discuss", callback_data=f"discuss_{memory_id}"),
            InlineKeyboardButton("🎨 Visualize", callback_data=f"visualize_{memory_id}")
        ],
        [
            InlineKeyboardButton("🎭 Roleplay", callback_data=f"roleplay_{memory_id}"),
            InlineKeyboardButton("💾 Save", callback_data=f"save_{memory_id}")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="memories")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
