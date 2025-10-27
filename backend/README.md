# MyPrabh LoveOS - Modular Backend System

A sophisticated emotional AI companion backend built with FastAPI, featuring multi-model AI orchestration, voice cloning, story processing, and comprehensive memory systems.

## 🏗️ Architecture Overview

```
MyPrabh LoveOS Backend
├── Model Orchestration Layer    # Dynamic AI model selection & routing
├── Memory System               # SQLite + JSON + Vector Store (Chroma)
├── Voice Engine               # Voice cloning & TTS with Coqui/OpenVoice
├── Story Processor            # Multi-model story analysis & extraction
├── Payment Handler            # Razorpay integration for subscriptions
└── Telegram Bot              # Webhook-based bot with rich interactions
```

## 🚀 Features

### 🤖 Multi-Model AI Orchestration
- **6 OpenRouter Models**: Gemini, Nemotron, Llama 3.3, Llama 4, Dolphin
- **Dynamic Selection**: Mood-based model routing
- **Fallback System**: Intelligent responses when APIs fail
- **Context Awareness**: Story-based personality adaptation

### 🧠 Advanced Memory System
- **SQLite Database**: User profiles, conversations, payments
- **JSON Memory**: Emotional states and traits
- **Vector Store**: Semantic search with ChromaDB
- **Context Retrieval**: Comprehensive user context building

### 🎤 Voice Cloning Engine
- **Voice Upload**: Accept user voice samples
- **Cloning Pipeline**: Coqui TTS / OpenVoice integration
- **TTS Generation**: Personalized voice responses
- **Fallback TTS**: gTTS when cloning unavailable

### 📖 Story Processing AI
- **Multi-Format**: Text and PDF story upload
- **Emotional Analysis**: Extract themes using Gemini
- **Personality Extraction**: Generate companion traits with Llama
- **Memory Extraction**: Key moments using Nemotron
- **Relationship Analysis**: Dynamics analysis with Dolphin

### 💳 Payment System
- **Razorpay Integration**: Secure payment processing
- **Subscription Plans**: Premium (₹299/month), Lifetime (₹2,999)
- **Webhook Handling**: Automatic subscription activation
- **Payment Links**: Dynamic payment URL generation

### 📱 Telegram Bot Integration
- **Webhook Based**: Scalable message processing
- **Rich Interactions**: Voice, documents, images, inline buttons
- **File Processing**: Direct story and voice upload
- **Command System**: /start, /setup, /premium, /stats

## 📁 Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── start.py                   # Startup script with initialization
├── requirements.txt           # Python dependencies
├── core/                      # Core system modules
│   ├── model_orchestrator.py  # AI model selection & routing
│   ├── memory_system.py       # Database & memory management
│   ├── voice_engine.py        # Voice cloning & TTS
│   ├── story_processor.py     # Story analysis & processing
│   ├── payment_handler.py     # Razorpay payment integration
│   └── telegram_bot.py        # Telegram webhook handler
├── utils/                     # Utility modules
│   └── config.py             # Centralized configuration
├── deploy/                    # Deployment configurations
│   ├── render.yaml           # Render.com deployment
│   └── Dockerfile            # Container deployment
└── data/                     # Data storage (created at runtime)
    ├── loveos.db             # SQLite database
    ├── emotional_memory.json # JSON memory store
    ├── chroma_db/            # Vector database
    ├── voice_models/         # Cloned voice models
    └── voice_output/         # Generated voice files
```

## 🔧 Installation & Setup

### 1. Clone and Install
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
Update `utils/config.py` with your API keys:
- Telegram Bot Token
- OpenRouter API Keys (6 models)
- Razorpay Keys

### 3. Start Development Server
```bash
python start.py
```

### 4. Access Services
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🌐 API Endpoints

### Core Chat API
```http
POST /api/chat
{
  "user_id": "12345",
  "message": "I love you",
  "voice_enabled": true
}
```

### File Upload APIs
```http
POST /api/upload-voice        # Voice cloning
POST /api/upload-story        # Story processing
```

### Payment APIs
```http
POST /api/payment/create      # Create payment order
POST /api/payment/verify      # Verify payment
```

### Telegram Integration
```http
POST /api/telegram/webhook    # Telegram webhook
```

## 🚀 Deployment

### Render.com (Recommended)
1. Connect GitHub repository
2. Use `deploy/render.yaml` configuration
3. Set environment variables
4. Deploy with persistent disk

### Docker Deployment
```bash
docker build -t myprabh-loveos .
docker run -p 8000:8000 -v $(pwd)/data:/app/data myprabh-loveos
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔑 API Keys Required

