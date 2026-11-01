"""
Create test doctor and admin users with known passwords
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def create_users():
    print("="*70)
    print("CREATING TEST USERS WITH KNOWN PASSWORDS")
    print("="*70)
    
    users = [
        {
            "email": "testadmin@medinova.com",
            "password": "Admin@123",
            "first_name": "Test",
            "last_name": "Admin",
            "role": "admin",
            "phone": "+1234567890",
            "date_of_birth": "1985-01-01",
            "gender": "male"
        },
        {
            "email": "testdoctor@medinova.com",
            "password": "Doctor@123",
            "first_name": "Test",
            "last_name": "Doctor",
            "role": "doctor",
            "phone": "+1234567891",
            "date_of_birth": "1980-01-01",
            "gender": "female"
        }
    ]
    
    for user in users:
        print(f"\n{'='*70}")
        print(f"Creating {user['role'].upper()}: {user['email']}")
        print(f"{'='*70}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register",
                json=user,
                timeout=5
            )
            
            if response.status_code == 201:
                print(f"✅ SUCCESS!")
                print(f"   Email: {user['email']}")
                print(f"   Password: {user['password']}")
                print(f"   Role: {user['role']}")
            elif "exists" in response.text.lower():
                print(f"ℹ️  User already exists")
                print(f"   Email: {user['email']}")
                print(f"   Password: {user['password']}")
                print(f"   Role: {user['role']}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ CREDENTIALS READY TO USE:")
    print("="*70)
    print("\n👨‍💼 ADMIN LOGIN:")
    print("   Email: testadmin@medinova.com")
    print("   Password: Admin@123")
    print("\n👨‍⚕️ DOCTOR LOGIN:")
    print("   Email: testdoctor@medinova.com")
    print("   Password: Doctor@123")
    print("\n👤 PATIENT LOGIN:")
    print("   Email: sharma333@test.com")
    print("   Password: Test@1234")
    print("\n" + "="*70)
    print("🌐 Login at: http://localhost:5173/login")
    print("="*70)

if __name__ == "__main__":
    create_users()
