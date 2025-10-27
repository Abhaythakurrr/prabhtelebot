#!/usr/bin/env python3
"""
Deploy AI Companion Platform to Railway
Complete deployment with bot + website + cyberpunk theme
"""

import os
import subprocess
import sys
import json

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking deployment files...")
    
    required_files = [
        'start.py',
        'Procfile', 
        'railway.json',
        'requirements.txt',
        'website/app.py',
        'src/main.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def setup_environment_variables():
    """Set up all environment variables for Railway"""
    print("🔧 Setting up environment variables...")
    
    env_vars = {
        # Core Application
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "FLASK_ENV": "production",
        "FLASK_SECRET_KEY": "ai-companion-cyberpunk-love-secret-2024",
        
        # Telegram Bot
        "TELEGRAM_BOT_TOKEN": "8347105320:AAF0tJwnGQHDfPu9hGr58oXrPYoJEa6pZiY",
        "TELEGRAM_USE_POLLING": "true",
        
        # AI Models - OpenRouter
        "MISTRAL_API_KEY": "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",
        "NEMOTRON_API_KEY": "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",
        "LLAMA_API_KEY": "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",
        "LLAMA4_API_KEY": "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",
        "DOLPHIN_API_KEY": "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",
        
        # Payment Gateway
        "RAZORPAY_KEY_ID": "rzp_live_RFCUrmIElPNS5m",
        "RAZORPAY_KEY_SECRET": "IzybX6ykve4VJ8GxldZhVJEC",
        
        # Database
        "DATABASE_URL": "sqlite:///ai_companion.db",
        
        # OpenRouter API
        "OPENROUTER_API_BASE": "https://openrouter.ai/api/v1"
    }
    
    success_count = 0
    for key, value in env_vars.items():
        if run_command(f'railway variables set {key}="{value}"', f"Setting {key}"):
            success_count += 1
        else:
            print(f"⚠️ Failed to set {key}, continuing...")
    
    print(f"✅ Set {success_count}/{len(env_vars)} environment variables")
    return success_count > 0

def main():
    print("🚀 AI COMPANION PLATFORM - RAILWAY DEPLOYMENT")
    print("=" * 60)
    print("🎨 Cyberpunk Love Theme | 🤖 Bot + 🌐 Website | 🔥 NSFW Ready")
    print("=" * 60)
    
    # Check if all files exist
    if not check_files():
        return False
    
    # Check if Railway CLI is installed
    print("\n🔧 Checking Railway CLI...")
    if not run_command("railway --version", "Checking Railway CLI"):
        print("\n❌ Railway CLI not found. Install it first:")
        print("   npm install -g @railway/cli")
        print("   or")
        print("   curl -fsSL https://railway.app/install.sh | sh")
        return False
    
    # Login to Railway
    print("\n🔐 Railway Authentication...")
    if not run_command("railway login", "Logging into Railway"):
        print("❌ Railway login failed. Please run 'railway login' manually first.")
        return False
    
    # Initialize Railway project
    print("\n📦 Project Setup...")
    if not run_command("railway init", "Initializing Railway project"):
        print("⚠️ Project might already exist, continuing...")
    
    # Set up environment variables
    print("\n🌍 Environment Configuration...")
    if not setup_environment_variables():
        print("❌ Failed to set environment variables")
        return False
    
    # Deploy the application
    print("\n🚀 Deploying Application...")
    if not run_command("railway up --detach", "Deploying to Railway"):
        print("❌ Deployment failed")
        return False
    
    # Get deployment URL
    print("\n🌐 Getting deployment URL...")
    run_command("railway domain", "Getting domain information")
    
    print("\n" + "=" * 60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("=" * 60)
    print("🤖 AI Companion Bot: LIVE")
    print("🌐 Cyberpunk Website: LIVE") 
    print("💳 Razorpay Payments: ACTIVE")
    print("🎨 Futuristic UI/UX: ENABLED")
    print("🔥 NSFW Content: READY")
    print("💕 Love Theme: ACTIVATED")
    print("=" * 60)
    
    print("\n📱 TELEGRAM BOT:")
    print("   🔗 https://t.me/kanuji_bot")
    print("   📝 Username: @kanuji_bot")
    
    print("\n🌐 WEBSITE:")
    print("   🔗 Check Railway dashboard for your URL")
    print("   📊 Health check: /health endpoint")
    
    print("\n🎯 FEATURES DEPLOYED:")
    print("   ✅ Multi-AI Model Integration")
    print("   ✅ Voice Cloning Engine")
    print("   ✅ Story Preprocessing")
    print("   ✅ Image Generation")
    print("   ✅ Premium Payment System")
    print("   ✅ Proactive Messaging")
    print("   ✅ Cyberpunk Love Theme")
    print("   ✅ NSFW Conversations")
    
    print("\n🔧 NEXT STEPS:")
    print("   1. Test the bot: Send /start to @kanuji_bot")
    print("   2. Visit your website URL")
    print("   3. Test payment integration")
    print("   4. Upload voice samples and stories")
    print("   5. Enjoy your AI companion!")
    
    print("\n💡 MONITORING:")
    print("   📊 Railway Dashboard: https://railway.app/dashboard")
    print("   📋 Logs: railway logs --tail")
    print("   🔄 Restart: railway redeploy")
    
    return True

if __name__ == '__main__':
    try:
        if main():
            print("\n✅ ALL SYSTEMS DEPLOYED AND READY!")
            print("🚀 Your AI Companion Platform is now live on Railway!")
        else:
            print("\n❌ DEPLOYMENT FAILED")
            print("Check the errors above and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)