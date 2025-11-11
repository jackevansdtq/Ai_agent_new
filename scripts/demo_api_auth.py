#!/usr/bin/env python3
"""
Demo API Authentication - Hướng dẫn sử dụng API với authentication
"""

import requests
import json

def demo_api_auth():
    """Demo cách sử dụng API với authentication"""

    base_url = "http://localhost:8001"
    api_key = "fiss-c61197f847cc4682a91ada560bbd7119"

    print("🚀 DEMO API AUTHENTICATION")
    print("=" * 50)
    print(f"API URL: {base_url}")
    print(f"API Key: {api_key}")
    print()

    # Example 1: Using Bearer token
    print("📝 Example 1: Bearer Token Authentication")
    print("Header: Authorization: Bearer YOUR_API_KEY")
    print()

    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "message": "Bảo hiểm xe máy có những loại nào?",
        "session_id": "demo_session_123"
    }

    try:
        response = requests.post(f"{base_url}/chat", json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Response: {result['response']}")
            print(f"Processing time: {result['processing_time']:.2f}s")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")

    print("\n" + "-" * 50)

    # Example 2: Using X-API-Key header
    print("📝 Example 2: X-API-Key Header Authentication")
    print("Header: X-API-Key: YOUR_API_KEY")
    print()

    headers = {"X-API-Key": api_key}
    data = {
        "message": "Giá bảo hiểm xe máy khoảng bao nhiêu?",
    }

    try:
        response = requests.post(f"{base_url}/chat", json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Response: {result['response']}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")

    print("\n" + "-" * 50)

    # Example 3: Error without authentication
    print("📝 Example 3: Error Response (No Authentication)")
    print("No headers provided")
    print()

    try:
        response = requests.post(f"{base_url}/chat", json={"message": "Hello"})
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            error_data = response.json()
            print("✅ Correctly rejected!")
            print(f"Error: {error_data['error']['message']}")
            print(f"Type: {error_data['error']['type']}")
        else:
            print("❌ Should have been rejected")
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")

    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETED!")
    print("\n💡 Backend Integration Tips:")
    print("1. Store API key securely (not in client code)")
    print("2. Use environment variables for API keys")
    print("3. Handle authentication errors gracefully")
    print("4. Implement retry logic for network issues")
    print("5. Cache responses when appropriate")

def demo_curl_commands():
    """Show curl commands for testing"""

    api_key = "fiss-c61197f847cc4682a91ada560bbd7119"

    print("\n🛠️  CURL COMMANDS FOR TESTING:")
    print("=" * 50)

    print("\n# 1. Test with Bearer token:")
    print("""curl -X POST "http://localhost:8001/chat" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer fiss-c61197f847cc4682a91ada560bbd7119" \\
  -d '{"message": "Xin chào"}'""")

    print("\n# 2. Test with X-API-Key:")
    print("""curl -X POST "http://localhost:8001/chat" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: fiss-c61197f847cc4682a91ada560bbd7119" \\
  -d '{"message": "Bảo hiểm là gì"}'""")

    print("\n# 3. Test without authentication (should fail):")
    print("""curl -X POST "http://localhost:8001/chat" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hello"}'""")

    print("\n# 4. Test health check (no auth needed):")
    print("""curl -X GET "http://localhost:8001/health" """)

if __name__ == "__main__":
    demo_api_auth()
    demo_curl_commands()
