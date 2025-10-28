# 🚀 Deploy Latest Changes to Production

## Current Status

✅ **Local:** All changes working (payment, image generation, bot)
❌ **Production:** Showing old website without payment endpoints

## What Needs to Be Done

Your production server needs to pull the latest code from GitHub.

---

## Deployment Steps

### Option 1: If Using Railway/Render/Heroku

These platforms auto-deploy from GitHub. Just trigger a redeploy:

**Railway:**
```bash
# Go to Railway dashboard
# Click on your project
# Click "Deploy" or "Redeploy"
# Or push a new commit to trigger auto-deploy
```

**Render:**
```bash
# Go to Render dashboard
# Click "Manual Deploy" > "Deploy latest commit"
```

**Heroku:**
```bash
# In your local terminal
git push heroku main
```

---

### Option 2: If Using VPS/Custom Server

SSH into your server and pull latest changes:

```bash
# SSH into your server
ssh user@your-server-ip

# Navigate to project directory
cd /path/to/prabhtelebot

# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Restart the bot
# If using systemd:
sudo systemctl restart prabh-bot

# If using PM2:
pm2 restart prabh-bot

# If using screen/tmux:
# Stop the current process (Ctrl+C)
# Then restart:
python start.py
```

---

### Option 3: Manual File Upload

If you can't use git on production:

1. **Download these files from your local:**
   - `website/app.py` (has payment endpoints)
   - `src/generation/content_generator.py` (has list format handling)
   - `start.py` (has .env loading)

2. **Upload to production server**

3. **Restart the bot**

---

## Verify Deployment

After deploying, test these:

### 1. Check Website
```bash
curl https://your-domain.com/api/status
```

Should return:
```json
{
  "status": "operational",
  "features": {
    "telegram_bot": "active",
    ...
  }
}
```

### 2. Test Payment Endpoint
```bash
curl -X POST https://your-domain.com/api/create-order \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","plan_id":"basic"}'
```

Should return order details with `order_id`.

### 3. Test Website
Visit: `https://your-domain.com/pricing`

Click "Subscribe Now" button - should show payment modal.

---

## Environment Variables

Make sure production has these environment variables:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_token

# Bytez (Image/Video)
BYTEZ_API_KEY_1=1043901e59687190c4eebd9f12f08f2d
BYTEZ_API_KEY_2=1043901e59687190c4eebd9f12f08f2d

# Razorpay (Payment)
RAZORPAY_KEY_ID=rzp_live_RFCUrmIElPNS5m
RAZORPAY_KEY_SECRET=your_secret

# OpenRouter (AI)
OPENROUTER_API_KEY=your_key
```

---

## What Changed

### Commit: `b4bb239`
**Title:** CRITICAL FIXES: Image/Video Generation + Payment System Working

**Changes:**
1. ✅ `website/app.py` - Added 5 payment API endpoints
2. ✅ `src/generation/content_generator.py` - Fixed image/video generation
3. ✅ `src/bot/message_templates.py` - Modern bot UI
4. ✅ `src/bot/modern_keyboards.py` - Beautiful keyboards

### Commit: `d2a1e43`
**Title:** FIX: Bot now loads .env and runs correctly

**Changes:**
1. ✅ `start.py` - Added .env loading
2. ✅ `delete_webhook.py` - Webhook deletion script

---

## Quick Deploy Commands

### For Railway:
```bash
# Trigger redeploy
railway up
```

### For Render:
```bash
# Manual deploy from dashboard
# Or push to trigger auto-deploy
git commit --allow-empty -m "Trigger deploy"
git push origin main
```

### For VPS:
```bash
ssh user@server "cd /path/to/project && git pull && pip install -r requirements.txt && sudo systemctl restart prabh-bot"
```

---

## Troubleshooting

### Issue: Still seeing old website
**Solution:** Clear browser cache or use incognito mode

### Issue: Payment button not working
**Solution:** Check browser console (F12) for JavaScript errors

### Issue: API endpoints returning 404
**Solution:** Make sure `website/app.py` was updated and server restarted

### Issue: Bot not responding
**Solution:** Check if webhook is deleted: `python delete_webhook.py`

---

## Verification Checklist

After deployment, verify:

- [ ] Website loads: `https://your-domain.com`
- [ ] Pricing page loads: `https://your-domain.com/pricing`
- [ ] Payment button shows modal (not just alert)
- [ ] API endpoint works: `/api/create-order`
- [ ] Bot responds in Telegram
- [ ] `/generate` command works
- [ ] Image generation works

---

## Need Help?

If deployment fails:

1. Check server logs
2. Verify environment variables
3. Test API endpoints manually
4. Check if port 8000 is accessible
5. Verify git pull succeeded

---

## Summary

**What to do:**
1. Go to your production server/platform
2. Pull latest code: `git pull origin main`
3. Restart the bot
4. Test payment button

**Expected result:**
- ✅ Payment button opens Razorpay modal
- ✅ Image generation works
- ✅ Bot responds correctly

---

## Status After Deployment

Once deployed, everything should work:
- ✅ Payment system functional
- ✅ Image generation working
- ✅ Video generation working
- ✅ Bot personality correct
- ✅ Modern UI active

🚀 **Ready to deploy!**
