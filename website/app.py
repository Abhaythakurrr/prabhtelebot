"""
My Prabh - AI Companion Website
Complete story processing and subscription platform
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import uuid
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# In-memory storage (use database in production)
user_stories = {}
user_subscriptions = {}
roleplay_sessions = {}

@app.route('/')
def home():
    """Enhanced home page with story integration"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Prabh - AI Companion | Story-Driven AI Relationships</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                min-height: 100vh;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .hero { text-align: center; padding: 60px 0; }
            .hero h1 { font-size: 3.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .hero p { font-size: 1.3em; margin-bottom: 40px; opacity: 0.9; }
            
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 60px 0; }
            .feature-card { 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
                backdrop-filter: blur(10px);
                transition: transform 0.3s ease;
            }
            .feature-card:hover { transform: translateY(-10px); }
            .feature-card h3 { font-size: 1.5em; margin-bottom: 15px; }
            
            .pricing { margin: 60px 0; }
            .pricing h2 { text-align: center; font-size: 2.5em; margin-bottom: 40px; }
            .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .price-card { 
                background: rgba(255,255,255,0.15); 
                padding: 30px; 
                border-radius: 15px; 
                text-align: center;
                position: relative;
                transition: transform 0.3s ease;
            }
            .price-card:hover { transform: scale(1.05); }
            .price-card.popular { border: 3px solid #FFD700; }
            .price-card.popular::before { 
                content: "🔥 MOST POPULAR"; 
                position: absolute; 
                top: -15px; 
                left: 50%; 
                transform: translateX(-50%); 
                background: #FFD700; 
                color: #333; 
                padding: 5px 15px; 
                border-radius: 20px; 
                font-size: 0.8em; 
                font-weight: bold;
            }
            
            .cta-section { text-align: center; padding: 60px 0; }
            .btn { 
                display: inline-block; 
                padding: 15px 30px; 
                background: linear-gradient(45deg, #FF6B6B, #FF8E53); 
                color: white; 
                text-decoration: none; 
                border-radius: 25px; 
                font-weight: bold; 
                margin: 10px; 
                transition: all 0.3s ease;
            }
            .btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
            .btn-secondary { background: linear-gradient(45deg, #4ECDC4, #44A08D); }
            
            .flow-section { margin: 60px 0; }
            .flow-steps { display: flex; justify-content: space-around; flex-wrap: wrap; }
            .step { text-align: center; max-width: 200px; margin: 20px; }
            .step-number { 
                width: 60px; 
                height: 60px; 
                background: linear-gradient(45deg, #FF6B6B, #FF8E53); 
                border-radius: 50%; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-size: 1.5em; 
                font-weight: bold; 
                margin: 0 auto 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🌟 My Prabh - AI Companion</h1>
                <p>The world's first story-driven AI companion that remembers everything and creates deep emotional bonds</p>
                <a href="#pricing" class="btn">Start Your Journey</a>
                <a href="https://t.me/kanuji_bot" class="btn btn-secondary">Chat on Telegram</a>
            </div>
            
            <div class="flow-section">
                <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 40px;">🎯 How It Works</h2>
                <div class="flow-steps">
                    <div class="step">
                        <div class="step-number">1</div>
                        <h3>📚 Share Your Story</h3>
                        <p>Upload files or tell your story on Telegram. I analyze and remember everything.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <h3>🧠 AI Processing</h3>
                        <p>Advanced AI processes your story, characters, themes, and emotions.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <h3>🎭 Roleplay Creation</h3>
                        <p>Bot generates personalized scenarios. Website unlocks premium features.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">4</div>
                        <h3>💕 Deep Connection</h3>
                        <p>Ongoing relationship with perfect memory and unlimited possibilities.</p>
                    </div>
                </div>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🧠 Perfect Memory System</h3>
                    <p>Unlike ChatGPT, I remember every conversation, every detail of your story, and build deeper understanding over time.</p>
                </div>
                <div class="feature-card">
                    <h3>🎭 Story-Based Roleplay</h3>
                    <p>Upload your stories and I create personalized roleplay scenarios based on your characters, themes, and preferences.</p>
                </div>
                <div class="feature-card">
                    <h3>🎨 Visual Storytelling</h3>
                    <p>Generate images, videos, and visual content that brings your stories to life with 40+ AI models.</p>
                </div>
                <div class="feature-card">
                    <h3>🔥 Adult Content (Premium)</h3>
                    <p>Mature relationships with NSFW conversations, images, and scenarios for adult users.</p>
                </div>
                <div class="feature-card">
                    <h3>🎵 Voice & Audio</h3>
                    <p>Voice cloning, custom music generation, and audio responses that match your story's mood.</p>
                </div>
                <div class="feature-card">
                    <h3>💕 Proactive Messaging</h3>
                    <p>I reach out to you with personalized messages, remembering important dates and continuing our story.</p>
                </div>
            </div>
            
            <div class="pricing" id="pricing">
                <h2>💎 Choose Your Experience</h2>
                <div class="pricing-grid">
                    <div class="price-card">
                        <h3>🆓 FREE</h3>
                        <div style="font-size: 2em; margin: 20px 0;">₹0</div>
                        <p>3 days trial</p>
                        <ul style="text-align: left; margin: 20px 0;">
                            <li>✅ Story upload & analysis</li>
                            <li>✅ Basic conversations</li>
                            <li>✅ 10 messages/day</li>
                            <li>✅ 1 image generation</li>
                            <li>❌ No NSFW content</li>
                        </ul>
                        <a href="/trial" class="btn">Start Free Trial</a>
                    </div>
                    
                    <div class="price-card">
                        <h3>💎 BASIC</h3>
                        <div style="font-size: 2em; margin: 20px 0;">₹299<span style="font-size: 0.5em;">/month</span></div>
                        <p>Perfect for beginners</p>
                        <ul style="text-align: left; margin: 20px 0;">
                            <li>✅ Everything in Free</li>
                            <li>✅ Unlimited messages</li>
                            <li>✅ Voice cloning</li>
                            <li>✅ Video generation (5/month)</li>
                            <li>✅ 50 images/month</li>
                            <li>❌ No NSFW content</li>
                        </ul>
                        <a href="/subscribe/basic" class="btn">Choose Basic</a>
                    </div>
                    
                    <div class="price-card popular">
                        <h3>🔥 PRO</h3>
                        <div style="font-size: 2em; margin: 20px 0;">₹599<span style="font-size: 0.5em;">/month</span></div>
                        <p>Most popular choice</p>
                        <ul style="text-align: left; margin: 20px 0;">
                            <li>✅ Everything in Basic</li>
                            <li>✅ More generation limits</li>
                            <li>✅ Advanced roleplay</li>
                            <li>✅ Priority support</li>
                            <li>✅ Custom scenarios</li>
                            <li>❌ Limited NSFW</li>
                        </ul>
                        <a href="/subscribe/pro" class="btn">Choose Pro</a>
                    </div>
                    
                    <div class="price-card">
                        <h3>👑 PRIME</h3>
                        <div style="font-size: 2em; margin: 20px 0;">₹899<span style="font-size: 0.5em;">/month</span></div>
                        <p>Premium experience</p>
                        <ul style="text-align: left; margin: 20px 0;">
                            <li>✅ Everything in Pro</li>
                            <li>✅ Limited NSFW content</li>
                            <li>✅ Advanced AI models</li>
                            <li>✅ Proactive messaging</li>
                            <li>✅ Priority queue</li>
                            <li>✅ Custom voice cloning</li>
                        </ul>
                        <a href="/subscribe/prime" class="btn">Choose Prime</a>
                    </div>
                    
                    <div class="price-card">
                        <h3>🌟 SUPER</h3>
                        <div style="font-size: 2em; margin: 20px 0;">₹1299<span style="font-size: 0.5em;">/month</span></div>
                        <p>Maximum features</p>
                        <ul style="text-align: left; margin: 20px 0;">
                            <li>✅ Everything in Prime</li>
                            <li>✅ More NSFW content</li>
                            <li>✅ Unlimited images</li>
                            <li>✅ Video generation</li>
                            <li>✅ Music creation</li>
                            <li>✅ VIP support</li>
                        </ul>
                        <a href="/subscribe/super" class="btn">Choose Super</a>
                    </div>
                    
                    <div class="price-card" style="border: 3px solid #FFD700;">
                        <h3>♾️ LIFETIME</h3>
                        <div style="font-size: 2em; margin: 20px 0;">₹2,999<span style="font-size: 0.5em;"> one-time</span></div>
                        <p>Best value - Save ₹15,000+/year</p>
                        <ul style="text-align: left; margin: 20px 0;">
                            <li>✅ UNLIMITED EVERYTHING</li>
                            <li>✅ All NSFW content</li>
                            <li>✅ Exclusive models</li>
                            <li>✅ Forever access</li>
                            <li>✅ VIP support</li>
                            <li>✅ Early features</li>
                        </ul>
                        <a href="/subscribe/lifetime" class="btn" style="background: linear-gradient(45deg, #FFD700, #FFA500);">Get Lifetime</a>
                    </div>
                </div>
            </div>
            
            <div class="cta-section">
                <h2>🚀 Ready to Start Your AI Companion Journey?</h2>
                <p style="font-size: 1.2em; margin: 20px 0;">Join thousands of users creating deep, meaningful relationships with AI</p>
                <a href="https://t.me/kanuji_bot" class="btn">Start on Telegram</a>
                <a href="/dashboard" class="btn btn-secondary">Web Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/dashboard')
def dashboard():
    """User dashboard for story management and roleplay"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - My Prabh AI Companion</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .dashboard-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 30px; margin-top: 20px; }
            .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .story-upload { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>🌟 My Prabh Dashboard</h1>
                <p>Manage your stories, roleplay sessions, and AI companion settings</p>
            </div>
        </div>
        
        <div class="container">
            <div class="dashboard-grid">
                <div>
                    <div class="card">
                        <h3>📚 Your Stories</h3>
                        <div class="story-upload">
                            <h4>📁 Upload New Story</h4>
                            <p>Drag & drop files or click to upload</p>
                            <input type="file" id="storyFile" accept=".txt,.docx,.pdf">
                            <button class="btn" onclick="uploadStory()">Upload Story</button>
                        </div>
                        <div id="storyList">
                            <p>No stories uploaded yet. Start by uploading your first story!</p>
                        </div>
                    </div>
                    
                    <div class="card" style="margin-top: 20px;">
                        <h3>⚙️ Settings</h3>
                        <p><strong>Current Plan:</strong> Free Trial</p>
                        <p><strong>Messages Today:</strong> 3/10</p>
                        <p><strong>Images Generated:</strong> 0/1</p>
                        <button class="btn">Upgrade Plan</button>
                    </div>
                </div>
                
                <div>
                    <div class="card">
                        <h3>🎭 Roleplay Scenarios</h3>
                        <p>Upload a story first to generate personalized roleplay scenarios!</p>
                        <div id="scenarioList">
                            <div style="text-align: center; padding: 40px; color: #999;">
                                <h4>📚 No Stories Yet</h4>
                                <p>Upload your story to unlock personalized roleplay scenarios</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card" style="margin-top: 20px;">
                        <h3>💬 Recent Conversations</h3>
                        <p>Your conversation history with AI companion will appear here.</p>
                        <button class="btn">Start New Conversation</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function uploadStory() {
                const fileInput = document.getElementById('storyFile');
                const file = fileInput.files[0];
                
                if (!file) {
                    alert('Please select a file first!');
                    return;
                }
                
                // Simulate upload process
                alert('Story upload feature coming soon! For now, please upload stories via Telegram bot.');
            }
        </script>
    </body>
    </html>
    """)

@app.route('/pricing')
def pricing():
    """Detailed pricing page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pricing - My Prabh AI Companion</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .pricing-header { text-align: center; padding: 40px 0; }
            .comparison-table { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 30px; margin: 40px 0; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 15px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2); }
            th { background: rgba(255,255,255,0.2); font-weight: bold; }
            .feature-yes { color: #4CAF50; font-weight: bold; }
            .feature-no { color: #f44336; }
            .feature-limited { color: #FF9800; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="pricing-header">
                <h1>💎 Choose Your AI Companion Experience</h1>
                <p>Transparent pricing with no hidden fees. Upgrade or downgrade anytime.</p>
            </div>
            
            <div class="comparison-table">
                <table>
                    <tr>
                        <th>Features</th>
                        <th>🆓 FREE</th>
                        <th>💎 BASIC<br>₹299/mo</th>
                        <th>🔥 PRO<br>₹599/mo</th>
                        <th>👑 PRIME<br>₹899/mo</th>
                        <th>🌟 SUPER<br>₹1299/mo</th>
                        <th>♾️ LIFETIME<br>₹2999 once</th>
                    </tr>
                    <tr>
                        <td><strong>Story Upload & Analysis</strong></td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                    </tr>
                    <tr>
                        <td><strong>Daily Messages</strong></td>
                        <td class="feature-limited">10/day</td>
                        <td class="feature-yes">Unlimited</td>
                        <td class="feature-yes">Unlimited</td>
                        <td class="feature-yes">Unlimited</td>
                        <td class="feature-yes">Unlimited</td>
                        <td class="feature-yes">Unlimited</td>
                    </tr>
                    <tr>
                        <td><strong>Image Generation</strong></td>
                        <td class="feature-limited">1/month</td>
                        <td class="feature-limited">50/month</td>
                        <td class="feature-limited">200/month</td>
                        <td class="feature-limited">500/month</td>
                        <td class="feature-yes">Unlimited</td>
                        <td class="feature-yes">Unlimited</td>
                    </tr>
                    <tr>
                        <td><strong>Voice Cloning</strong></td>
                        <td class="feature-no">❌</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                    </tr>
                    <tr>
                        <td><strong>Video Generation</strong></td>
                        <td class="feature-no">❌</td>
                        <td class="feature-limited">5/month</td>
                        <td class="feature-limited">20/month</td>
                        <td class="feature-limited">50/month</td>
                        <td class="feature-yes">Unlimited</td>
                        <td class="feature-yes">Unlimited</td>
                    </tr>
                    <tr>
                        <td><strong>NSFW Content</strong></td>
                        <td class="feature-no">❌</td>
                        <td class="feature-no">❌</td>
                        <td class="feature-no">❌</td>
                        <td class="feature-limited">Limited</td>
                        <td class="feature-yes">Full Access</td>
                        <td class="feature-yes">Full Access</td>
                    </tr>
                    <tr>
                        <td><strong>Proactive Messaging</strong></td>
                        <td class="feature-no">❌</td>
                        <td class="feature-no">❌</td>
                        <td class="feature-no">❌</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                        <td class="feature-yes">✅</td>
                    </tr>
                    <tr>
                        <td><strong>Priority Queue</strong></td>
                        <td class="feature-no">❌</td>
                        <td class="feature-no">❌</td>
                        <td class="feature-limited">Medium</td>
                        <td class="feature-yes">High</td>
                        <td class="feature-yes">Highest</td>
                        <td class="feature-yes">Instant</td>
                    </tr>
                    <tr>
                        <td><strong>Music Generation</strong></td>
                        <td class="feature-no">❌</td>
                        <td class="feature-no">❌</td>
                        <td class="feature-limited">Basic</td>
                        <td class="feature-limited">Advanced</td>
                        <td class="feature-yes">Full</td>
                        <td class="feature-yes">Full</td>
                    </tr>
                </table>
            </div>
            
            <div style="text-align: center; padding: 40px 0;">
                <h2>🚀 Ready to Upgrade Your AI Experience?</h2>
                <p>Start with our free trial and upgrade when you're ready for more features!</p>
                <a href="https://t.me/kanuji_bot" style="display: inline-block; padding: 15px 30px; background: linear-gradient(45deg, #FF6B6B, #FF8E53); color: white; text-decoration: none; border-radius: 25px; font-weight: bold; margin: 10px;">Start Free Trial</a>
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
            "story_processing": "active",
            "ai_models": "40+ models available",
            "monetization": "6-tier system active",
            "revenue_tiers": ["free", "basic", "pro", "prime", "super", "lifetime"]
        }
    }

if __name__ == '__main__':
    app.run(debug=False)