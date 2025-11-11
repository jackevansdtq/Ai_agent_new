#!/usr/bin/env python3
"""
Test script to check what headers Swagger UI sends
"""
import requests
import json

# Test 1: Without headers (should fail)
print("🧪 Test 1: Request WITHOUT headers")
try:
    response = requests.post(
        "http://localhost:8001/chat",
        json={"message": "test"},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 2: With Bearer token (should succeed)
print("🧪 Test 2: Request WITH Bearer token")
try:
    response = requests.post(
        "http://localhost:8001/chat",
        json={"message": "test"},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer fiss-c61197f847cc4682a91ada560bbd7119"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 3: With X-API-Key header (should succeed)
print("🧪 Test 3: Request WITH X-API-Key header")
try:
    response = requests.post(
        "http://localhost:8001/chat",
        json={"message": "test"},
        headers={
            "Content-Type": "application/json",
            "X-API-Key": "fiss-c61197f847cc4682a91ada560bbd7119"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

