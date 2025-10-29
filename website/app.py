"""
Flask Website - Complete with Templates and Payment
"""

from flask import Flask, render_template, request, jsonify, redirect
from flask_socketio import SocketIO, emit
from src.core.config import get_config
from src.core.user_manager import get_user_manager
from src.payment.razorpay import get_payment_handler
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
config = get_config()
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')


@app.route('/payment')
def payment_page():
    """Payment page"""
    order_id = request.args.get('order_id')
    user_id = request.args.get('user_id')
    tier = request.args.get('tier')
    
    if not all([order_id, user_id, tier]):
        return "Invalid payment link", 400
    
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


@app.route('/api/payment/verify', methods=['POST'])
def verify_payment():
    """Verify payment and upgrade user"""
    try:
        data = request.json
        payment_handler = get_payment_handler()
        user_manager = get_user_manager()
        
        # Verify payment
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
