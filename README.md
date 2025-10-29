# 🌟 My Prabh AI - Revolutionary AI Companion

Complete AI companion system with 35+ models, story-based personalization, and real-time features.

## 🚀 Features

### AI Generation
- **Image Generation** - 4 models (including NSFW)
- **Video Generation** - 3 models
- **Audio Generation** - 4 models (TTS + Music)

### Analysis
- **Image Analysis** - 9 models
- **Video Analysis** - 1 model
- **Audio Analysis** - 2 models
- **Text Processing** - 10 models
- **Visual QA** - 2 models

### Bot Features
- Story upload and analysis
- Character extraction
- Theme identification
- Interactive generation
- Payment integration

### Infrastructure
- Redis pub/sub
- SocketIO real-time
- Rate limiting
- Tier-based access

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Abhaythakurrr/prabhtelebot.git
cd prabhtelebot

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run
python start.py
```

## 🔐 Environment Setup

See `RAILWAY_ENV_PASTE_THIS.txt` for complete environment variables.

Required:
- Telegram Bot Token
- Bytez API Keys (for 35 models)
- Razorpay Keys (for payments)
- Redis URL (for real-time)
- ElevenLabs Key (for voice)

## 🚀 Deployment

### Railway:
1. Copy `RAILWAY_ENV_PASTE_THIS.txt` to Railway Variables
2. Push code to GitHub
3. Railway auto-deploys

### Local:
```bash
python start.py
```

## 📊 Architecture

```
┌─────────────────┐
│  Telegram Bot   │
│  - Commands     │
│  - Generation   │
│  - Story        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Redis       │
│  - Pub/Sub      │
│  - Caching      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Website      │
│  - Flask        │
│  - SocketIO     │
│  - Payment      │
└─────────────────┘
```

## 🎯 Usage

### Telegram Bot:
```
/start - Welcome and menu
/generate - Generate content
```

### Website:
```
http://localhost:8000 - Home
http://localhost:8000/pricing - Pricing
```

## 📝 License

Private project

## 👨‍💻 Author

Prabh AI Team

## 🎉 Status

✅ Production Ready
✅ 35 AI Models
✅ Complete Features
✅ Secure & Scalable
