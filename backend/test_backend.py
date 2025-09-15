#!/usr/bin/env python3
"""
PLAYALTER Backend Test Script
Tests the enhanced backend with n8n and Stripe integration
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 10

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Version: {data['version']}")
            print(f"   Integrations: {data['integrations']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False

def test_orchestrate_endpoint():
    """Test the orchestrate endpoint"""
    print("\n🔍 Testing orchestrate endpoint...")
    try:
        test_data = {
            "operation": "test",
            "request": "Test orchestration request",
            "user_id": "test_user_123"
        }
        response = requests.post(
            f"{BASE_URL}/api/orchestrate", 
            json=test_data, 
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Orchestrate test passed: {data['status']}")
            print(f"   Operation: {data['operation']}")
            print(f"   Message: {data['message']}")
            return True
        else:
            print(f"❌ Orchestrate test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Orchestrate test error: {e}")
        return False

def test_home_endpoint():
    """Test the home/root endpoint"""
    print("\n🔍 Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Home endpoint test passed")
            print(f"   Service: {data['service']}")
            print(f"   Version: {data['version']}")
            print(f"   Available endpoints: {len(data['endpoints'])} categories")
            return True
        else:
            print(f"❌ Home endpoint test failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Home endpoint test error: {e}")
        return False

def test_face_swap_endpoint():
    """Test the face swap endpoint"""
    print("\n🔍 Testing face swap endpoint...")
    try:
        test_data = {
            "source_image": "https://example.com/source.jpg",
            "target_image": "https://example.com/target.jpg",
            "user_id": "test_user_123"
        }
        response = requests.post(
            f"{BASE_URL}/api/face-swap", 
            json=test_data, 
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Face swap test passed: {data['status']}")
            print(f"   Message: {data['message']}")
            return True
        else:
            print(f"❌ Face swap test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Face swap test error: {e}")
        return False

def test_ar_mask_endpoint():
    """Test the AR mask endpoint"""
    print("\n🔍 Testing AR mask endpoint...")
    try:
        test_data = {
            "image": "https://example.com/image.jpg",
            "mask_type": "cat",
            "user_id": "test_user_123"
        }
        response = requests.post(
            f"{BASE_URL}/api/ar-mask", 
            json=test_data, 
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AR mask test passed: {data['status']}")
            print(f"   Message: {data['message']}")
            return True
        else:
            print(f"❌ AR mask test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AR mask test error: {e}")
        return False

def test_n8n_workflows_endpoint():
    """Test the n8n workflows endpoint"""
    print("\n🔍 Testing n8n workflows endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/n8n/workflows", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ n8n workflows test passed: {data['status']}")
            if 'workflows' in data:
                print(f"   Workflows available: {len(data.get('workflows', []))}")
            return True
        else:
            print(f"⚠️  n8n workflows test: {response.status_code} (n8n may not be running)")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"⚠️  n8n workflows test error: {e} (n8n may not be running)")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 PLAYALTER Backend Test Suite")
    print("=" * 50)
    print(f"Testing backend at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Home Endpoint", test_home_endpoint),
        ("Orchestrate API", test_orchestrate_endpoint),
        ("Face Swap API", test_face_swap_endpoint),
        ("AR Mask API", test_ar_mask_endpoint),
        ("n8n Workflows", test_n8n_workflows_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        result = test_func()
        if result:
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    elif passed >= total - 1:
        print("✅ Most tests passed! Backend is mostly functional.")
        print("   (n8n integration may need setup)")
    else:
        print("❌ Some tests failed. Check the backend configuration.")
    
    print("\n🔗 Quick Links:")
    print(f"   Backend API: {BASE_URL}")
    print(f"   Health Check: {BASE_URL}/health")
    print(f"   API Documentation: {BASE_URL}/")
    print("   n8n Interface: http://localhost:5678 (if running)")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
