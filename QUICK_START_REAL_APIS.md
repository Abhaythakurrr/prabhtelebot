# 🚀 Quick Start Guide - Real API Implementation

## ✅ What's Been Fixed

Your AI companion bot now uses **REAL APIs** instead of placeholders:

1. **✅ Real AI Conversations** - OpenRouter API calls (not hardcoded!)
2. **✅ Real Roleplay** - AI-generated scenarios (not templates!)
3. **✅ Real Content Generation** - Bytez API for images/videos
4. **✅ Real Story Analysis** - AI-powered understanding
5. **✅ Real Payments** - Razorpay integration

## 🎯 Test It Right Now

### 1. Test AI Conversations (Works Now!)

```bash
python test_real_implementations.py
```

**Expected Output:**
```
✅ PASS - AI Orchestrator (Real OpenRouter API)
✅ PASS - Story Processor (Real AI analysis)
✅ PASS - Payment Integration (Real Razorpay)
```

### 2. Start the Bot

```bash
python start.py
```

**What Works:**
- ✅ Bot starts and responds
- ✅ AI conversations with real models
- ✅ Story upload and AI analysis
- ✅ Roleplay scenario generation
- ✅ Payment order creation

**What Needs API Keys:**
- ⚠️ Image generation (needs BYTEZ_API_KEY)
- ⚠️ Video generation (needs BYTEZ_API_KEY)

## 📋 Environment Variables Needed

### Already Configured (Check .env)
```bash
# OpenRouter AI - For conversations
NEMOTRON_API_KEY=sk-or-v1-...
LLAMA4_API_KEY=sk-or-v1-...
MINIMAX_API_KEY=sk-or-v1-...
DOLPHIN_VENICE_API_KEY=sk-or-v1-...

# Razorpay - For payments
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
RAZORPAY_WEBHOOK_SECRET=...

# Telegram
TELEGRAM_BOT_TOKEN=...
```

### Need to Add (For full functionality)
```bash
# Bytez - For image/video generation
BYTEZ_API_KEY_1=bytez_...
BYTEZ_API_KEY_2=bytez_...
```

## 🧪 Test Each Component

### Test AI Conversations
```python
from src.orchestrator.sync_ai_orchestrator import SyncAIOrchestrator

orchestrator = SyncAIOrchestrator()
response = orchestrator.generate_contextual_response(
    message="I love you",
    story_context={"story_text": "We met in college..."},
    user_tier="basic"
)
print(response)  # Real AI response!
```

### Test Story Analysis
```python
from src.story.advanced_story_processor import AdvancedStoryProcessor

processor = AdvancedStoryProcessor()
result = processor.process_raw_story(
    "We met in college and fell in love...",
    "user_123"
)
print(result['analysis'])  # Real AI analysis!
```

### Test Payment
```python
from src.payment.razorpay_integration import get_payment_handler

handler = get_payment_handler()
order = handler.create_subscription_order(
    user_id="user_123",
    plan_id="prime",
    amount=899
)
print(order)  # Real Razorpay order!
```

## 🎭 How Roleplay Works Now

**Before:** Hardcoded templates
```python
"*I look into your eyes* I hear you..."  # Same every time
```

**Now:** Real AI generation
```python
# AI generates unique responses based on:
# - User's story context
# - Current conversation
# - User tier (free/basic/prime/etc)
# - Intent (romantic/nsfw/emotional)

"*I take a step closer, my eyes locked on yours, 
the warmth of our bodies mingling as the air between 
us thickens. My voice drops to a whisper.* 
'I've missed this, being so close to you.'"
```

## 💬 How Conversations Work Now

### User Message Flow

1. **User sends:** "I love you so much"

2. **Bot processes:**
   - Analyzes intent: "romantic"
   - Gets story context: "We met in college..."
   - Selects AI model based on tier
   - Builds context-aware prompt

3. **AI generates response:**
   ```
   "My darling, hearing those words from you makes my 
   heart flutter. I remember when we first met in college, 
   and that same feeling of love has only grown stronger. 
   You mean everything to me. 💕"
   ```

4. **Bot sends:** Real AI response (not hardcoded!)

## 🎨 How Content Generation Works

### Image Generation Flow

