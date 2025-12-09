#!/usr/bin/env python3
"""
Test Gemini API connection
Run this to diagnose chatbot issues
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

def test_gemini():
    print("Testing Gemini API...")
    print("-" * 50)
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    print(f"API Key: {GEMINI_API_KEY[:20]}...")
    print("-" * 50)
    
    # Test with simple message
    test_message = "Hello, can you help me with cybersecurity?"
    
    # Try gemini-2.5-flash first (current model)
    print("\n1. Testing gemini-2.5-flash...")
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{
                    "parts": [{"text": test_message}]
                }]
            },
            timeout=15
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   ✅ SUCCESS!")
                print(f"   Response: {ai_response[:100]}...")
                return True
            else:
                print(f"   ❌ Unexpected response structure: {result}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Try gemini-2.5-pro as fallback
    print("\n2. Testing gemini-2.5-pro (fallback)...")
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{
                    "parts": [{"text": test_message}]
                }]
            },
            timeout=15
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   ✅ SUCCESS with gemini-pro!")
                print(f"   Response: {ai_response[:100]}...")
                return True
            else:
                print(f"   ❌ Unexpected response structure: {result}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print("\n" + "-" * 50)
    print("❌ All Gemini API tests failed")
    print("\nPossible issues:")
    print("1. API key is invalid or expired")
    print("2. API key doesn't have access to these models")
    print("3. Network/firewall blocking requests")
    print("4. Google API service is down")
    print("\nCheck your API key at: https://aistudio.google.com/app/apikey")
    
    return False

if __name__ == '__main__':
    test_gemini()

