"""
Quick user registration via API
"""
import requests

url = "http://localhost:8000/api/v1/auth/register"
data = {
    "email": "sharma333@test.com",
    "password": "Test@1234",
    "first_name": "Sharma",
    "last_name": "Test",
    "role": "patient",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-01",
    "gender": "male"
}

print("Registering user sharma333@test.com...")
try:
    response = requests.post(url, json=data, timeout=5)
    if response.status_code == 201:
        print("✅ User created!")
        print(f"   User ID: {response.json()['user']['id']}")
    elif response.status_code == 400 and "exists" in response.text:
        print("✅ User already exists - ready to use!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