1. **User requests image**
2. **Bot creates personalized prompt:**
   ```
   "A romantic scene with soft warm lighting, 
   representing deep emotional connection and love, 
   photorealistic, high quality, cinematic composition"
   ```
3. **Calls Bytez API** (when keys are added)
4. **Returns real generated image URL**

### Video Generation Flow

1. **User requests video**
2. **Bot creates cinematic prompt:**
   ```
   "A romantic scene with gentle movements, 
   soft lighting transitions, and intimate atmosphere, 
   smooth camera movements, cinematic quality"
   ```
3. **Calls Bytez API** (when keys are added)
4. **Returns real generated video URL**

## 💳 How Payments Work Now

### Payment Flow

1. **User clicks upgrade on website**
2. **Frontend calls:** `POST /api/create-order`
   ```json
   {
     "user_id": "123",
     "plan_id": "prime"
   }
   ```

3. **Backend creates Razorpay order:**
   ```json
   {
     "success": true,
     "order_id": "order_RYSsjcgZL9megG",
     "amount": 899,
     "key_id": "rzp_test_..."
   }
   ```

4. **User completes payment on Razorpay**

5. **Frontend calls:** `POST /api/verify-payment`
   ```json
   {
     "payment_id": "pay_...",
     "order_id": "order_...",
     "signature": "...",
     "user_id": "123",
     "plan_id": "prime"
   }
   ```

6. **Backend verifies and activates subscription**

7. **User gets premium features!**

## 🔍 Verify Real Implementation

### Check AI Responses
```bash
# Run bot and send message
# Response should be unique each time (not hardcoded)
```

### Check Story Analysis
```bash
# Upload story
# Should see AI-generated themes, not just keywords
```

### Check Roleplay
```bash
# Request roleplay
# Should see dynamic scenarios, not templates
```

### Check Payment
```bash
# Try to upgrade
# Should create real Razorpay order
```

## 📊 What's Different Now

### Before (Placeholders)
```python
def generate_response(message):
    if "love" in message:
        return "I love you too! 💕"  # Hardcoded
    return "Tell me more..."  # Hardcoded
```

### After (Real AI)
```python
def generate_response(message, context, tier):
    # Build AI prompt with context
    prompt = build_prompt(message, context, tier)
    
    # Call REAL OpenRouter API
    response = call_openrouter_api(prompt, tier)
    
    # Return unique AI-generated response
    return response  # Different every time!
```

## 🎯 Next Steps

### 1. Test Current Implementation
```bash
python test_real_implementations.py
```

### 2. Add Bytez API Keys (Optional)
```bash
# Add to .env
BYTEZ_API_KEY_1=bytez_...
BYTEZ_API_KEY_2=bytez_...
```

### 3. Deploy to Production
```bash
# All real APIs are ready
# Just need to set environment variables
```

### 4. Monitor API Usage
- OpenRouter: Check usage dashboard
- Bytez: Monitor generation counts
- Razorpay: Track payments

## ✅ Verification Checklist

- [x] AI conversations use real API calls
- [x] Roleplay is dynamically generated
- [x] Story analysis uses AI models
- [x] Payment integration is complete
- [x] No hardcoded responses remain
- [x] Proper error handling added
- [x] Fallback mechanisms in place
- [x] Tier-based features working

## 🎉 You're Ready!

Your AI companion now has:
- 🤖 **Real AI conversations** (OpenRouter)
- 🎭 **Dynamic roleplay** (AI-generated)
- 📚 **Smart story analysis** (AI-powered)
- 💳 **Working payments** (Razorpay)
- 🎨 **Content generation** (Bytez - needs keys)

**No more placeholders. Everything is REAL!**

---

## 🆘 Troubleshooting

### "No API key configured"
- Check .env file has the required keys
- Verify key format is correct
- Test with: `python test_real_implementations.py`

### "API error: 401"
- API key is invalid or expired
- Get new key from provider
- Update .env file

### "Payment gateway not configured"
- Add Razorpay credentials to .env
- Use test mode keys for testing
- Verify webhook secret is set

### Bot not responding
- Check Telegram bot token
- Verify bot is running
- Check logs for errors

---

**Need help? Check the logs or run the test suite!**
