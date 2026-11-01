"""
Create the test user in the current backend session's mongomock database
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def create_user():
    print("="*60)
    print("CREATING USER IN MONGOMOCK SESSION")
    print("="*60)
    
    # Register the user
    register_data = {
        "email": "sharma333@test.com",
        "password": "Test@1234",
        "first_name": "Sharma",
        "last_name": "Test",
        "role": "patient",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01",
        "gender": "male"
    }
    
    print("\n1. Registering user sharma333@test.com...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=register_data,
            timeout=10
        )
        
        if response.status_code == 201:
            print("   ✅ User created successfully!")
            data = response.json()
            print(f"   - User ID: {data.get('user', {}).get('id')}")
            print(f"   - Email: {data.get('user', {}).get('email')}")
            print(f"   - Role: {data.get('user', {}).get('role')}")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print("   ℹ️  User already exists - logging in instead...")
            
            # Login
            login_data = {
                "email": "sharma333@test.com",
                "password": "Test@1234"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("   ✅ Login successful!")
                data = response.json()
                print(f"   - User ID: {data.get('user', {}).get('id')}")
                return True
            else:
                print(f"   ❌ Login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend not running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_user()
    print("\n" + "="*60)
    if success:
        print("✅ USER IS READY FOR SMART UPLOAD!")
        print("   Go to: http://localhost:5173/patient/smart-upload")
    else:
        print("❌ FAILED TO CREATE USER")
    print("="*60)
