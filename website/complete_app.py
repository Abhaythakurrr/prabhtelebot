"""
Complete Flask Website with Payment Integration and User Dashboard
"""

from flask import Flask, request, jsonify, Response, redirect, session
from flask_socketio import SocketIO, emit
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.payment.razorpay import get_payment_handler
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

app = Flask(__name__)
config = get_config()
app.config['SECRET_KEY'] = config.razorpay_key_secret or 'change-this-secret-key'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize managers
user_manager = get_user_manager()
payment_handler = get_payment_handler()


@app.route('/')
def home():
    """Home page with features and CTA"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Prabh AI - Revolutionary AI Companion Bot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            overflow-x: hidden;
        }
        .nav {
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        .nav-logo { font-size: 1.5rem; font-weight: 800; }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 30px;
            font-weight: 600;
            transition: opacity 0.3s;
        }
        .nav-links a:hover { opacity: 0.7; }
        .hero {
            min-height: 90vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 4rem; margin-bottom: 20px; text-shadow: 2px 2px 20px rgba(0,0,0,0.3); }
        .tagline { font-size: 1.5rem; margin-bottom: 40px; opacity: 0.95; }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s;
        }
        .feature:hover { transform: translateY(-10px); }
        .feature-icon { font-size: 3.5rem; margin-bottom: 20px; }
        .feature-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 15px; }
        .btn {
            display: inline-block;
            padding: 20px 50px;
            font-size: 1.2rem;
            font-weight: 700;
            border-radius: 50px;
            text-decoration: none;
            margin: 15px;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .btn-primary { background: white; color: #667eea; }
        .btn-primary:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.4); }
        .btn-secondary { background: rgba(255,255,255,0.2); color: white; border: 2px solid white; }
        .btn-secondary:hover { background: white; color: #667eea; }
        .stats {
            display: flex;
            justify-content: center;
            gap: 80px;
            margin: 60px 0;
            flex-wrap: wrap;
        }
        .stat { text-align: center; }
        .stat-number { font-size: 3.5rem; font-weight: 900; color: #FFD700; }
        .stat-label { font-size: 1.1rem; opacity: 0.9; margin-top: 10px; }
        .section {
            padding: 80px 20px;
            background: rgba(0,0,0,0.1);
        }
        .section h2 { font-size: 3rem; text-align: center; margin-bottom: 60px; }
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .features { grid-template-columns: 1fr; }
            .nav { flex-direction: column; gap: 20px; }
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-logo">My Prabh AI</div>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/pricing">Pricing</a>
            <a href="/dashboard">Dashboard</a>
            <a href="https://t.me/kanuji_bot">Bot</a>
        </div>
    </nav>
    
    <div class="hero">
        <div class="container">
            <h1>Your AI Companion Awaits</h1>
            <p class="tagline">Deep Roleplay • NSFW Content • Memory System • 35+ AI Models</p>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">35+</div>
                    <div class="stat-label">AI Models</div>
                </div>
                <div class="stat">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Available</div>
                </div>
                <div class="stat">
                    <div class="stat-number">∞</div>
                    <div class="stat-label">Possibilities</div>
                </div>
            </div>
            
            <div>
                <a href="https://t.me/kanuji_bot" class="btn btn-primary">Start Free on Telegram</a>
                <a href="/pricing" class="btn btn-secondary">View Pricing</a>
            </div>
        </div>
    </div>
    
    <div class="section">
        <div class="container">
            <h2>Powerful Features</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">💬</div>
                    <div class="feature-title">Deep Roleplay</div>
                    <p>Story-based conversations with context awareness and memory</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-title">Image Generation</div>
                    <p>Multiple styles: Normal, Anime, Realistic, NSFW</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎬</div>
                    <div class="feature-title">Video Creation</div>
                    <p>Text-to-video with HD quality options</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🔞</div>
                    <div class="feature-title">NSFW Content</div>
                    <p>Adult roleplay and explicit generation (Premium)</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🧠</div>
                    <div class="feature-title">Memory System</div>
                    <p>AI remembers your preferences and conversation history</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Proactive AI</div>
                    <p>Initiates conversations and checks in on you</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    return Response(html, mimetype='text/html')


@app.route('/pricing')
def pricing():
    """Pricing page with payment integration"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing - My Prabh AI</title>
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .nav {
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
        }
        .nav-logo { font-size: 1.5rem; font-weight: 800; }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 30px;
            font-weight: 600;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { text-align: center; font-size: 3.5rem; margin-bottom: 20px; }
        .subtitle { text-align: center; font-size: 1.3rem; margin-bottom: 60px; opacity: 0.9; }
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
        }
        .plan {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            border: 2px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
            position: relative;
        }
        .plan:hover { transform: translateY(-15px); box-shadow: 0 30px 60px rgba(0,0,0,0.4); }
        .plan-popular { border: 3px solid #FFD700; }
        .popular-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #FFD700;
            color: #667eea;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
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
    <nav class="nav">
        <div class="nav-logo">My Prabh AI</div>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/pricing">Pricing</a>
            <a href="/dashboard">Dashboard</a>
        </div>
    </nav>
    
    <div class="container">
        <h1>Choose Your Plan</h1>
        <p class="subtitle">Start free, upgrade anytime for unlimited power</p>
        
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
                    <li>✅ 10 memory slots</li>
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
                    <li>✅ 50 memory slots</li>
                    <li>✅ Proactive messages</li>
                    <li>❌ No NSFW</li>
                </ul>
                <button onclick="buyPlan('basic', 299)" class="btn btn-primary">Subscribe Now</button>
            </div>
            
            <div class="plan plan-popular">
                <div class="popular-badge">MOST POPULAR</div>
                <div class="plan-icon">👑</div>
                <div class="plan-name">PRIME</div>
                <div class="plan-price">₹899</div>
                <div class="plan-period">per month</div>
                <ul class="plan-features">
                    <li>✅ Unlimited messages</li>
                    <li>✅ 500 images/month</li>
                    <li>✅ 50 videos/month</li>
                    <li>✅ 500 audio/month</li>
                    <li>✅ 200 memory slots</li>
                    <li>✅ Proactive messages</li>
                    <li>🔞 NSFW content</li>
                    <li>✅ Priority support</li>
                </ul>
                <button onclick="buyPlan('prime', 899)" class="btn btn-gold">Get Prime Now</button>
            </div>
            
            <div class="plan">
                <div class="plan-icon">♾️</div>
                <div class="plan-name">LIFETIME</div>
                <div class="plan-price">₹2999</div>
                <div class="plan-period">one-time payment</div>
                <ul class="plan-features">
                    <li>✅ Unlimited everything</li>
                    <li>✅ All features forever</li>
                    <li>✅ Unlimited memories</li>
                    <li>🔞 NSFW content</li>
                    <li>✅ VIP support</li>
                    <li>✅ Early access</li>
                    <li>✅ No recurring fees</li>
                    <li>💎 Lifetime updates</li>
                </ul>
                <button onclick="buyPlan('lifetime', 2999)" class="btn btn-gold">Buy Lifetime</button>
            </div>
        </div>
    </div>
    
    <script>
        function buyPlan(tier, amount) {
            // Get user ID from Telegram (you'll need to pass this)
            const userId = prompt("Enter your Telegram User ID (get it from the bot with /start):");
            if (!userId) {
                alert("User ID is required to purchase!");
                return;
            }
            
            // Create order
            fetch('/api/create-order', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    amount: amount,
                    tier: tier,
                    user_id: userId
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Open Razorpay checkout
                    const options = {
                        key: data.razorpay_key,
                        amount: data.amount,
                        currency: 'INR',
                        name: 'My Prabh AI',
                        description: tier.toUpperCase() + ' Subscription',
                        order_id: data.order_id,
                        handler: function(response) {
                            // Verify payment
                            fetch('/api/verify-payment', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({
                                    razorpay_order_id: response.razorpay_order_id,
                                    razorpay_payment_id: response.razorpay_payment_id,
                                    razorpay_signature: response.razorpay_signature,
                                    user_id: userId,
                                    tier: tier
                                })
                            })
                            .then(res => res.json())
                            .then(result => {
                                if (result.success) {
                                    alert('Payment successful! Your subscription is now active. Check the bot!');
                                    window.location.href = '/dashboard?user_id=' + userId;
                                } else {
                                    alert('Payment verification failed: ' + result.message);
                                }
                            });
                        },
                        prefill: {
                            name: 'User',
                            email: 'user@example.com'
                        },
                        theme: {
                            color: '#667eea'
                        }
                    };
                    const rzp = new Razorpay(options);
                    rzp.open();
                } else {
                    alert('Failed to create order: ' + data.message);
                }
            })
            .catch(err => {
                alert('Error: ' + err.message);
            });
        }
    </script>
