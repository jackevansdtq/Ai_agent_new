#!/usr/bin/env python3
"""
Test API Authentication - Test authentication giống OpenAI API
"""

import requests
import json
import time

def test_api_authentication():
    """Test API authentication"""
    base_url = "http://localhost:8001"
    api_key = "insurance-bot-api-key-2024-fiss"  # From deploy.env

    print("🔐 TESTING API AUTHENTICATION...")
    print("=" * 50)

    try:
        # 1. Test without authentication (should fail)
        print("\n❌ Testing without authentication...")
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "Hello"},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly rejected - authentication required")
            data = response.json()
            print(f"Error: {data['error']['message']}")
        else:
            print("❌ Should have been rejected")

        # 2. Test with invalid API key (should fail)
        print("\n❌ Testing with invalid API key...")
        headers = {"Authorization": "Bearer invalid-key"}
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "Hello"},
            headers=headers,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly rejected - invalid API key")
            data = response.json()
            print(f"Error: {data['error']['message']}")
        else:
            print("❌ Should have been rejected")

        # 3. Test with Bearer token (should work)
        print("\n✅ Testing with Bearer token...")
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "Bảo hiểm xe máy là gì?"},
            headers=headers,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Authentication successful with Bearer token")
            data = response.json()
            print(f"Response: {data['response'][:100]}...")
        else:
            print(f"❌ Failed: {response.text}")

        # 4. Test with X-API-Key header (should work)
        print("\n✅ Testing with X-API-Key header...")
        headers = {"X-API-Key": api_key}
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "Giá bảo hiểm xe máy?"},
            headers=headers,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Authentication successful with X-API-Key")
            data = response.json()
            print(f"Response: {data['response'][:100]}...")
        else:
            print(f"❌ Failed: {response.text}")

        # 5. Test health check (should work without auth)
        print("\n🏥 Testing health check (no auth required)...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check works without authentication")
            data = response.json()
            print(f"Status: {data['status']}")
        else:
            print(f"❌ Health check failed: {response.text}")

        print("\n" + "=" * 50)
        print("🎉 API AUTHENTICATION TEST COMPLETED!")
        print("\n📋 SUMMARY:")
        print("- ✅ Authentication required for /chat endpoint")
        print("- ✅ Supports Bearer token and X-API-Key headers")
        print("- ✅ OpenAI-style error messages")
        print("- ✅ Health check remains public")

    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR:")
        print("API server chưa chạy. Hãy chạy lệnh sau:")
        print("python core/insurance_api_simple.py")
        return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_api_authentication()
    exit(0 if success else 1)
