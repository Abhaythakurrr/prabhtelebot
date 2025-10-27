"""
My Prabh - AI Companion Website
Simple Flask app for health checks and basic info
"""

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Prabh - AI Companion</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            .feature { background: rgba(255,255,255,0.1); padding: 20px; margin: 20px 0; border-radius: 10px; }
            .price { background: rgba(255,255,255,0.2); padding: 15px; margin: 10px; border-radius: 8px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 My Prabh - AI Companion 🌟</h1>
            <p>Your personal AI companion with advanced memory and 40+ AI models</p>
            
            <div class="feature">
                <h2>💎 Features</h2>
                <p>🧠 Memory-Driven AI • 🔥 NSFW Content • 🎵 Voice Cloning • 🎬 Video Generation • 🎨 Image Creation</p>
            </div>
            
            <div class="feature">
                <h2>💰 Pricing</h2>
                <div class="price">🆓 FREE<br>3 days trial</div>
                <div class="price">💎 BASIC<br>₹299/month</div>
                <div class="price">🔥 PREMIUM<br>₹599/month</div>
                <div class="price">👑 LIFETIME<br>₹2,999 one-time</div>
            </div>
            
            <div class="feature">
                <h2>🚀 Get Started</h2>
                <p>Message <strong>@kanuji_bot</strong> on Telegram to start!</p>
            </div>
            
            <div class="feature">
                <h2>📊 Revenue Projections</h2>
                <p>Year 1: ₹1.5 Crore • Year 2: ₹15 Crore • Year 3: ₹60 Crore → Unicorn! 🦄</p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "My Prabh AI Companion"}

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "features": {
            "telegram_bot": "active",
            "ai_models": "40+ models available",
            "monetization": "active",
            "revenue_tiers": ["free", "basic", "premium", "lifetime"]
        }
    }

if __name__ == '__main__':
    app.run(debug=False)