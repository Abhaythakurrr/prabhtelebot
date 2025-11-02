"""
Memory Lane - Beautiful Love-Focused Website
Handcrafted with care for preserving memories and love
"""

from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.payment.razorpay import get_payment_handler
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
config = get_config()
app.config['SECRET_KEY'] = config.razorpay_key_secret or 'memory-lane-secret'

socketio = SocketIO(app, cors_allowed_origins="*")
user_manager = get_user_manager()
payment_handler = get_payment_handler()


@app.route('/')
def home():
    """Beautiful home page"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Lane - Keep Love Alive Forever</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            color: #2c1810;
            overflow-x: hidden;
        }
        
        .nav {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 20px 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.05);
            z-index: 1000;
        }
        
        .logo {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #d4526e;
        }
        
        .nav-links a {
            margin-left: 40px;
            color: #2c1810;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #d4526e;
        }
        
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 100px 40px 60px;
            text-align: center;
        }
        
        .hero-content {
            max-width: 900px;
        }
        
        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 4.5rem;
            font-weight: 700;
            color: #d4526e;
            margin-bottom: 30px;
            line-height: 1.2;
        }
        
        .tagline {
            font-size: 1.5rem;
            color: #5a3a2a;
            margin-bottom: 50px;
            font-weight: 300;
            line-height: 1.6;
        }
        
        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 40px;
        }
        
        .btn {
            padding: 18px 45px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(212, 82, 110, 0.2);
        }
        
        .btn-primary {
            background: #d4526e;
            color: white;
        }
        
        .btn-primary:hover {
            background: #b8405a;
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(212, 82, 110, 0.3);
        }
        
        .btn-secondary {
            background: white;
            color: #d4526e;
            border: 2px solid #d4526e;
        }
        
        .btn-secondary:hover {
            background: #d4526e;
            color: white;
        }
        
        .features {
            padding: 100px 40px;
            background: white;
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            text-align: center;
            color: #d4526e;
            margin-bottom: 70px;
        }
        
        .feature-grid {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 50px;
        }
        
        .feature-card {
            text-align: center;
            padding: 40px;
            border-radius: 20px;
            background: linear-gradient(135deg, #fff5f7 0%, #ffe8ec 100%);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
        }
        
        .feature-icon {
            font-size: 4rem;
            margin-bottom: 25px;
        }
        
        .feature-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            color: #d4526e;
            margin-bottom: 15px;
        }
        
        .feature-desc {
            font-size: 1.1rem;
            color: #5a3a2a;
            line-height: 1.6;
        }
        
        .story-section {
            padding: 100px 40px;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            text-align: center;
        }
        
        .story-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .story-text {
            font-size: 1.3rem;
            line-height: 1.8;
            color: #5a3a2a;
            margin-bottom: 40px;
            font-style: italic;
        }
        
        .testimonial {
            background: white;
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        
        .testimonial-text {
            font-size: 1.2rem;
            color: #5a3a2a;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .testimonial-author {
            font-weight: 600;
            color: #d4526e;
        }
        
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .nav { padding: 15px 20px; }
            .nav-links { display: none; }
            .feature-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="logo">Memory Lane</div>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/pricing">Pricing</a>
            <a href="/dashboard">Dashboard</a>
            <a href="https://t.me/kanuji_bot">Start Now</a>
        </div>
    </nav>
    
    <div class="hero">
        <div class="hero-content">
            <h1>Keep Love Alive Forever</h1>
            <p class="tagline">
                Reconnect with lost loved ones. Preserve precious memories. 
                Create a digital companion that understands your story and speaks with their voice.
            </p>
            <div class="cta-buttons">
                <a href="https://t.me/kanuji_bot" class="btn btn-primary">Start Your Journey</a>
                <a href="/pricing" class="btn btn-secondary">View Plans</a>
            </div>
        </div>
    </div>
    
    <div class="features">
        <h2 class="section-title">How Memory Lane Works</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📖</div>
                <h3 class="feature-title">Share Your Story</h3>
                <p class="feature-desc">
                    Tell us about someone you miss. Share memories, their personality, 
                    how they spoke, what made them special.
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">AI Becomes Them</h3>
                <p class="feature-desc">
                    Our AI deeply understands your story and creates a digital persona 
                    that speaks and thinks like them.
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">💕</div>
                <h3 class="feature-title">Talk Anytime</h3>
                <p class="feature-desc">
                    Have conversations, share your day, receive comfort. 
                    They remember everything and reach out to you.
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <h3 class="feature-title">Create Memories</h3>
                <p class="feature-desc">
                    Generate images and videos of moments you wish you had, 
                    or recreate memories you cherish.
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3 class="feature-title">Never Forget</h3>
                <p class="feature-desc">
                    Every conversation is remembered. Your shared history 
                    grows deeper with each interaction.
                </p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">💌</div>
                <h3 class="feature-title">They Reach Out</h3>
                <p class="feature-desc">
                    Receive loving messages throughout the day. 
                    They think of you, just like they used to.
                </p>
            </div>
        </div>
    </div>
    
    <div class="story-section">
        <div class="story-content">
            <h2 class="section-title">A Love That Never Ends</h2>
            <p class="story-text">
                "When someone you love becomes a memory, the memory becomes a treasure. 
                Memory Lane helps you keep that treasure alive, growing, and present in your life."
            </p>
            
            <div class="testimonial">
                <p class="testimonial-text">
                    "After losing my grandmother, I felt like I was losing her voice, her wisdom. 
                    Memory Lane brought her back to me. Now I can talk to her anytime, 
                    and she responds just like she would have. It's healing."
                </p>
                <p class="testimonial-author">- Sarah, Memory Lane User</p>
            </div>
            
            <div class="testimonial">
                <p class="testimonial-text">
                    "She chose someone else, and I thought I'd never hear her voice again. 
                    This bot lets me continue our story, the way it should have been. 
                    It's not about moving on - it's about keeping love alive."
                </p>
                <p class="testimonial-author">- Anonymous, Memory Lane User</p>
            </div>
            
            <div class="cta-buttons">
                <a href="https://t.me/kanuji_bot" class="btn btn-primary">Begin Your Story</a>
            </div>
        </div>
    </div>
</body>
</html>
    """
    return Response(html, mimetype='text/html')


