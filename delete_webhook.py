"""
Delete webhook to allow polling
"""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    print("❌ No TELEGRAM_BOT_TOKEN found")
    exit(1)

# Delete webhook
url = f"https://api.telegram.org/bot{token}/deleteWebhook"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data.get("ok"):
        print("✅ Webhook deleted successfully!")
        print("   You can now use polling mode")
    else:
        print(f"❌ Failed to delete webhook: {data}")
else:
    print(f"❌ Error: {response.status_code}")