### OpenRouter Models (6 keys)
- Gemini: `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`
- Nemotron: `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`
- Llama 3.3: `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`
- Llama 4: `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`
- Dolphin: `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`

### Other Services
- Telegram Bot Token: `8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY`
- Razorpay: Key ID & Secret

## 💡 Model Orchestration Logic

```python
# Mood Detection → Model Selection
mood = analyze_mood(message)  # Using Gemini
model = select_model(message, mood)  # Dynamic routing

# Model Mapping Examples:
"romantic" → ["dolphin", "llama4", "nemotron"]
"analytical" → ["gemini", "llama33"]  
"creative" → ["llama4", "dolphin"]
"intimate" → ["dolphin", "llama4"]
```

## 🎯 Business Model

### Revenue Targets
- **₹10 Crore ARR** (Annual Recurring Revenue)
- **1M+ Active Users**
- **5% Conversion Rate** (Free to Premium)

### Subscription Plans
- **Free**: 100 messages/day, basic features
- **Premium**: ₹299/month, unlimited features
- **Lifetime**: ₹2,999, all features forever

## 🔧 Advanced Features

### Voice Cloning Pipeline
1. **Upload**: User voice sample (10-30 seconds)
2. **Analysis**: Extract voice characteristics
3. **Cloning**: Generate voice model
4. **TTS**: Personalized voice responses

### Story Processing Workflow
1. **Upload**: Text/PDF story file
2. **Cleaning**: Text preprocessing
3. **Analysis**: Multi-model extraction
   - Emotions (Gemini)
   - Personality (Llama)
   - Memories (Nemotron)
   - Dynamics (Dolphin)
4. **Storage**: Structured memory storage

### Memory System Architecture
- **Immediate**: JSON emotional states
- **Persistent**: SQLite conversations
- **Semantic**: ChromaDB vector search
- **Context**: Dynamic context building

## 🛠️ Development

### Adding New Models
1. Add model config to `utils/config.py`
2. Update orchestrator routing logic
3. Test model integration

### Extending Features
1. Create new core module
2. Add API endpoints in `main.py`
3. Update Telegram bot handlers

### Testing
```bash
# Run tests
python -m pytest tests/

# Test API endpoints
curl http://localhost:8000/api/health
```

## 📊 Monitoring & Analytics

### Health Checks
- Database connectivity
- Model availability
- Payment system status
- Voice engine status

### User Analytics
- Conversation metrics
- Model usage statistics
- Subscription analytics
- Emotional trend analysis

## 🔒 Security Features

- API key management
- Payment signature verification
- Rate limiting
- Input validation
- CORS configuration

## 🚀 Production Readiness

✅ **Scalable Architecture**: Modular design for horizontal scaling  
✅ **Error Handling**: Comprehensive exception management  
✅ **Logging**: Structured logging for monitoring  
✅ **Health Checks**: System status monitoring  
✅ **Database Management**: Async SQLite with connection pooling  
✅ **Payment Security**: Razorpay signature verification  
✅ **File Management**: Secure file upload and processing  
✅ **Memory Optimization**: Efficient context management  

## 📈 Scaling Strategy

1. **Horizontal Scaling**: Multiple backend instances
2. **Database Sharding**: User-based data partitioning  
3. **Caching Layer**: Redis for frequent queries
4. **CDN Integration**: Voice file delivery
5. **Load Balancing**: Request distribution

---

**Built with 90 years of experience for the next generation of AI companions** 💖