</body>
</html>
    """
    return Response(html, mimetype='text/html')


@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return redirect('/pricing')
    
    try:
        user = user_manager.get_user(int(user_id))
        tier_info = user_manager.get_tier_info(user['tier'])
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - My Prabh AI</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 3rem; margin-bottom: 40px; }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        .card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .card h2 {{ font-size: 1.5rem; margin-bottom: 20px; }}
        .stat-row {{ display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .stat-label {{ opacity: 0.8; }}
        .stat-value {{ font-weight: 700; color: #FFD700; }}
        .btn {{
            display: inline-block;
            padding: 15px 30px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 700;
            margin-top: 20px;
            transition: transform 0.3s;
        }}
        .btn:hover {{ transform: translateY(-3px); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Your Dashboard</h1>
        
        <div class="dashboard-grid">
            <div class="card">
                <h2>Subscription</h2>
                <div class="stat-row">
                    <span class="stat-label">Current Tier:</span>
                    <span class="stat-value">{user['tier'].upper()}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Status:</span>
                    <span class="stat-value">Active</span>
                </div>
                <a href="/pricing" class="btn">Upgrade Plan</a>
            </div>
            
            <div class="card">
                <h2>Usage This Month</h2>
                <div class="stat-row">
                    <span class="stat-label">Messages Today:</span>
                    <span class="stat-value">{user['usage']['messages_today']}/{tier_info['messages_per_day']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Images:</span>
                    <span class="stat-value">{user['usage']['images_this_month']}/{tier_info['images_per_month']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Videos:</span>
                    <span class="stat-value">{user['usage']['videos_this_month']}/{tier_info['videos_per_month']}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>Features</h2>
                <div class="stat-row">
                    <span class="stat-label">NSFW Content:</span>
                    <span class="stat-value">{'✅ Enabled' if tier_info['nsfw_enabled'] else '❌ Disabled'}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Memory Slots:</span>
                    <span class="stat-value">{len(user['memories'])}/{tier_info['memory_slots']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Proactive Messages:</span>
                    <span class="stat-value">{'✅ Yes' if tier_info['proactive_messages'] else '❌ No'}</span>
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 60px;">
            <a href="https://t.me/kanuji_bot" class="btn">Open Telegram Bot</a>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </div>
</body>
</html>
        """
        return Response(html, mimetype='text/html')
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return redirect('/pricing')


