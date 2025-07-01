#!/usr/bin/env python3
"""
Test script to verify improved error handling in the LinkedIn backend.
This script will help test different error scenarios and ensure proper error messages are displayed.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app
from fastapi.testclient import TestClient

def test_error_handling():
    """Test various error scenarios to ensure proper error messages are displayed."""
    
    client = TestClient(app)
    
    print("Testing LinkedIn backend error handling...")
    print("=" * 50)
    
    # Test 1: Health check when LinkedIn agent is not initialized
    print("\n1. Testing health check with uninitialized LinkedIn agent:")
    try:
        response = client.get("/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test 2: Profile fetch with uninitialized LinkedIn agent
    print("\n2. Testing profile fetch with uninitialized LinkedIn agent:")
    try:
        response = client.get("/api/profile/test-user")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test 3: Queue status with uninitialized LinkedIn agent
    print("\n3. Testing queue status with uninitialized LinkedIn agent:")
    try:
        response = client.get("/api/queue")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test 4: Root endpoint (should work regardless of LinkedIn agent status)
    print("\n4. Testing root endpoint:")
    try:
        response = client.get("/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Error handling test completed!")

if __name__ == "__main__":
    test_error_handling() 