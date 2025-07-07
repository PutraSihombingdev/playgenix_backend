#!/usr/bin/env python3
"""
Quick test untuk memverifikasi backend berfungsi
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_register():
    """Test register"""
    print("\n🔍 Testing register...")
    try:
        data = {"username": "testuser", "password": "testpass"}
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [201, 409]  # 409 = user already exists
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login():
    """Test login"""
    print("\n🔍 Testing login...")
    try:
        data = {"username": "testuser", "password": "testpass"}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_products():
    """Test products"""
    print("\n🔍 Testing products...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Test PlayGenix Backend")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health),
        ("Register", test_register),
        ("Login", test_login),
        ("Products", test_products)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.") 