@app.route('/api/create-order', methods=['POST'])
def create_order():
    """Create Razorpay order"""
    try:
        data = request.json
        amount = data['amount']
        tier = data['tier']
        user_id = data['user_id']
        
        # Create order
        order = payment_handler.create_order(amount, f"subscription_{tier}_{user_id}")
        
        if order:
            return jsonify({
                "success": True,
                "order_id": order['id'],
                "amount": order['amount'],
                "razorpay_key": config.razorpay_key_id
            })
        else:
            return jsonify({"success": False, "message": "Failed to create order"}), 400
            
    except Exception as e:
        logger.error(f"Create order error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """Verify payment and upgrade user"""
    try:
        data = request.json
        
        # Verify payment signature
        is_valid = payment_handler.verify_payment(
            data['razorpay_order_id'],
            data['razorpay_payment_id'],
            data['razorpay_signature']
        )
        
        if is_valid:
            # Upgrade user
            user_id = int(data['user_id'])
            tier = data['tier']
            duration = 30 if tier != "lifetime" else 999999
            
            user_manager.upgrade_subscription(user_id, tier, duration)
            
            logger.info(f"✅ Payment verified for user {user_id}, tier {tier}")
            
            return jsonify({
                "success": True,
                "message": "Payment successful! Your subscription is now active."
            })
        else:
            return jsonify({
                "success": False,
                "message": "Payment verification failed"
            }), 400
            
    except Exception as e:
        logger.error(f"❌ Payment verification error: {e}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "My Prabh AI",
        "bot": "active",
        "website": "active",
        "payment": "active"
    })


# SocketIO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('status', {'bot': 'online', 'website': 'online'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


def run_website(port=8000):
    """Run the website"""
    try:
        logger.info(f"🌐 Starting complete website on port {port}...")
        socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
    except Exception as e:
        logger.error(f"Website error: {e}")
        app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    run_website()
