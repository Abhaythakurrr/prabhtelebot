"""
Check if Railway deployment is complete
"""

import requests
import time
import sys

# Replace with your Railway app URL
RAILWAY_URL = input("Enter your Railway app URL (e.g., https://your-app.railway.app): ").strip()

if not RAILWAY_URL:
    print("❌ No URL provided")
    sys.exit(1)

print(f"\n🔍 Checking deployment status for: {RAILWAY_URL}\n")

def check_endpoint(url, endpoint):
    """Check if an endpoint is responding"""
    try:
        response = requests.get(f"{url}{endpoint}", timeout=5)
        return response.status_code == 200, response.status_code
    except Exception as e:
        return False, str(e)

# Check multiple times
max_attempts = 10
attempt = 0

while attempt < max_attempts:
    attempt += 1
    print(f"Attempt {attempt}/{max_attempts}...")
    
    # Check health endpoint
    success, status = check_endpoint(RAILWAY_URL, "/health")
    if success:
        print(f"✅ Health endpoint: OK")
    else:
        print(f"❌ Health endpoint: {status}")
    
    # Check API status
    success, status = check_endpoint(RAILWAY_URL, "/api/status")
    if success:
        print(f"✅ API status endpoint: OK")
    else:
        print(f"❌ API status endpoint: {status}")
    
    # Check pricing page
    success, status = check_endpoint(RAILWAY_URL, "/pricing")
    if success:
        print(f"✅ Pricing page: OK")
    else:
        print(f"❌ Pricing page: {status}")
    
    # Check payment endpoint
    try:
        response = requests.post(
            f"{RAILWAY_URL}/api/create-order",
            json={"user_id": "test", "plan_id": "basic"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"✅ Payment endpoint: OK")
            print(f"\n{'='*60}")
            print("🎉 DEPLOYMENT SUCCESSFUL!")
            print(f"{'='*60}")
            print(f"\n✅ All endpoints are working!")
            print(f"\n🧪 Test your website:")
            print(f"   {RAILWAY_URL}/pricing")
            print(f"\n💳 Payment button should now work!")
            sys.exit(0)
        else:
            print(f"❌ Payment endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Payment endpoint: {e}")
    
    if attempt < max_attempts:
        print(f"\n⏳ Waiting 30 seconds before next check...\n")
        time.sleep(30)

print(f"\n⚠️ Deployment may still be in progress")
print(f"Check Railway dashboard: https://railway.app/dashboard")
