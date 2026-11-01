"""
Seed mongomock with user and test data via API
This script registers the user and creates sample notifications/health records
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def seed_data():
    print("="*60)
    print("SEEDING MONGOMOCK WITH TEST DATA")
    print("="*60)
    
    # 1. Register/Login user
    print("\n1. Registering user...")
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
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=5)
        if response.status_code == 201:
            print("   ✅ User registered")
            token = response.json()["access_token"]
        elif "exists" in response.text.lower():
            print("   ℹ️  User exists, logging in...")
            login_response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": "sharma333@test.com", "password": "Test@1234"},
                timeout=5
            )
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                print("   ✅ Logged in successfully")
            else:
                print(f"   ❌ Login failed: {login_response.status_code}")
                return
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create sample health record
    print("\n2. Creating sample health record...")
    health_record_data = {
        "record_type": "lab_test",
        "title": "Blood Test Results",
        "description": "Routine blood work - all values normal",
        "recorded_at": datetime.utcnow().isoformat(),
        "lab_test": {
            "test_name": "Complete Blood Count",
            "test_date": datetime.utcnow().isoformat(),
            "results": [
                {"parameter": "Hemoglobin", "value": "14.5", "unit": "g/dL", "status": "normal"},
                {"parameter": "WBC Count", "value": "7500", "unit": "cells/mcL", "status": "normal"}
            ],
            "lab_name": "City Diagnostics",
            "notes": "All parameters within normal range"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/health-records",
            json=health_record_data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 201:
            print("   ✅ Health record created")
        else:
            print(f"   ⚠️  Health record creation: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # 3. Create sample medication
    print("\n3. Creating sample medication...")
    medication_data = {
        "medicine_name": "Aspirin",
        "dosage": "100mg",
        "frequency": "Once daily",
        "duration_days": 30,
        "instructions": "Take after breakfast",
        "meal_timing": "after_meal",
        "time_of_day": ["morning"],
        "current_quantity": 30,
        "start_date": datetime.utcnow().isoformat()
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/medications",
            json=medication_data,
            headers=headers,
            timeout=5
        )
        if response.status_code == 201:
            print("   ✅ Medication created (notification should be generated)")
        else:
            print(f"   ⚠️  Medication creation: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # 4. Check notifications
    print("\n4. Checking notifications...")
    try:
        response = requests.get(
            f"{BASE_URL}/notifications",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            notifications = response.json()
            print(f"   ✅ Found {len(notifications)} notifications")
            for notif in notifications[:3]:
                print(f"      - {notif.get('title')}: {notif.get('message')[:50]}...")
        else:
            print(f"   ⚠️  Notifications fetch: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # 5. Check health records
    print("\n5. Checking health records...")
    try:
        response = requests.get(
            f"{BASE_URL}/health-records",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            records = response.json()
            print(f"   ✅ Found {len(records)} health records")
            for record in records[:3]:
                print(f"      - {record.get('title')}: {record.get('record_type')}")
        else:
            print(f"   ⚠️  Health records fetch: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    print("\n" + "="*60)
    print("✅ SEEDING COMPLETE!")
    print("   - User: sharma333@test.com")
    print("   - Health records and notifications should now be visible")
    print("   - Refresh your browser at http://localhost:5174")
    print("="*60)

if __name__ == "__main__":
    seed_data()
