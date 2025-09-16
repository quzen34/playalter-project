"""
PLAYALTER Local Production Test
www.playalter.com domain simülasyonu için local test
"""

import os
import sys
import subprocess
import time
import requests
import threading
from pathlib import Path

def start_backend():
    """Start backend server"""
    print("🚀 Starting backend server...")
    os.chdir("backend")
    
    # Start Flask app
    env = os.environ.copy()
    env["FLASK_ENV"] = "production"
    env["HOST"] = "0.0.0.0"
    env["PORT"] = "8000"
    
    process = subprocess.Popen([
        sys.executable, "app_enhanced.py"
    ], env=env)
    
    os.chdir("..")
    return process

def start_frontend():
    """Start frontend development server"""
    print("🌐 Starting frontend server...")
    os.chdir("frontend")
    
    # Start Vite dev server
    process = subprocess.Popen([
        "npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"
    ])
    
    os.chdir("..")
    return process

def wait_for_service(url, timeout=30):
    """Wait for service to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 404]:  # 404 is OK for some endpoints
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_local_endpoints():
    """Test local endpoints"""
    print("\n🧪 Testing Local Endpoints...")
    print("-" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test backend health
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            data = response.json()
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            integrations = data.get('integrations', {})
            for name, status in integrations.items():
                status_icon = "✅" if status == "connected" or status == "configured" else "❌"
                print(f"   {name}: {status_icon} {status}")
        else:
            print(f"❌ Backend health check failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Backend test error: {str(e)}")
    
    # Test AI endpoints
    print("\n🤖 Testing AI Services...")
    
    ai_tests = [
        ("/api/ai-agents", "GET"),
        ("/api/face-swap", "POST", {
            "source_base64": "data:image/jpeg;base64,test",
            "target_base64": "data:image/jpeg;base64,test", 
            "user_id": "test_user"
        }),
        ("/api/orchestrate", "POST", {
            "operation": "general",
            "request": "Test local orchestration",
            "user_id": "test_user"
        })
    ]
    
    for test in ai_tests:
        endpoint = test[0]
        method = test[1] 
        data = test[2] if len(test) > 2 else None
        
        try:
            url = f"{base_url}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                print(f"✅ {endpoint} - PASS")
            else:
                print(f"❌ {endpoint} - FAIL (HTTP {response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint} - ERROR: {str(e)}")

def main():
    """Main test function"""
    print("🏠 PLAYALTER Local Production Test")
    print("Simulating www.playalter.com environment locally")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("backend/app_enhanced.py").exists():
        print("❌ Error: Please run from project root directory")
        return 1
    
    # Start services
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend()
        print("⏳ Waiting for backend to start...")
        
        if wait_for_service("http://localhost:8000/health", 20):
            print("✅ Backend is ready!")
        else:
            print("❌ Backend failed to start")
            return 1
        
        # Start frontend  
        frontend_process = start_frontend()
        print("⏳ Waiting for frontend to start...")
        
        if wait_for_service("http://localhost:5173", 15):
            print("✅ Frontend is ready!")
        else:
            print("❌ Frontend failed to start")
        
        # Run tests
        test_local_endpoints()
        
        print("\n🎉 Local Production Test Complete!")
        print("\n🌐 Access URLs:")
        print("   Frontend: http://localhost:5173")
        print("   Backend API: http://localhost:8000")
        print("   Health Check: http://localhost:8000/health")
        print("   AI Agents: http://localhost:8000/api/ai-agents")
        
        print("\n📝 Test your features:")
        print("   - Visit frontend in browser")
        print("   - Test face swap functionality")
        print("   - Try AI agent orchestration") 
        print("   - Verify Stripe integration")
        print("   - Check hierarchical AI system")
        
        print("\n⌨️  Press Ctrl+C to stop servers")
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping servers...")
        
    finally:
        # Clean up processes
        if backend_process:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        if frontend_process:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print("✅ Cleanup complete")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
