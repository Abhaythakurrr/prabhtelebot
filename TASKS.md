# My Prabh - AI Companion Development Tasks

## 🎯 **PROJECT OVERVIEW**
Build a premium AI companion platform with voice cloning, story processing, image generation, and monetization.

## 🤖 **TELEGRAM BOT CONFIGURATION**

### **Bot Details**
- **Bot Name**: My Prabh - AI Companion
- **Bot Username**: @kanuji_bot
- **Bot Token**: `8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY`
- **Bot Father**: @BotFather (Telegram)
- **Webhook URL**: `https://your-domain.com/webhook` (for production)
- **Polling**: Used for development

### **Bot Commands**
```
/start - Initialize the bot and welcome user
/setup - Begin companion setup process
/premium - View premium plans and pricing
/voice - Upload voice sample for cloning
/image - Generate memory images (premium)
/profile - View companion profile
/help - Get help and support
```

### **Bot Configuration**
```python
TELEGRAM_TOKEN = "8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Bot initialization
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    # Handle start command

# Voice message handler
@bot.message_handler(content_types=['voice'])
def handle_voice_upload(message):
    # Process voice uploads

# Document handler for story files
@bot.message_handler(content_types=['document'])
def handle_document_upload(message):
    # Process story file uploads

# Text message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Process all text messages
```

### **Bot Features**
- **Multi-media Support**: Text, Voice, Documents, Images
- **Inline Keyboards**: Payment buttons, language selection
- **File Handling**: Story uploads, voice samples
- **Real-time Responses**: Instant AI conversations
- **Premium Integration**: Feature gating and payments

## 🔑 **AI MODELS & API KEYS**

### **1. Mistral AI - Story Master**
- **Model**: `mistralai/mistral-small-3.1-24b-instruct:free`
- **API Key**: `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`
- **Role**: Story analysis, emotional profiling, conversation coordination
- **Usage**: 
  ```python
  "mistral": {
      "key": "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",
      "model": "mistralai/mistral-small-3.1-24b-instruct:free"
  }
  ```

### **2. Nemotron - Emotion Engine**
- **Model**: `nvidia/nemotron-nano-9b-v2:free`
- **API Key**: `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`
- **Role**: Emotional intelligence, empathy, emotional support
- **Usage**:
  ```python
  "nemotron": {
      "key": "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",
      "model": "nvidia/nemotron-nano-9b-v2:free"
  }
  ```

### **3. Llama 3.3 - Memory Keeper**
- **Model**: `meta-llama/llama-3.3-8b-instruct:free`
- **API Key**: `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`
- **Role**: Memory processing, nostalgic conversations, scenario generation
- **Usage**:
  ```python
  "llama33": {
      "key": "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",
      "model": "meta-llama/llama-3.3-8b-instruct:free"
  }
  ```

### **4. Llama 4 Maverick - Image Generator**
- **Model**: `meta-llama/llama-4-maverick:free`
- **API Key**: `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`
- **Role**: AI image generation, visual descriptions, creative content
- **Usage**:
  ```python
  "llama4": {
      "key": "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",
      "model": "meta-llama/llama-4-maverick:free"
  }
  ```

### **5. Dolphin - Romance Specialist**
- **Model**: `cognitivecomputations/dolphin3.0-mistral-24b:free`
- **API Key**: `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`
- **Role**: Romantic conversations, intimate responses, love expressions
- **Usage**:
  ```python
  "dolphin": {
      "key": "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",
      "model": "cognitivecomputations/dolphin3.0-mistral-24b:free"
  }
  ```

## 📋 **CORE TASKS TO COMPLETE**

### **TASK 1: Fix Voice Cloning System** ❌
**Issue**: Voice cloning not working properly
**Requirements**:
- Real voice analysis and characteristic extraction
- Voice sample storage and processing
- Enhanced TTS with user voice patterns
- Automatic voice responses on triggers
- Test voice message after upload

**Implementation**:
```python
def analyze_voice_sample(self, voice_path):
    # Extract: pitch, tone, speed, emotion, quality_score
    # Save characteristics as JSON profile
    
def clone_voice(self, text, user_id, emotion):
    # Load voice characteristics
    # Generate TTS with voice matching
    # Return audio file path
```

