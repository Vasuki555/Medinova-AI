"""
Register test users via API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

test_users = [
    {
        "email": "patient@test.com",
        "password": "Password@123",
        "first_name": "John",
        "last_name": "Patient",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15",
        "role": "patient",
        "blood_group": "O+",
        "emergency_contact_name": "Jane Patient",
        "emergency_contact_phone": "+1234567899",
        "emergency_contact_relationship": "Spouse"
    },
    {
        "email": "doctor@test.com",
        "password": "Password@123",
        "first_name": "Sarah",
        "last_name": "Smith",
        "phone": "+1234567891",
        "date_of_birth": "1985-05-20",
        "role": "doctor",
        "specialization": "General Physician",
        "license_number": "DOC123456",
        "years_of_experience": 10,
        "qualification": "MBBS, MD",
        "consultation_fee": 100.0,
        "hospital_affiliation": "City General Hospital"
    },
    {
        "email": "admin@test.com",
        "password": "Password@123",
        "first_name": "Admin",
        "last_name": "User",
        "phone": "+1234567892",
        "date_of_birth": "1980-03-10",
        "role": "admin"
    }
]

print("🚀 Registering test users...\n")

for user in test_users:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print(f"✅ Created {user['role'].upper()}: {user['email']}")
        elif response.status_code == 400 and "already registered" in response.text.lower():
            print(f"⚠️  {user['role'].upper()}: {user['email']} already exists")
        else:
            print(f"❌ Failed to create {user['email']}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error creating {user['email']}: {str(e)}")

print("\n" + "=" * 60)
print("📋 LOGIN CREDENTIALS")
print("=" * 60)
print("\n🧑 PATIENT:")
print("  Email:    patient@test.com")
print("  Password: Password@123")
print("  URL:      http://localhost:5173/login")
print("\n👨‍⚕️ DOCTOR:")
print("  Email:    doctor@test.com")
print("  Password: Password@123")
print("  URL:      http://localhost:5173/login")
print("\n👤 ADMIN:")
print("  Email:    admin@test.com")
print("  Password: Password@123")
print("  URL:      http://localhost:5173/login")
print("\n" + "=" * 60)
print("\n✨ You can now login at: http://localhost:5173/login")
