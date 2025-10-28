"""
Trigger Railway Deployment
This will create an empty commit to trigger Railway auto-deploy
"""

import subprocess
import sys

print("🚀 TRIGGERING RAILWAY DEPLOYMENT\n")

print("Step 1: Creating empty commit to trigger deploy...")
try:
    result = subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "🚀 Deploy: Latest payment and generation fixes"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Empty commit created")
    else:
        print(f"❌ Error creating commit: {result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\nStep 2: Pushing to GitHub (will trigger Railway deploy)...")
try:
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Pushed to GitHub")
        print(result.stdout)
    else:
        print(f"❌ Error pushing: {result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ DEPLOYMENT TRIGGERED!")
print("="*60)
print("\n📋 Next Steps:")
print("1. Go to Railway dashboard: https://railway.app/dashboard")
print("2. Click on your project")
print("3. Watch the deployment logs")
print("4. Wait for 'Deployed' status (usually 2-5 minutes)")
print("\n🧪 After Deployment:")
print("1. Test website: https://your-app.railway.app/pricing")
print("2. Test API: https://your-app.railway.app/api/status")
print("3. Test payment button - should open Razorpay modal")
print("\n✅ Your latest code will be live in a few minutes!")
