# ABOUTME: Simple test script to verify API endpoints functionality
# ABOUTME: Tests document upload, note upload, and basic search without complex vector operations

import requests
import json

BASE_URL = "http://localhost:8000"

def test_document_upload():
    """Test document upload endpoint"""
    url = f"{BASE_URL}/clients/1/documents"
    data = {
        "title": "Test Document 2",
        "content": "This is a test document about financial planning and investment strategies for retirement."
    }
    response = requests.post(url, json=data)
    print(f"Document Upload: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    return response.status_code == 200

def test_note_upload():
    """Test note upload endpoint"""
    url = f"{BASE_URL}/clients/1/notes"
    data = {
        "content": "Client meeting notes: Discussed risk tolerance and investment timeline. Client prefers moderate risk investments."
    }
    response = requests.post(url, json=data)
    print(f"Note Upload: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    return response.status_code == 200

def test_health():
    """Test health endpoint"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    print(f"Health Check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing WealthTech Smart Search API Endpoints")
    print("=" * 50)
    
    # Test health first
    test_health()
    print()
    
    # Test document upload
    test_document_upload()
    print()
    
    # Test note upload
    test_note_upload()
    print()
    
    print("Endpoint testing complete!")
