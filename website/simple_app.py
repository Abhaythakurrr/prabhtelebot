"""
Simple Flask Website - No Template Dependencies
"""

from flask import Flask, jsonify, Response
from flask_socketio import SocketIO
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def home():
    """Home page"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Prabh AI - Revolutionary AI Companion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { max-width: 1200px; text-align: center; }
        h1 { font-size: 3.5rem; margin-bottom: 20px; text-shadow: 2px 2px 20px rgba(0,0,0,0.3); }
        .tagline { font-size: 1.5rem; margin-bottom: 40px; opacity: 0.95; }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s;
        }
        .feature:hover { transform: translateY(-10px); }
        .feature-icon { font-size: 3rem; margin-bottom: 15px; }
        .feature-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 10px; }
        .btn {
            display: inline-block;
            padding: 18px 40px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 50px;
            text-decoration: none;
            margin: 10px;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .btn-primary { background: white; color: #667eea; }
        .btn-primary:hover { transform: translateY(-3px); }
        .btn-secondary { background: rgba(255,255,255,0.2); color: white; border: 2px solid white; }
        .btn-secondary:hover { background: white; color: #667eea; }
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>My Prabh AI</h1>
        <p class="tagline">Revolutionary AI Companion with Deep Personality & NSFW Capabilities</p>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Deep Roleplay</div>
                <p>Story-based conversations with memory</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎨</div>
                <div class="feature-title">Image Generation</div>
                <p>35+ AI models, anime, realistic, NSFW</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎬</div>
                <div class="feature-title">Video Creation</div>
                <p>Text-to-video with HD quality</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔞</div>
                <div class="feature-title">NSFW Content</div>
                <p>Adult roleplay & explicit generation</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Memory System</div>
                <p>Remembers your preferences & history</p>
            </div>
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Proactive AI</div>
                <p>Initiates conversations naturally</p>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <a href="https://t.me/kanuji_bot" class="btn btn-primary">Start Free on Telegram</a>
            <a href="/pricing" class="btn btn-secondary">View Pricing</a>
        </div>
    </div>
</body>
</html>
    """
    return Response(html, mimetype='text/html')


@app.route('/pricing')
def pricing():
    """Pricing page"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing - My Prabh AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { text-align: center; font-size: 3.5rem; margin-bottom: 20px; }
        .subtitle { text-align: center; font-size: 1.3rem; margin-bottom: 60px; opacity: 0.9; }
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }
        .plan {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            border: 2px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
        }
        .plan:hover { transform: translateY(-15px); box-shadow: 0 30px 60px rgba(0,0,0,0.4); }
        .plan-popular { border: 3px solid #FFD700; }
        .popular-badge {
            background: #FFD700;
            color: #667eea;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 20px;
        }
        .plan-icon { font-size: 4rem; margin-bottom: 20px; }
        .plan-name { font-size: 2rem; font-weight: 800; margin-bottom: 15px; }
        .plan-price { font-size: 3rem; font-weight: 800; color: #FFD700; margin-bottom: 10px; }
        .plan-period { font-size: 1rem; opacity: 0.8; margin-bottom: 30px; }
        .plan-features { list-style: none; margin-bottom: 30px; }
        .plan-features li { padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .btn {
            width: 100%;
            padding: 18px;
            font-size: 1.1rem;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            text-decoration: none;
            display: block;
            text-align: center;
            transition: all 0.3s;
        }
        .btn-primary { background: white; color: #667eea; }
        .btn-primary:hover { background: #FFD700; transform: scale(1.05); }
        .btn-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #333; }
        .btn-gold:hover { transform: scale(1.05); }
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .pricing-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Choose Your Plan</h1>
        <p class="subtitle">Unlock the full power of AI companionship</p>
        
        <div class="pricing-grid">
            <div class="plan">
                <div class="plan-icon">🆓</div>
                <div class="plan-name">FREE</div>
                <div class="plan-price">₹0</div>
                <div class="plan-period">Forever</div>
                <ul class="plan-features">
                    <li>✅ 10 messages/day</li>
                    <li>✅ 1 image/month</li>
                    <li>✅ Basic AI models</li>
                    <li>❌ No videos</li>
                    <li>❌ No NSFW</li>
                </ul>
                <a href="https://t.me/kanuji_bot" class="btn btn-primary">Start Free</a>
            </div>
            
            <div class="plan">
                <div class="plan-icon">💎</div>
                <div class="plan-name">BASIC</div>
                <div class="plan-price">₹299</div>
                <div class="plan-period">per month</div>
                <ul class="plan-features">
                    <li>✅ Unlimited messages</li>
                    <li>✅ 50 images/month</li>
                    <li>✅ 5 videos/month</li>
                    <li>✅ 100 audio/month</li>
                    <li>❌ No NSFW</li>
                </ul>
                <a href="https://t.me/kanuji_bot" class="btn btn-primary">Subscribe</a>
            </div>
            
            <div class="plan plan-popular">
                <div class="popular-badge">POPULAR</div>
                <div class="plan-icon">👑</div>
                <div class="plan-name">PRIME</div>
                <div class="plan-price">₹899</div>
                <div class="plan-period">per month</div>
                <ul class="plan-features">
                    <li>✅ Unlimited messages</li>
                    <li>✅ 500 images/month</li>
                    <li>✅ 50 videos/month</li>
                    <li>✅ 500 audio/month</li>
                    <li>🔞 NSFW content</li>
                    <li>✅ Priority support</li>
                </ul>
                <a href="https://t.me/kanuji_bot" class="btn btn-gold">Get Prime</a>
            </div>
            
            <div class="plan">
                <div class="plan-icon">♾️</div>
                <div class="plan-name">LIFETIME</div>
                <div class="plan-price">₹2999</div>
                <div class="plan-period">one-time payment</div>
                <ul class="plan-features">
                    <li>✅ Unlimited everything</li>
                    <li>✅ All features forever</li>
                    <li>🔞 NSFW content</li>
                    <li>✅ VIP support</li>
                    <li>✅ No recurring fees</li>
                </ul>
                <a href="https://t.me/kanuji_bot" class="btn btn-gold">Buy Lifetime</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 60px;">
            <a href="/" style="color: white; text-decoration: none; font-size: 1.2rem;">← Back to Home</a>
        </div>
    </div>
</body>
</html>
    """
    return Response(html, mimetype='text/html')


@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "My Prabh AI", "models": 35})


@app.route('/api/status')
def status():
    """API status"""
    return jsonify({
        "status": "online",
        "bot": "active",
        "website": "active",
        "features": {
            "roleplay": True,
            "image_generation": True,
            "video_generation": True,
            "nsfw": True,
            "memory": True
        }
    })


# SocketIO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


def run_website(port=8000):
    """Run the website"""
    try:
        logger.info(f"Starting website on port {port}...")
        socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
    except Exception as e:
        logger.error(f"Website error: {e}")
        # Fallback to basic Flask
        app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    run_website()
