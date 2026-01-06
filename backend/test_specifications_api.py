"""Test the specifications API endpoint"""
import requests
import json

try:
    response = requests.get('http://localhost:8888/api/specifications')
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
    print("Make sure backend server is running: python server.py")

