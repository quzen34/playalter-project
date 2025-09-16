"""
PLAYALTER Production Test Suite
Tests all endpoints on the deployed Vercel production instance
"""

import requests
import json
import time
from datetime import datetime

# Production URL from latest deployment
PRODUCTION_URL = "https://playalter-g9xtgp20l-fatihs-projects-9166e25f.vercel.app"
API_BASE = f"{PRODUCTION_URL}/api"

def test_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Test a specific endpoint"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        print(f"Testing {method} {endpoint}... ", end="")
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.request(method, url, json=data, timeout=30)
        
        if response.status_code == expected_status:
            print(f"✅ PASS (HTTP {response.status_code})")
            return True, response.json() if response.content else {}
        else:
            print(f"❌ FAIL (HTTP {response.status_code})")
            print(f"   Response: {response.text[:200]}...")
            return False, {}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {str(e)}")
        return False, {}

def main():
    """Run all production tests"""
    print("🚀 PLAYALTER Production Test Suite")
    print("=" * 50)
    print(f"Testing: {PRODUCTION_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 50)
    
    tests = [
        # Basic connectivity
        ("/health", "GET"),
        ("/", "GET"),
        
        # AI Services  
        ("/ai-agents", "GET"),
        ("/face-swap", "POST", {
            "source_base64": "data:image/jpeg;base64,test",
            "target_base64": "data:image/jpeg;base64,test",
            "user_id": "test_user"
        }),
        ("/ar-mask", "POST", {
            "image": "data:image/jpeg;base64,test",
            "mask_type": "cat_ears",
            "user_id": "test_user"
        }),
        ("/face-ethics", "POST", {
            "image_base64": "data:image/jpeg;base64,test"
        }),
        ("/live-stream", "POST", {
            "channel_name": "test_channel",
            "uid": 12345
        }),
        
        # Grok AI
        ("/grok/chat", "POST", {
            "messages": [{"role": "user", "content": "Hello, test message"}]
        }),
        
        # Stripe
        ("/customers", "POST", {
            "email": "test@playalter.com",
            "name": "Test User"
        }),
        
        # N8N
        ("/n8n/workflows", "GET"),
        ("/orchestrate", "POST", {
            "operation": "general",
            "request": "Test orchestration",
            "user_id": "test_user"
        }),
        
        # User Testing
        ("/user-test", "POST", {
            "user_id": "test_user",
            "feedback": "Great platform! Love the AI features.",
            "test_type": "production",
            "rating": 5
        })
    ]
    
    passed = 0
    total = len(tests)
    
    print("\n🧪 Running Tests...")
    print("-" * 30)
    
    for test in tests:
        endpoint = test[0]
        method = test[1]
        data = test[2] if len(test) > 2 else None
        
        success, response = test_endpoint(endpoint, method, data)
        if success:
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ PLAYALTER is fully operational on production")
    else:
        print(f"⚠️  {total - passed} tests failed")
        print("Some endpoints may need additional configuration")
    
    print(f"\n🌐 Production URLs:")
    print(f"   Frontend: {PRODUCTION_URL}")
    print(f"   API: {API_BASE}")
    print(f"   Health: {API_BASE}/health")
    
    # Test frontend accessibility
    print(f"\n🔍 Testing frontend accessibility...")
    try:
        response = requests.get(PRODUCTION_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend error: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend test failed: {str(e)}")

if __name__ == "__main__":
    main()
