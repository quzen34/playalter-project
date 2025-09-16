"""
PLAYALTER Production Test Suite
Tests all endpoints on the deployed Vercel production instance
"""

import requests
import json
import time
import os
from datetime import datetime

# Production URL from latest deployment
PRODUCTION_URL = "https://playalter-g9xtgp20l-fatihs-projects-9166e25f.vercel.app"
API_BASE = f"{PRODUCTION_URL}/api"

def load_base64_image(filename):
    """Load base64 image data from file"""
    try:
        with open(filename, 'r') as file:
            base64_data = file.read().strip()
            print(f"✅ Loaded base64 image from {filename}")
            return base64_data
    except FileNotFoundError:
        print(f"❌ Base64 file {filename} not found")
        return "data:image/jpeg;base64,test"
    except Exception as e:
        print(f"❌ Error loading base64 file: {str(e)}")
        return "data:image/jpeg;base64,test"

def test_endpoint(endpoint, method="GET", data=None, expected_status=200, validate_orchestrate=False):
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
            response_data = response.json() if response.content else {}
            
            # Special validation for orchestrate endpoint
            if validate_orchestrate and response_data:
                required_fields = ['status', 'swapped_url', 'stream_token']
                missing_fields = [field for field in required_fields if field not in response_data]
                
                if missing_fields:
                    print(f"❌ FAIL - Missing fields: {missing_fields}")
                    return False, response_data
                
                if response_data.get('status') != 'success':
                    print(f"❌ FAIL - Status not success: {response_data.get('status')}")
                    return False, response_data
                
                print(f"✅ PASS (HTTP {response.status_code}) - Orchestration validated")
                print(f"   Status: {response_data.get('status')}")
                print(f"   Swapped URL: {response_data.get('swapped_url', 'N/A')[:50]}...")
                print(f"   Stream Token: {response_data.get('stream_token', 'N/A')[:30]}...")
                return True, response_data
            
            print(f"✅ PASS (HTTP {response.status_code})")
            return True, response_data
        else:
            print(f"❌ FAIL (HTTP {response.status_code})")
            print(f"   Response: {response.text[:200]}...")
            return False, {}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {str(e)}")
        return False, {}
    except json.JSONDecodeError as e:
        print(f"❌ JSON ERROR: {str(e)}")
        return False, {}

def main():
    """Run all production tests"""
    print("🚀 PLAYALTER Production Test Suite")
    print("=" * 50)
    print(f"Testing: {PRODUCTION_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Load real selfie base64 for orchestration test
    base64_image = load_base64_image('base64.txt')
    
    tests = [
        # Basic connectivity
        ("/health", "GET", None, 200, False),
        ("/", "GET", None, 200, False),
        
        # AI Services  
        ("/ai-agents", "GET", None, 200, False),
        ("/face-swap", "POST", {
            "source_base64": "data:image/jpeg;base64,test",
            "target_base64": "data:image/jpeg;base64,test",
            "user_id": "test_user"
        }, 200, False),
        ("/ar-mask", "POST", {
            "image": "data:image/jpeg;base64,test",
            "mask_type": "cat_ears",
            "user_id": "test_user"
        }, 200, False),
        ("/face-ethics", "POST", {
            "image_base64": "data:image/jpeg;base64,test"
        }, 200, False),
        ("/live-stream", "POST", {
            "channel_name": "test_channel",
            "uid": 12345
        }, 200, False),
        
        # Grok AI
        ("/grok/chat", "POST", {
            "messages": [{"role": "user", "content": "Hello, test message"}]
        }, 200, False),
        
        # Stripe
        ("/customers", "POST", {
            "email": "test@playalter.com",
            "name": "Test User"
        }, 200, False),
        
        # N8N
        ("/n8n/workflows", "GET", None, 200, False),
        
        # Orchestrate with real selfie base64 input
        ("/orchestrate", "POST", {
            "input_image": base64_image,
            "ethnic": "diverse",
            "quality": "ultra",
            "AR": "overlays",
            "user_id": "test_user_production",
            "session_id": f"session_{int(time.time())}"
        }, 200, True),
        
        # User Testing
        ("/user-test", "POST", {
            "user_id": "test_user",
            "feedback": "Great platform! Love the AI features.",
            "test_type": "production",
            "rating": 5
        }, 200, False)
    ]
    
    passed = 0
    total = len(tests)
    
    print("\n🧪 Running Tests...")
    print("-" * 30)
    
    for test in tests:
        endpoint = test[0]
        method = test[1]
        data = test[2] if len(test) > 2 else None
        expected_status = test[3] if len(test) > 3 else 200
        validate_orchestrate = test[4] if len(test) > 4 else False
        
        success, response = test_endpoint(endpoint, method, data, expected_status, validate_orchestrate)
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
