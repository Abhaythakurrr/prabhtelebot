"""
Check which bot this token belongs to
"""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    print("❌ No TELEGRAM_BOT_TOKEN found")
    exit(1)

# Get bot info
url = f"https://api.telegram.org/bot{token}/getMe"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data.get("ok"):
        bot_info = data.get("result", {})
        print("🤖 BOT INFORMATION:")
        print(f"   ID: {bot_info.get('id')}")
        print(f"   Username: @{bot_info.get('username')}")
        print(f"   First Name: {bot_info.get('first_name')}")
        print(f"   Is Bot: {bot_info.get('is_bot')}")
        print(f"\n✅ This is YOUR bot token")
        print(f"\n⚠️ If you're testing @kanuji_bot, that's a DIFFERENT bot!")
        print(f"   You need to test @{bot_info.get('username')} instead")
    else:
        print("❌ Invalid response from Telegram")
else:
    print(f"❌ Error: {response.status_code}")
