#!/usr/bin/env python3
"""
Simple test script untuk memverifikasi backend berfungsi dengan baik
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_register():
    """Test user registration"""
    print("\nTesting user registration...")
    try:
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        if response.status_code in [201, 409]:  # 409 means user already exists
            print("✅ Registration endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {e}")

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    try:
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        if response.status_code == 200:
            print("✅ Login successful")
            result = response.json()
            if "token" in result:
                print("✅ JWT token received")
                return result["token"]
            else:
                print("❌ No token in response")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    return None

def test_products():
    """Test products endpoint"""
    print("\nTesting products endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/")
        if response.status_code == 200:
            print("✅ Products endpoint working")
            products = response.json()
            print(f"Found {len(products)} products")
        else:
            print(f"❌ Products failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Products error: {e}")

def test_cors():
    """Test CORS headers"""
    print("\nTesting CORS headers...")
    try:
        response = requests.options(f"{BASE_URL}/api/health")
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        if cors_headers:
            print("✅ CORS headers present")
            print(f"CORS Origins: {cors_headers}")
        else:
            print("❌ CORS headers missing")
    except Exception as e:
        print(f"❌ CORS test error: {e}")

if __name__ == "__main__":
    print("🚀 Testing PlayGenix Backend...")
    print("=" * 50)
    
    test_health_check()
    test_register()
    token = test_login()
    test_products()
    test_cors()
    
    print("\n" + "=" * 50)
    print("✅ Backend testing completed!")
    print(f"Backend URL: {BASE_URL}")
    print("Frontend dapat terhubung ke backend ini.") 