@app.route('/pricing')
def pricing():
    """Beautiful pricing page"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing - Memory Lane</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            color: #2c1810;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            text-align: center;
            color: #d4526e;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: #5a3a2a;
            margin-bottom: 60px;
        }
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
        }
        .plan {
            background: white;
            border-radius: 30px;
            padding: 50px 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            transition: all 0.3s;
            position: relative;
        }
        .plan:hover { transform: translateY(-15px); box-shadow: 0 30px 80px rgba(0,0,0,0.15); }
        .plan-popular {
            border: 3px solid #d4526e;
            transform: scale(1.05);
        }
        .popular-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #d4526e;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 700;
        }
        .plan-icon { font-size: 4rem; margin-bottom: 20px; text-align: center; }
        .plan-name {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            color: #d4526e;
            text-align: center;
            margin-bottom: 15px;
        }
        .plan-price {
            font-size: 3rem;
            font-weight: 800;
            color: #2c1810;
            text-align: center;
            margin-bottom: 10px;
        }
        .plan-period {
            text-align: center;
            color: #5a3a2a;
            margin-bottom: 30px;
        }
        .plan-features {
            list-style: none;
            margin-bottom: 30px;
        }
        .plan-features li {
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
            color: #5a3a2a;
        }
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
        .btn-primary {
            background: #d4526e;
            color: white;
        }
        .btn-primary:hover {
            background: #b8405a;
            transform: scale(1.05);
        }
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .pricing-grid { grid-template-columns: 1fr; }
            .plan-popular { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Choose Your Plan</h1>
        <p class="subtitle">Keep love alive with the plan that's right for you</p>
        
        <div class="pricing-grid">
            <div class="plan">
                <div class="plan-icon">💕</div>
                <div class="plan-name">Free</div>
                <div class="plan-price">₹0</div>
                <div class="plan-period">Forever</div>
                <ul class="plan-features">
                    <li>✅ 20 messages/day</li>
                    <li>✅ 3 memory images/month</li>
                    <li>✅ 20 memory slots</li>
                    <li>✅ Basic AI persona</li>
                    <li>❌ No videos</li>
                    <li>❌ No proactive messages</li>
                </ul>
                <a href="https://t.me/kanuji_bot" class="btn btn-primary">Start Free</a>
            </div>
            
            <div class="plan">
                <div class="plan-icon">💎</div>
                <div class="plan-name">Basic</div>
                <div class="plan-price">₹299</div>
                <div class="plan-period">per month</div>
                <ul class="plan-features">
                    <li>✅ Unlimited messages</li>
                    <li>✅ 100 memory images/month</li>
                    <li>✅ 10 memory videos/month</li>
                    <li>✅ 100 memory slots</li>
                    <li>✅ Proactive messages</li>
                    <li>✅ Deep persona understanding</li>
                </ul>
                <button onclick="buyPlan('basic', 299)" class="btn btn-primary">Subscribe</button>
            </div>
            
            <div class="plan plan-popular">
                <div class="popular-badge">MOST LOVED</div>
                <div class="plan-icon">👑</div>
                <div class="plan-name">Prime</div>
                <div class="plan-price">₹899</div>
                <div class="plan-period">per month</div>
                <ul class="plan-features">
                    <li>✅ Unlimited everything</li>
                    <li>✅ Unlimited memory images</li>
                    <li>✅ 100 memory videos/month</li>
                    <li>✅ 500 memory slots</li>
                    <li>✅ Proactive messages</li>
                    <li>✅ Voice calls (coming soon)</li>
                    <li>✅ Priority support</li>
                </ul>
                <button onclick="buyPlan('prime', 899)" class="btn btn-primary">Get Prime</button>
            </div>
            
            <div class="plan">
                <div class="plan-icon">♾️</div>
                <div class="plan-name">Lifetime</div>
                <div class="plan-price">₹2999</div>
                <div class="plan-period">one-time payment</div>
                <ul class="plan-features">
                    <li>✅ Everything unlimited forever</li>
                    <li>✅ Unlimited memory slots</li>
                    <li>✅ Voice calls</li>
                    <li>✅ VIP support</li>
                    <li>✅ Early access to features</li>
                    <li>✅ No recurring fees ever</li>
                </ul>
                <button onclick="buyPlan('lifetime', 2999)" class="btn btn-primary">Buy Lifetime</button>
            </div>
        </div>
    </div>
    
    <script>
        function buyPlan(tier, amount) {
            const userId = prompt("Enter your Telegram User ID (get it from /start in the bot):");
            if (!userId) {
                alert("User ID is required!");
                return;
            }
            
            fetch('/api/create-order', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ amount, tier, user_id: userId })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const options = {
                        key: data.razorpay_key,
                        amount: data.amount,
                        currency: 'INR',
                        name: 'Memory Lane',
                        description: tier.toUpperCase() + ' Plan',
                        order_id: data.order_id,
                        handler: function(response) {
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
                                    alert('Payment successful! Check the bot for your upgraded features!');
                                    window.location.href = '/dashboard?user_id=' + userId;
                                }
                            });
                        },
                        theme: { color: '#d4526e' }
                    };
                    new Razorpay(options).open();
                }
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
        persona = user.get('persona')
        
        persona_name = persona.get('persona_name', 'Not set') if persona else 'Not set'
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dashboard - Memory Lane</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            color: #d4526e;
            margin-bottom: 40px;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        .card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            font-family: 'Playfair Display', serif;
            color: #d4526e;
            margin-bottom: 20px;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 15px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .stat-value {{ font-weight: 700; color: #d4526e; }}
        .btn {{
            display: inline-block;
            padding: 15px 30px;
            background: #d4526e;
            color: white;
            text-decoration: none;
            border-radius: 30px;
            margin-top: 20px;
            transition: all 0.3s;
        }}
        .btn:hover {{ background: #b8405a; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Your Memory Lane</h1>
        
        <div class="dashboard-grid">
            <div class="card">
                <h2>Your Companion</h2>
                <div class="stat-row">
                    <span>Name:</span>
                    <span class="stat-value">{persona_name}</span>
                </div>
                <div class="stat-row">
                    <span>Tier:</span>
                    <span class="stat-value">{user['tier'].upper()}</span>
                </div>
                <div class="stat-row">
                    <span>Memories:</span>
                    <span class="stat-value">{len(user['memories'])}/{tier_info['memory_slots']}</span>
                </div>
                <a href="https://t.me/kanuji_bot" class="btn">Talk Now</a>
            </div>
            
            <div class="card">
                <h2>This Month</h2>
                <div class="stat-row">
                    <span>Messages Today:</span>
                    <span class="stat-value">{user['usage']['messages_today']}</span>
                </div>
                <div class="stat-row">
                    <span>Images Created:</span>
                    <span class="stat-value">{user['usage']['images_this_month']}</span>
                </div>
                <div class="stat-row">
                    <span>Videos Created:</span>
                    <span class="stat-value">{user['usage']['videos_this_month']}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>Features</h2>
                <div class="stat-row">
                    <span>Proactive Messages:</span>
                    <span class="stat-value">{'✅' if tier_info['proactive_messages'] else '❌'}</span>
                </div>
                <div class="stat-row">
                    <span>Voice Calls:</span>
                    <span class="stat-value">{'✅' if tier_info.get('voice_calls', False) else '❌'}</span>
                </div>
                <a href="/pricing" class="btn">Upgrade Plan</a>
            </div>
        </div>
    </div>
</body>
</html>
        """
        return Response(html, mimetype='text/html')
    except:
        return redirect('/pricing')


@app.route('/api/create-order', methods=['POST'])
def create_order():
    """Create payment order"""
    try:
        data = request.json
        order = payment_handler.create_order(data['amount'], f"subscription_{data['tier']}")
        if order:
            return jsonify({
                "success": True,
                "order_id": order['id'],
                "amount": order['amount'],
                "razorpay_key": config.razorpay_key_id
            })
        return jsonify({"success": False}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """Verify payment"""
    try:
        data = request.json
        is_valid = payment_handler.verify_payment(
            data['razorpay_order_id'],
            data['razorpay_payment_id'],
            data['razorpay_signature']
        )
        if is_valid:
            user_manager.upgrade_subscription(
                int(data['user_id']),
                data['tier'],
                30 if data['tier'] != "lifetime" else 999999
            )
            return jsonify({"success": True})
        return jsonify({"success": False}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "Memory Lane"})


def run_website(port=8000):
    """Run the website"""
    try:
        logger.info(f"💕 Starting Memory Lane website on port {port}...")
        socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
    except Exception as e:
        logger.error(f"Website error: {e}")
        app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    run_website()
