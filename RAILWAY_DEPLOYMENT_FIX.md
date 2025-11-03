# Railway Deployment Fix 🚂

## Issues Fixed

### 1. Multiple Instance Conflict ✅
**Error**: `Conflict: terminated by other getUpdates request`

**Cause**: Railway keeps old deployments alive during redeployment, causing conflicts.

**Solutions Implemented**:

#### A. Webhook Clearing on Startup
Added automatic webhook deletion before starting polling:
```python
# In src/main.py
async def clear_webhook():
    bot = Bot(token=config.telegram_token)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Cleared any existing webhooks")
```

#### B. Drop Pending Updates
```python
# In src/bot/advanced_handler.py
self.app.run_polling(
    allowed_updates=Update.ALL_TYPES,
    drop_pending_updates=True  # Ignore old updates
)
```

#### C. Retry Logic with Exponential Backoff
```python
max_retries = 3
retry_delay = 5

for attempt in range(max_retries):
    try:
        self.app.run_polling(...)
        break
    except Exception as e:
        if "Conflict" in str(e) and attempt < max_retries - 1:
            logger.warning(f"Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
            retry_delay *= 2  # 5s, 10s, 20s
```

### 2. Image URL Extraction ✅
**Error**: `Invalid file http url specified: unsupported url protocol`

**Fix**: Properly extract URL from Bytez Response objects
```python
if hasattr(result, 'output'):
    image_url = result.output
```

---

## Railway-Specific Configuration

### Environment Variables
Make sure these are set in Railway:
```
TELEGRAM_BOT_TOKEN=your_token
BYTEZ_API_KEY_1=your_key
TELEGRAM_USE_POLLING=true
PORT=8000
```

### Deployment Settings

#### 1. Health Check (Optional)
Railway URL: `https://your-app.railway.app/`
The website serves as health check.

#### 2. Start Command
Railway should use:
```
python start.py
```

#### 3. Build Command (if needed)
```
pip install -r requirements.txt
```

---

## How Railway Deployments Work

### Normal Flow:
1. You push to GitHub
2. Railway detects changes
3. Railway builds new deployment
4. Railway starts new instance
5. Railway stops old instance ← **Conflict happens here!**

### Our Fix:
1. New instance starts
2. Clears webhooks immediately
3. Drops pending updates
4. Retries if conflict detected
5. Old instance eventually stops
6. New instance takes over ✅

---

## Testing on Railway

### 1. Check Logs
In Railway dashboard:
- Look for: `✅ Cleared any existing webhooks`
- Look for: `🤖 Starting advanced bot...`
- Should NOT see: `Conflict: terminated by other getUpdates`

### 2. Test Bot
```
/start          # Should show new menu
/joke           # Test features
```

### 3. Test Image Generation
```
/start
Click "Create Image"
Select "Anime"
Enter: "cute anime girl watching sunset"
```
Should work now! ✅

---

## If Issues Persist

### Option 1: Manual Restart
In Railway dashboard:
1. Go to your service
2. Click "Restart"
3. Wait for new deployment

### Option 2: Redeploy
```bash
# Make a small change and push
git commit --allow-empty -m "Trigger Railway redeploy"
git push origin main
```

### Option 3: Check for Multiple Services
In Railway dashboard:
- Make sure you only have ONE service running the bot
- Delete any duplicate services

### Option 4: Check Bot Token
- Make sure the token is only used in ONE Railway service
- Not running locally AND on Railway simultaneously

---

## Monitoring

### Good Logs:
```
✅ Configuration loaded
✅ Cleared any existing webhooks
✅ Website thread started
🤖 Starting advanced bot...
✅ Advanced bot handlers registered
💕 Proactive messaging system started
Application started
```

### Bad Logs:
```
❌ Conflict: terminated by other getUpdates request
```
If you see this, the retry logic should kick in automatically.

---

## Railway Best Practices

### 1. Single Service
Only deploy the bot to ONE Railway service.

### 2. Environment Variables
Set all required env vars in Railway dashboard, not in code.

### 3. Graceful Shutdown
Our code now handles:
- Webhook clearing
- Pending update drops
- Retry logic
- Graceful errors

### 4. Logs
Always check Railway logs after deployment:
```
railway logs
```

### 5. Health Checks
The website at `/` serves as a health check for Railway.

---

## Files Modified

1. `src/main.py`:
   - Added webhook clearing on startup
   - Added graceful shutdown handling
   - Railway-specific initialization

2. `src/bot/advanced_handler.py`:
   - Added `drop_pending_updates=True`
   - Added retry logic with exponential backoff
   - Better error handling

3. `src/ai/generator.py`:
   - Fixed URL extraction from Bytez Response objects

---

## Deployment Checklist

Before deploying to Railway:

- [ ] All environment variables set
- [ ] Only ONE service running the bot
- [ ] Latest code pushed to GitHub
- [ ] Railway connected to correct branch
- [ ] Start command is `python start.py`
- [ ] Check logs after deployment
- [ ] Test bot functionality
- [ ] Test image generation

---

## Success Indicators

✅ Bot starts without conflicts
✅ Website accessible at Railway URL
✅ Commands work (`/start`, `/joke`)
✅ Image generation works
✅ Proactive messages work
✅ No error logs

---

## Support

If issues continue:
1. Check Railway logs
2. Verify environment variables
3. Ensure single service deployment
4. Try manual restart
5. Check bot token usage

---

## Status

✅ **Ready for Railway Deployment**

All Railway-specific issues have been addressed:
- Webhook conflicts: Fixed
- Multiple instances: Handled with retry logic
- Image URLs: Fixed
- Graceful shutdown: Implemented

Deploy with confidence! 🚂✨
