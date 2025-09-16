#!/usr/bin/env python3
"""
🤖 Grok (XAI) Integration Test
=============================
Test Grok AI integration and capabilities
"""

import requests
import json
import os
from datetime import datetime

def test_grok_chat():
    """Test Grok chat completion"""
    print("🤖 Testing Grok Chat Completion...")
    
    # Test data
    payload = {
        "messages": [
            {"role": "system", "content": "You are Grok, a helpful AI assistant."},
            {"role": "user", "content": "Hello Grok! Please respond with 'GROK_TEST_OK' to confirm you're working."}
        ],
        "model": "grok-beta",
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/grok/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Grok Chat Test Successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Check if response contains expected content
            if result.get('status') == 'success':
                grok_response = result.get('result', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"Grok said: {grok_response}")
                return True
            else:
                print("❌ Unexpected response format")
                return False
        else:
            print(f"❌ Chat test failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test error: {str(e)}")
        return False

def test_grok_reasoning():
    """Test Grok advanced reasoning"""
    print("\n🧠 Testing Grok Advanced Reasoning...")
    
    # Test data
    payload = {
        "context": "PLAYALTER is a platform that integrates multiple AI services including face swapping, streaming, and content generation.",
        "question": "What are the key advantages of using an orchestrated multi-platform approach for AI applications?",
        "reasoning_depth": "detailed",
        "max_tokens": 200,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/grok/reason",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=45
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Grok Reasoning Test Successful!")
            print(f"Context: {result.get('context')}")
            print(f"Question: {result.get('question')}")
            print(f"Reasoning: {result.get('reasoning')}")
            return True
        else:
            print(f"❌ Reasoning test failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Reasoning test error: {str(e)}")
        return False

def test_backend_health():
    """Test if backend recognizes Grok integration"""
    print("\n❤️ Testing Backend Health with Grok...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            integrations = health_data.get('integrations', {})
            grok_status = integrations.get('grok', 'not_found')
            
            print(f"Grok Integration Status: {grok_status}")
            
            if grok_status in ['configured', 'connected']:
                print("✅ Grok integration detected in backend!")
                return True
            else:
                print("⚠️ Grok integration not configured")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def main():
    """Run all Grok integration tests"""
    print("🎭 PLAYALTER - Grok (XAI) Integration Test Suite")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Test results
    results = {
        "health_check": test_backend_health(),
        "chat_completion": test_grok_chat(),
        "advanced_reasoning": test_grok_reasoning()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL GROK INTEGRATION TESTS PASSED! 🎉")
        print("🤖 Grok is ready for AI agent operations!")
    elif passed > 0:
        print("\n⚠️ PARTIAL SUCCESS - Some tests passed")
        print("🔧 Check configuration and try again")
    else:
        print("\n❌ ALL TESTS FAILED")
        print("💡 Make sure backend is running and Grok API key is configured")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