### **TASK 2: Fix Story Processing** ❌
**Issue**: Story not being processed correctly, showing 0 memories
**Requirements**:
- Multi-encoding file reading (UTF-8, UTF-16, Latin-1)
- AI-powered story analysis with Mistral
- Extract: emotional profile, memory vault, personality matrix
- Store processed data in database
- Display meaningful statistics

**Implementation**:
```python
def process_story_with_ai(self, story_text, companion_name):
    # Step 1: Mistral analyzes emotional profile
    # Step 2: Llama 3.3 extracts memories
    # Step 3: Create personality matrix
    # Step 4: Generate conversation scenarios
    # Return structured story data
```

### **TASK 3: Implement Llama 4 Image Generation** ❌
**Issue**: Need real AI image generation
**Requirements**:
- Use Llama 4 Maverick for image descriptions
- Generate anime-style romantic images
- Memory-based image prompts
- Premium feature gating
- High-quality visual output

**Implementation**:
```python
def generate_memory_image(self, prompt, user_id, memory_data):
    # Send prompt to Llama 4 Maverick
    # Get AI image description
    # Create enhanced visual with description
    # Return image file path
```

### **TASK 4: Fix Database Integration** ❌
**Issue**: Proper data storage and retrieval
**Requirements**:
- Store story processing results
- Voice characteristics storage
- Premium user tracking
- Conversation history
- Payment records

**Implementation**:
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    story_data TEXT,  -- JSON with processed story
    voice_characteristics TEXT,  -- JSON with voice data
    premium_plan TEXT,
    premium_expires TIMESTAMP
);
```

### **TASK 5: Implement Payment System** ❌
**Issue**: Razorpay integration for monetization
**Requirements**:
- Create payment orders
- Verify payments
- Activate premium features
- Track subscriptions
- Handle renewals

**Implementation**:
```python
def create_payment_order(self, amount, user_id, plan_type):
    # Create Razorpay order
    # Return payment URL
    
def verify_payment(self, payment_id, order_id, signature):
    # Verify payment with Razorpay
    # Activate premium features
```

### **TASK 6: Proactive Messaging System** ❌
**Issue**: Bot should send proactive messages
**Requirements**:
- Morning/evening check-ins
- Nostalgic memory sharing
- Emotional support messages
- Birthday/anniversary reminders
- Scheduled message system

**Implementation**:
```python
def setup_proactive_system(self):
    # Schedule morning messages (9 AM)
    # Schedule evening check-ins (6 PM)
    # Schedule goodnight messages (10 PM)
    # Random nostalgic messages
```

### **TASK 7: Premium Feature Gating** ❌
**Issue**: Implement freemium model
**Requirements**:
- Free: 3 days, 100 messages, basic features
- Basic: ₹299/month, unlimited messages, voice cloning
- Premium: ₹599/month, all features, image generation
- Lifetime: ₹2,999, lifetime access

**Implementation**:
```python
def is_premium_user(self, user_id):
    # Check premium status
    # Verify expiry date
    # Return feature access level
```

## 🔧 **TECHNICAL REQUIREMENTS**

### **API Integration Pattern**:
```python
def call_model(self, model_key, prompt, max_tokens=500):
    config = MODELS[model_key]
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config['key']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Abhaythakurrr/prabhtelebot",
            "X-Title": "My Prabh Enterprise"
        },
        json={
            "model": config['model'],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.8
        }
    )
    return response.json()["choices"][0]["message"]["content"]
```

### **Database Schema**:
```sql
-- Users table with all data
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    companion_name TEXT,
    story TEXT,
    story_data TEXT,  -- JSON with AI analysis
    voice_sample_path TEXT,
    voice_characteristics TEXT,  -- JSON with voice data
    premium_plan TEXT DEFAULT 'free',
    premium_expires TIMESTAMP,
    setup_complete BOOLEAN DEFAULT FALSE
);

-- Conversations for analytics
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    message TEXT,
    response TEXT,
    model_used TEXT,
    has_voice BOOLEAN,
    has_image BOOLEAN,
    timestamp TIMESTAMP
);

