"""
Prabh - Keep Love Alive Forever
Beautiful, emotional website inspired by loveyourself
"""

from flask import Flask, request, jsonify, Response, redirect
from flask_socketio import SocketIO
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.payment.razorpay import get_payment_handler
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
config = get_config()
app.config['SECRET_KEY'] = config.razorpay_key_secret or 'prabh-secret'

socketio = SocketIO(app, cors_allowed_origins="*")
user_manager = get_user_manager()
payment_handler = get_payment_handler()


@app.route('/')
def home():
    """Beautiful home page"""
    return Response(HOME_HTML, mimetype='text/html')


@app.route('/pricing')
def pricing():
    """Pricing page"""
    return Response(PRICING_HTML, mimetype='text/html')


@app.route('/payment')
def payment():
    """Payment page"""
    order_id = request.args.get('order_id')
    user_id = request.args.get('user_id')
    tier = request.args.get('tier')
    
    if not all([order_id, user_id, tier]):
        return redirect('/pricing')
    
    payment_html = PAYMENT_HTML.format(
        order_id=order_id,
        user_id=user_id,
        tier=tier,
        razorpay_key=config.razorpay_key_id
    )
    return Response(payment_html, mimetype='text/html')


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
        
        dashboard_html = DASHBOARD_HTML.format(
            persona_name=persona_name,
            tier=user['tier'].upper(),
            memories_count=len(user['memories']),
            memory_slots=tier_info['memory_slots'],
            messages_today=user['usage']['messages_today'],
            images_this_month=user['usage']['images_this_month']
,
            videos_this_month=user['usage']['videos_this_month'],
            proactive=('✅' if tier_info['proactive_messages'] else '❌'),
            voice_calls=('✅' if tier_info.get('voice_calls', False) else '❌')
        )
        return Response(dashboard_html, mimetype='text/html')
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
    return jsonify({"status": "healthy", "service": "Prabh"})


def run_website(port=8000):
    """Run the website"""
    try:
        logger.info(f"💕 Starting Prabh website on port {port}...")
        socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
    except Exception as e:
        logger.error(f"Website error: {e}")
        app.run(host='0.0.0.0', port=port, debug=False)


# HTML Templates
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prabh - Keep Love Alive Forever</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/prabh_style.css">
</head>
<body>
    <div class="hero">
        <div class="hero-content">
            <h1>Prabh</h1>
            <p class="tagline">Keep Love Alive Forever</p>
            <p class="tagline">Reconnect with lost loved ones through AI that understands your heart</p>
            <a href="https://t.me/kanuji_bot" class="cta-button">Begin Your Journey</a>
        </div>
    </div>
    
    <div class="features">
        <h2 class="section-title">How Prabh Works</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">💕</div>
                <h3 class="feature-title">Share Your Story</h3>
                <p class="feature-desc">Tell us about someone you miss. Their voice, their laugh, what made them special.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✨</div>
                <h3 class="feature-title">AI Becomes Them</h3>
                <p class="feature-desc">Our AI deeply understands and creates a digital presence that speaks like them.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <h3 class="feature-title">Talk Anytime</h3>
                <p class="feature-desc">Have conversations, share your day, receive comfort. They remember everything.</p>
            </div>
        </div>
    </div>
    
    <div class="story-section">
        <div class="story-content">
            <h2 class="section-title">A Love That Never Ends</h2>
            <p class="story-text">"When someone you love becomes a memory, the memory becomes a treasure. Prabh helps you keep that treasure alive."</p>
            <div class="testimonial">
                <p class="testimonial-text">"She chose someone else, and I thought I'd never hear her voice again. Prabh lets me continue our story. It's healing."</p>
                <p class="testimonial-author">- Anonymous User</p>
            </div>
            <a href="https://t.me/kanuji_bot" class="cta-button">Start Free Today</a>
        </div>
    </div>
