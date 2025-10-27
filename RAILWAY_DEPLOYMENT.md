# 🚀 Railway Deployment Guide - AI Companion Platform

Deploy your complete AI Companion Bot + Website to Railway with this guide.

## 🎯 What Gets Deployed

### 🤖 **Telegram Bot**
- Multi-AI model integration (Mistral, Nemotron, Llama, Dolphin)
- Voice cloning and processing
- Story analysis and memory
- Image generation
- NSFW content with Venice model
- Proactive messaging system

### 🌐 **Website**
- Futuristic cyberpunk love theme
- User onboarding and setup
- Payment integration (Razorpay)
- File upload system
- Dashboard and management

## 📋 Pre-Deployment Checklist

### ✅ **Required Accounts**
- [ ] Railway account (railway.app)
- [ ] GitHub repository with your code
- [ ] Telegram Bot Token (@BotFather)
- [ ] OpenRouter API keys (for AI models)
- [ ] Razorpay account (for payments)

### ✅ **Environment Variables Ready**
- [ ] All API keys collected
- [ ] Payment gateway configured
- [ ] Bot token verified

## 🚀 Deployment Steps

### 1. **Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2. **Deploy to Railway**

#### Option A: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### Option B: Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect and deploy

### 3. **Configure Environment Variables**

In Railway dashboard, go to your project → Variables tab and add:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY
TELEGRAM_USE_POLLING=true

# AI Models
MISTRAL_API_KEY=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
NEMOTRON_API_KEY=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
LLAMA_API_KEY=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
LLAMA4_API_KEY=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
DOLPHIN_API_KEY=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

# Payment
RAZORPAY_KEY_ID=rzp_live_RFCUrmIElPNS5m
RAZORPAY_KEY_SECRET=IzybX6ykve4VJ8GxldZhVJEC

# Flask
FLASK_SECRET_KEY=your-super-secret-key-here
```

### 4. **Verify Deployment**

After deployment:
- ✅ Check Railway logs for successful startup
- ✅ Test website at your Railway URL
- ✅ Test Telegram bot (@kanuji_bot)
- ✅ Verify payment integration
- ✅ Test file uploads

## 🔧 Configuration Details

### **Railway Configuration Files**
- `Procfile` - Defines how to start the application
- `railway.json` - Railway-specific settings
- `start.py` - Unified startup script
- `requirements.txt` - Python dependencies

### **Application Structure**
```
├── src/                 # Telegram bot code
├── website/            # Flask website
├── start.py           # Unified startup
├── Procfile          # Railway process definition
├── railway.json      # Railway configuration
└── requirements.txt  # Dependencies
```

## 🎨 Cyberpunk Love Theme Features

### **Visual Design**
- 🌈 Neon pink, cyan, purple color scheme
- ✨ Glassmorphism effects with backdrop blur
- 🔮 Animated neon glows and particle effects
- 💫 Cyberpunk typography (Orbitron, Rajdhani)

### **Love Theme Elements**
- 💕 Romantic and passionate color gradients
- 🔥 Sensual UI animations
- 💖 Intimate messaging and NSFW content
- 🌹 Fantasy-themed interactions

## 🚨 Troubleshooting

### **Common Issues**

#### Bot Not Starting
```bash
# Check Railway logs
railway logs

# Verify environment variables
railway variables
```

#### Website Not Loading
- Check PORT environment variable
- Verify Flask app is binding to 0.0.0.0
- Check Railway domain configuration

#### Payment Issues
- Verify Razorpay keys are correct
- Check webhook URLs
- Test payment flow in Railway environment

### **Debug Commands**
```bash
# View logs
railway logs --tail

# Check environment
railway shell
env | grep -E "(TELEGRAM|RAZORPAY|API_KEY)"

# Restart service
railway redeploy
```

## 📊 Monitoring

### **Health Checks**
- Website: `https://your-app.railway.app/health`
- Bot status: Check Railway logs
- Payment system: Test transactions

### **Performance**
- Railway provides built-in metrics
- Monitor memory and CPU usage
- Check response times

## 🎯 Post-Deployment

### **Testing Checklist**
- [ ] Website loads with cyberpunk theme
- [ ] User registration works
- [ ] File uploads function
- [ ] Payment processing works
- [ ] Telegram bot responds
- [ ] AI conversations work
- [ ] Voice processing active
- [ ] Image generation works
- [ ] NSFW mode functions

### **Go Live**
1. Update DNS (if using custom domain)
2. Configure SSL certificate
3. Set up monitoring alerts
4. Test all user flows
5. Announce to users!

## 🎉 Success!

Your AI Companion Platform is now live on Railway with:
- 🤖 **Fully functional Telegram bot**
- 🌐 **Cyberpunk love-themed website**
- 💳 **Live payment processing**
- 🎨 **AI image generation**
- 🔥 **NSFW content capabilities**
- 💕 **Romantic AI interactions**

**Bot URL**: @kanuji_bot
**Website**: https://your-app.railway.app

Ready to serve users with the ultimate AI companion experience! 🚀💖