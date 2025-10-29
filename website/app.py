"""
Flask Website - Minimal Working Version
"""

from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO
from src.core.config import get_config
from src.payment.razorpay import get_payment_handler

app = Flask(__name__)
config = get_config()
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def home():
    """Home page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Prabh AI - Revolutionary AI Companion</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 800px;
                padding: 40px;
                text-align: center;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            p {
                font-size: 1.2rem;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                margin: 10px;
                transition: transform 0.3s;
            }
            .btn:hover {
                transform: translateY(-3px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 My Prabh AI</h1>
            <p>Revolutionary AI Companion with 35+ Models</p>
            <p>Image Generation • Video Creation • Voice Synthesis • Story-Based Personalization</p>
            <a href="https://t.me/kanuji_bot" class="btn">🤖 Open Telegram Bot</a>
            <a href="/pricing" class="btn">💎 View Pricing</a>
        </div>
    </body>
    </html>
    """)


@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pricing - My Prabh AI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { text-align: center; font-size: 3rem; margin-bottom: 40px; }
            .plans {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 30px;
            }
            .plan {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                transition: transform 0.3s;
            }
            .plan:hover { transform: translateY(-10px); }
            .plan h2 { font-size: 2rem; margin-bottom: 20px; }
            .price { font-size: 2.5rem; margin: 20px 0; color: #FFD700; }
            .features { list-style: none; margin: 20px 0; }
            .features li { padding: 8px 0; }
            .btn {
                display: block;
                padding: 15px;
                background: white;
                color: #667eea;
                text-align: center;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💎 Pricing Plans</h1>
            <div class="plans">
                <div class="plan">
                    <h2>🆓 FREE</h2>
                    <div class="price">₹0</div>
                    <ul class="features">
                        <li>✅ 10 messages/day</li>
                        <li>✅ 1 image/month</li>
                        <li>✅ Basic AI</li>
                    </ul>
                    <a href="https://t.me/kanuji_bot" class="btn">Start Free</a>
                </div>
                <div class="plan">
                    <h2>💎 BASIC</h2>
                    <div class="price">₹299</div>
                    <ul class="features">
                        <li>✅ Unlimited messages</li>
                        <li>✅ 50 images/month</li>
                        <li>✅ 5 videos/month</li>
                    </ul>
                    <a href="#" class="btn">Subscribe</a>
                </div>
                <div class="plan">
                    <h2>👑 PRIME</h2>
                    <div class="price">₹899</div>
                    <ul class="features">
                        <li>✅ 500 images/month</li>
                        <li>✅ 50 videos/month</li>
                        <li>✅ NSFW content</li>
                    </ul>
                    <a href="#" class="btn">Subscribe</a>
                </div>
                <div class="plan">
                    <h2>♾️ LIFETIME</h2>
                    <div class="price">₹2999</div>
                    <ul class="features">
                        <li>✅ Unlimited everything</li>
                        <li>✅ All features forever</li>
                        <li>✅ VIP support</li>
                    </ul>
                    <a href="#" class="btn">Buy Lifetime</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "models": 35})


# SocketIO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


def run_website():
    """Run the website"""
    socketio.run(app, host='0.0.0.0', port=config.port, debug=False)


if __name__ == '__main__':
    run_website()
