"""
Verify doctors via Admin API
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

# First, login as admin to get token
print("🔐 Logging in as admin...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "admin@test.com",
        "password": "Password@123"
    }
)

if login_response.status_code != 200:
    print(f"❌ Admin login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("✅ Admin logged in successfully\n")

# Get all users
print("📋 Fetching all users...")
users_response = requests.get(f"{BASE_URL}/admin/users", headers=headers)

if users_response.status_code != 200:
    print(f"❌ Failed to fetch users: {users_response.status_code}")
    exit(1)

users = users_response.json()
doctors = [u for u in users if u.get("role") == "doctor"]

print(f"Found {len(doctors)} doctors\n")
print("=" * 70)

verified_count = 0

for doctor in doctors:
    user_id = doctor["id"]
    email = doctor["email"]
    name = f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}"
    
    # Check verification status
    profile = doctor.get("profile", {})
    is_verified = profile.get("is_verified", False)
    
    if is_verified:
        print(f"✓ {name} ({email}) - Already verified")
        verified_count += 1
        continue
    
    # Verify the doctor
    print(f"🔄 Verifying {name} ({email})...")
    verify_response = requests.post(
        f"{BASE_URL}/admin/verify-doctor/{user_id}",
        headers=headers
    )
    
    if verify_response.status_code == 200:
        print(f"   ✅ Verified successfully")
        verified_count += 1
    else:
        print(f"   ❌ Failed: {verify_response.status_code}")

print("=" * 70)
print(f"\n🎉 Total verified doctors: {verified_count}/{len(doctors)}")
print("\n✨ All doctors are now available for appointments!")