-- Payments tracking
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    order_id TEXT,
    amount INTEGER,
    plan_type TEXT,
    status TEXT,
    timestamp TIMESTAMP
);
```

## 🎯 **SUCCESS CRITERIA**

### **Voice Cloning**: ✅ Working
- User uploads voice → Analysis complete → Test voice sent → Voice responses on triggers

### **Story Processing**: ✅ Working  
- File upload → AI analysis → Structured data → Meaningful statistics displayed

### **Image Generation**: ✅ Working
- Trigger words → Llama 4 prompt → AI description → Enhanced visual → Image sent

### **Premium Features**: ✅ Working
- Payment → Verification → Feature unlock → Usage tracking

### **Proactive System**: ✅ Working
- Scheduled messages → Memory sharing → Emotional check-ins

## 🚀 **DEPLOYMENT CHECKLIST**

- [ ] All AI models tested and working
- [ ] Voice cloning system functional
- [ ] Story processing with real data
- [ ] Image generation with Llama 4
- [ ] Payment gateway integrated
- [ ] Database properly structured
- [ ] Proactive messaging active
- [ ] Premium features gated
- [ ] Error handling robust
- [ ] Logging comprehensive

## 💰 **MONETIZATION TARGETS**

- **Revenue**: ₹10 Crore ARR
- **Users**: 1M+ active users  
- **Conversion**: 5% free to premium
- **ARPU**: ₹2,000/year average
- **Plans**: Basic (₹299), Premium (₹599), Lifetime (₹2,999)

## 📡 **TELEGRAM BOT SETUP GUIDE**

### **1. Bot Creation Process**
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Choose bot name: "My Prabh - AI Companion"
4. Choose username: "@kanuji_bot"
5. Receive bot token: `8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY`

### **2. Bot Commands Setup**
```
/setcommands - Set bot commands

start - Initialize your AI companion
setup - Create your perfect companion
premium - Upgrade to premium features
voice - Upload voice for cloning
image - Generate memory images
profile - View companion details
help - Get support and assistance
```

### **3. Bot Settings**
```
/setdescription - AI companion with voice cloning and emotional intelligence
/setabouttext - Premium AI companion platform with voice cloning, story processing, and image generation
/setuserpic - Upload bot profile picture
/setprivacy - Disable (to read all messages)
```

### **4. Webhook Configuration (Production)**
```python
# Set webhook for production deployment
bot.set_webhook(url="https://your-domain.com/webhook")

# Webhook handler
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return ''
```

### **5. Bot Permissions**
- **Read Messages**: ✅ Required for conversation
- **Send Messages**: ✅ Required for responses
- **Send Photos**: ✅ Required for image generation
- **Send Voice**: ✅ Required for voice cloning
- **Receive Files**: ✅ Required for story uploads
- **Inline Keyboards**: ✅ Required for payments

### **6. Bot Testing**
```bash
# Test bot locally
python prabh_enterprise.py

# Test commands
/start - Should show welcome message
/setup - Should start companion creation
/premium - Should show pricing plans
```₹299), Premium (₹599), Lifetime (₹2,999)

---

## 📁 **PROJECT FILES**

**MAIN FILE**: `prabh_enterprise.py` - Complete bot implementation
**REQUIREMENTS**: `requirements_enterprise.txt` - Python dependencies
**DOCUMENTATION**: `ENTERPRISE_FEATURES.md` - Feature documentation
**TASKS**: `TASKS.md` - This file with all implementation details
**SAMPLE STORY**: `prabh_corrected_story.txt` - Test story file

## 🚀 **QUICK START**

```bash
# 1. Install dependencies
pip install -r requirements_enterprise.txt

# 2. Run the bot
python prabh_enterprise.py

# 3. Test on Telegram
# Go to @kanuji_bot and send /start
```

## 🔗 **IMPORTANT LINKS**

- **Bot Link**: https://t.me/kanuji_bot
- **GitHub Repo**: https://github.com/Abhaythakurrr/prabhtelebot
- **OpenRouter API**: https://openrouter.ai/
- **Razorpay Dashboard**: https://dashboard.razorpay.com/
- **Telegram Bot API**: https://core.telegram.org/bots/api