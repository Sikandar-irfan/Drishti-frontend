#!/usr/bin/env python3
"""
Backend Test Script
Quick test to verify all API endpoints are working correctly
"""

import requests
import json
import time

# Configuration
RPI_IP = "192.168.0.101"
RPI_PORT = "5000"
BASE_URL = f"http://{RPI_IP}:{RPI_PORT}"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            if response.headers.get('content-type', '').startswith('application/json'):
                print(f"   Data: {json.dumps(response.json(), indent=2)[:200]}...")
            else:
                print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ {method} {endpoint}: ERROR - {e}")
        return False

def main():
    print("🚀 Testing Raspberry Pi Backend API Endpoints")
    print("=" * 50)
    
    # Test connection
    print(f"🔌 Testing connection to {BASE_URL}")
    
    endpoints_to_test = [
        ("/api/system_status", "GET"),
        ("/api/slam_map", "GET"),
        ("/api/voice_status", "GET"),
        ("/video_feed", "GET"),
        ("/", "GET"),  # Dashboard
    ]
    
    success_count = 0
    total_count = len(endpoints_to_test)
    
    for endpoint, method in endpoints_to_test:
        if test_endpoint(endpoint, method):
            success_count += 1
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {success_count}/{total_count} endpoints working")
    
    if success_count == total_count:
        print("🎉 All endpoints are working correctly!")
        print("✅ Backend is ready for frontend integration")
    else:
        print("⚠️  Some endpoints are not responding")
        print("💡 Make sure the backend is running on the Raspberry Pi")
    
    print(f"\n🌐 Backend URL: {BASE_URL}")
    print(f"📹 Stream URL: {BASE_URL}/video_feed")

if __name__ == "__main__":
    main()