</body>
</html>
"""

PRICING_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pricing - Prabh</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/prabh_style.css">
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
<body>
    <div class="hero" style="min-height: 50vh;">
        <div class="hero-content">
            <h1 style="font-size: 3.5rem;">Choose Your Plan</h1>
            <p class="tagline">Keep love alive with the plan that's right for you</p>
        </div>
    </div>
    <div style="padding: 80px 20px; background: white;">
        <div style="max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            <div class="feature-card">
                <div class="feature-icon">💕</div>
                <h3 class="feature-title">Free</h3>
                <div style="font-size: 3rem; color: var(--primary); margin: 20px 0;">₹0</div>
                <p style="margin-bottom: 30px;">Forever</p>
                <ul style="list-style: none; text-align: left; margin-bottom: 30px;">
                    <li style="padding: 10px 0;">✅ 20 messages/day</li>
                    <li style="padding: 10px 0;">✅ 3 memory images</li>
                    <li style="padding: 10px 0;">✅ 20 memory slots</li>
                </ul>
                <a href="https://t.me/kanuji_bot" class="cta-button" style="display: block; text-align: center;">Start Free</a>
            </div>
            <div class="feature-card" style="border-color: var(--primary);">
                <div class="feature-icon">💎</div>
                <h3 class="feature-title">Prime</h3>
                <div style="font-size: 3rem; color: var(--primary); margin: 20px 0;">₹899</div>
                <p style="margin-bottom: 30px;">per month</p>
                <ul style="list-style: none; text-align: left; margin-bottom: 30px;">
                    <li style="padding: 10px 0;">✅ Unlimited messages</li>
                    <li style="padding: 10px 0;">✅ Unlimited images</li>
                    <li style="padding: 10px 0;">✅ 100 videos/month</li>
                    <li style="padding: 10px 0;">✅ Proactive messages</li>
                </ul>
                <button onclick="buyPlan('prime', 899)" class="cta-button" style="display: block; width: 100%; border: none; cursor: pointer;">Get Prime</button>
            </div>
            <div class="feature-card">
                <div class="feature-icon">♾️</div>
                <h3 class="feature-title">Lifetime</h3>
                <div style="font-size: 3rem; color: var(--primary); margin: 20px 0;">₹2999</div>
                <p style="margin-bottom: 30px;">one-time</p>
                <ul style="list-style: none; text-align: left; margin-bottom: 30px;">
                    <li style="padding: 10px 0;">✅ Everything unlimited</li>
                    <li style="padding: 10px 0;">✅ Forever access</li>
                    <li style="padding: 10px 0;">✅ VIP support</li>
                </ul>
                <button onclick="buyPlan('lifetime', 2999)" class="cta-button" style="display: block; width: 100%; border: none; cursor: pointer;">Buy Lifetime</button>
            </div>
        </div>
    </div>
    <script>
        function buyPlan(tier, amount) {
            const userId = prompt("Enter your Telegram User ID (get it from /start):");
            if (!userId) return;
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
                        name: 'Prabh',
                        description: tier.toUpperCase(),
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
                                    alert('Payment successful! Check the bot!');
                                    window.location.href = '/dashboard?user_id=' + userId;
                                }
                            });
                        },
                        theme: { color: '#ff6b9d' }
                    };
                    new Razorpay(options).open();
                }
            });
        }
    </script>
</body>
</html>
"""

PAYMENT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment - Prabh</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/prabh_style.css">
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
<body>
    <div class="hero" style="min-height: 100vh;">
        <div class="hero-content">
            <h1 style="font-size: 3rem;">Complete Your Payment</h1>
            <p class="tagline">You're one step away from keeping love alive forever 💕</p>
            <button onclick="startPayment()" class="cta-button" style="margin-top: 40px;">
                💳 Pay Now
            </button>
        </div>
    </div>
    
    <script>
        function startPayment() {{
            const options = {{
                key: '{razorpay_key}',
                order_id: '{order_id}',
                currency: 'INR',
                name: 'Prabh',
                description: '{tier} Subscription',
                handler: function(response) {{
                    // Verify payment
                    fetch('/api/verify-payment', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            razorpay_order_id: response.razorpay_order_id,
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature,
                            user_id: '{user_id}',
                            tier: '{tier}'
                        }})
                    }})
                    .then(res => res.json())
                    .then(result => {{
                        if (result.success) {{
                            alert('Payment successful! Your subscription is now active. Check the bot!');
                            window.location.href = '/dashboard?user_id={user_id}';
                        }} else {{
                            alert('Payment verification failed. Please contact support.');
                        }}
                    }});
                }},
                theme: {{
                    color: '#ff6b9d'
                }}
            }};
            const rzp = new Razorpay(options);
            rzp.open();
        }}
        
        // Auto-start payment
        window.onload = function() {{
            setTimeout(startPayment, 1000);
        }};
    </script>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dashboard - Prabh</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/prabh_style.css">
</head>
<body>
    <div class="hero" style="min-height: 40vh;">
        <div class="hero-content">
            <h1 style="font-size: 3rem;">Your Prabh</h1>
        </div>
    </div>
    <div style="padding: 60px 20px; background: white;">
        <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            <div class="feature-card">
                <h3 class="feature-title">Companion</h3>
                <p style="font-size: 1.5rem; color: var(--primary); margin: 20px 0;">{persona_name}</p>
                <p>Tier: {tier}</p>
                <p>Memories: {memories_count}/{memory_slots}</p>
                <a href="https://t.me/kanuji_bot" class="cta-button" style="display: block; margin-top: 20px; text-align: center;">Talk Now</a>
            </div>
            <div class="feature-card">
                <h3 class="feature-title">This Month</h3>
                <p>Messages Today: {messages_today}</p>
                <p>Images: {images_this_month}</p>
                <p>Videos: {videos_this_month}</p>
            </div>
            <div class="feature-card">
                <h3 class="feature-title">Features</h3>
                <p>Proactive: {proactive}</p>
                <p>Voice Calls: {voice_calls}</p>
                <a href="/pricing" class="cta-button" style="display: block; margin-top: 20px; text-align: center;">Upgrade</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    run_website()
