#!/usr/bin/env python3
"""
Simple test server to verify Grok integration
"""

import os
import requests
import json
import time

def test_simple_grok():
    """Test Grok API directly"""
    print("🤖 Testing Grok API directly...")
    
    # API key should be loaded from environment variable
    api_key = os.getenv("GROK_API_KEY", "your-grok-api-key-here")
    
    if not api_key or api_key == "your-grok-api-key-here":
        print("❌ Error: GROK_API_KEY environment variable not set")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-beta",
        "messages": [
            {"role": "system", "content": "You are Grok, a helpful AI assistant."},
            {"role": "user", "content": "Hello! Please respond with 'GROK_DIRECT_TEST_OK' to confirm you're working."}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Direct Grok API Test Successful!")
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"Grok Response: {content}")
            return True
        else:
            print(f"❌ Direct API test failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Direct API test error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎭 PLAYALTER - Direct Grok API Test")
    print("=" * 50)
    
    success = test_simple_grok()
    
    if success:
        print("\n🎉 GROK API KEY WORKS! 🎉")
        print("🔧 Ready for integration into PLAYALTER!")
    else:
        print("\n❌ GROK API KEY FAILED")
        print("💡 Check API key or Grok service status")
    
    exit(0 if success else 1)
