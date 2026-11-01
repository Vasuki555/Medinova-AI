"""
Comprehensive Sample Data Creator for MediNova AI
Creates users, appointments, medicines, health records, and more
"""

import requests
import json
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000/api/v1"

# Test users
TEST_USERS = [
    # PATIENTS
    {
        "email": "john.patient@test.com",
        "password": "Patient123!",
        "first_name": "John",
        "last_name": "Doe",
        "role": "patient",
        "phone": "+14155551234",
        "date_of_birth": "1990-05-15"
    },
    {
        "email": "sarah.patient@test.com",
        "password": "Patient123!",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "role": "patient",
        "phone": "+14155552345",
        "date_of_birth": "1985-08-22"
    },
    # DOCTORS
    {
        "email": "dr.smith@test.com",
        "password": "Doctor123!",
        "first_name": "Michael",
        "last_name": "Smith",
        "role": "doctor",
        "phone": "+14155553456"
    },
    {
        "email": "dr.williams@test.com",
        "password": "Doctor123!",
        "first_name": "Emily",
        "last_name": "Williams",
        "role": "doctor",
        "phone": "+14155554567"
    },
    # ADMIN
    {
        "email": "admin@medinova.com",
        "password": "Admin123!",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "phone": "+14155558901"
    }
]

# Sample medicines
SAMPLE_MEDICINES = [
    {
        "medicine_name": "Amoxicillin",
        "dosage": "500mg",
        "frequency": "Three times daily",
        "schedule_times": ["08:00", "14:00", "20:00"],
        "duration_days": 7,
        "instructions": "Take with food",
        "meal_timing": "after_meal",
        "current_quantity": 21,
        "refill_reminder_at": 5
    },
    {
        "medicine_name": "Metformin",
        "dosage": "850mg",
        "frequency": "Twice daily",
        "schedule_times": ["08:00", "20:00"],
        "duration_days": 30,
        "instructions": "Take with meals",
        "meal_timing": "with_meal",
        "current_quantity": 60,
        "refill_reminder_at": 10
    },
    {
        "medicine_name": "Lisinopril",
        "dosage": "10mg",
        "frequency": "Once daily",
        "schedule_times": ["09:00"],
        "duration_days": 30,
        "instructions": "Take in the morning",
        "meal_timing": "anytime",
        "current_quantity": 30,
        "refill_reminder_at": 5
    },
    {
        "medicine_name": "Vitamin D3",
        "dosage": "2000 IU",
        "frequency": "Once daily",
        "schedule_times": ["09:00"],
        "duration_days": 90,
        "instructions": "Take with breakfast",
        "meal_timing": "with_meal",
        "current_quantity": 90,
        "refill_reminder_at": 15
    },
    {
        "medicine_name": "Ibuprofen",
        "dosage": "400mg",
        "frequency": "As needed",
        "schedule_times": ["12:00"],
        "duration_days": None,
        "instructions": "Take for pain relief, max 3 times per day",
        "meal_timing": "after_meal",
        "current_quantity": 20,
        "refill_reminder_at": 5
    }
]

# Sample health records
SAMPLE_HEALTH_RECORDS = [
    {
        "record_type": "lab_report",
        "recorded_at": (datetime.utcnow() - timedelta(days=30)).isoformat(),
        "notes": "Complete Blood Count (CBC)\n\nResults show normal values across all parameters. Hemoglobin levels are within healthy range.",
        "test_results": [
            {"parameter": "Hemoglobin", "value": "14.5", "unit": "g/dL", "normal_range": "13.5-17.5", "status": "normal"},
            {"parameter": "WBC Count", "value": "7200", "unit": "/μL", "normal_range": "4000-11000", "status": "normal"},
            {"parameter": "Platelet Count", "value": "250000", "unit": "/μL", "normal_range": "150000-400000", "status": "normal"}
        ],
        "diagnosis": None,
        "source": "lab"
    },
    {
        "record_type": "vitals",
        "recorded_at": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        "notes": "Regular checkup vitals",
        "vitals": {
            "blood_pressure_systolic": 120.0,
            "blood_pressure_diastolic": 80.0,
            "heart_rate": 72,
            "temperature": 98.6,
            "oxygen_saturation": 98,
            "weight": 75.0,
            "height": 175.0
        },
        "diagnosis": None,
        "source": "self_reported"
    },
    {
        "record_type": "lab_report",
        "recorded_at": (datetime.utcnow() - timedelta(days=60)).isoformat(),
        "notes": "Lipid Panel\n\nCholesterol levels are slightly elevated. Consider dietary modifications.",
        "test_results": [
            {"parameter": "Total Cholesterol", "value": "210", "unit": "mg/dL", "normal_range": "<200", "status": "high"},
            {"parameter": "LDL Cholesterol", "value": "130", "unit": "mg/dL", "normal_range": "<100", "status": "high"},
            {"parameter": "HDL Cholesterol", "value": "45", "unit": "mg/dL", "normal_range": ">40", "status": "normal"},
            {"parameter": "Triglycerides", "value": "160", "unit": "mg/dL", "normal_range": "<150", "status": "high"}
        ],
        "diagnosis": "Borderline high cholesterol",
        "source": "lab"
    }
]

def create_users():
    """Create test users"""
    print("\n" + "=" * 60)
    print("📝 Creating Test Users...")
    print("=" * 60)
    
    created_users = {}
    
    for user_data in TEST_USERS:
        print(f"\nCreating: {user_data['first_name']} {user_data['last_name']} ({user_data['role']})")
        
        try:
            response = requests.post(
                f"{API_BASE}/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                user_id = result['user']['_id']
                created_users[user_data['email']] = {
                    'user_id': user_id,
                    'role': user_data['role'],
                    'token': result['access_token']
                }
                print(f"  ✓ Success! User ID: {user_id}")
            elif response.status_code == 400:
                error = response.json()
                if "EMAIL_EXISTS" in str(error):
                    print(f"  ⚠ User already exists - logging in...")
                    # Try to login
                    login_response = requests.post(
                        f"{API_BASE}/auth/login",
                        json={
                            "email": user_data['email'],
                            "password": user_data['password']
                        }
                    )
                    if login_response.status_code == 200:
                        result = login_response.json()
                        created_users[user_data['email']] = {
                            'user_id': result['user']['_id'],
                            'role': result['user']['role'],
                            'token': result['access_token']
                        }
                        print(f"  ✓ Logged in! User ID: {result['user']['_id']}")
                else:
                    print(f"  ✗ Failed: {error.get('detail', 'Unknown error')}")
            else:
                print(f"  ✗ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return created_users

def create_doctor_profiles(users):
    """Create doctor profiles"""
    print("\n" + "=" * 60)
    print("🩺 Creating Doctor Profiles...")
    print("=" * 60)
    
    doctors = [(email, data) for email, data in users.items() if data['role'] == 'doctor']
    
    doctor_profiles = [
        {
            "specialization": "General Practitioner",
            "qualification": "MD",
            "experience_years": 15,
            "consultation_fee": 75.0,
            "bio": "Experienced general practitioner with focus on preventive care and chronic disease management.",
            "languages": ["English", "Spanish"]
        },
        {
            "specialization": "Cardiologist",
            "qualification": "MD, FACC",
            "experience_years": 20,
            "consultation_fee": 150.0,
            "bio": "Board-certified cardiologist specializing in heart disease prevention and treatment.",
            "languages": ["English"]
        }
    ]
    
    for idx, (email, user_data) in enumerate(doctors):
        if idx >= len(doctor_profiles):
            break
            
        profile_data = doctor_profiles[idx]
        print(f"\nCreating profile for: {email}")
        
        try:
            response = requests.post(
                f"{API_BASE}/doctors/profile",
                json=profile_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {user_data['token']}"
                }
            )
            
            if response.status_code in [200, 201]:
                print(f"  ✓ Profile created successfully")
            else:
                print(f"  ⚠ Status: {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def create_appointments(users):
    """Create sample appointments"""
    print("\n" + "=" * 60)
    print("📅 Creating Sample Appointments...")
    print("=" * 60)
    
    patients = [(email, data) for email, data in users.items() if data['role'] == 'patient']
    doctors = [(email, data) for email, data in users.items() if data['role'] == 'doctor']
    
    if not patients or not doctors:
        print("  ⚠ Need both patients and doctors to create appointments")
        return
    
    # Create appointments for the first patient with different doctors
    patient_email, patient_data = patients[0]
    
    appointments = [
        {
            "doctor_id": doctors[0][1]['user_id'],
            "appointment_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
            "duration_minutes": 30,
            "type": "video",
            "reason": "Annual checkup",
            "symptoms": ["General wellness check", "Preventive screening"]
        },
        {
            "doctor_id": doctors[1][1]['user_id'] if len(doctors) > 1 else doctors[0][1]['user_id'],
            "appointment_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "duration_minutes": 45,
            "type": "in_person",
            "reason": "Follow-up consultation",
            "symptoms": ["Chest pain follow-up", "Elevated cholesterol"]
        },
        {
            "doctor_id": doctors[0][1]['user_id'],
            "appointment_date": (datetime.utcnow() - timedelta(days=10)).isoformat(),
            "duration_minutes": 30,
            "type": "video",
            "reason": "Flu symptoms",
            "symptoms": ["Fever", "Cough", "Fatigue"]
        }
    ]
    
    for idx, apt_data in enumerate(appointments):
        print(f"\nCreating appointment {idx + 1}...")
        
        try:
            response = requests.post(
                f"{API_BASE}/appointments",
                json=apt_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {patient_data['token']}"
                }
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"  ✓ Appointment created: {result.get('appointment_number')}")
            else:
                print(f"  ⚠ Status: {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def create_medicines(users):
    """Create sample medicines"""
    print("\n" + "=" * 60)
    print("💊 Creating Sample Medicines...")
    print("=" * 60)
    
    patients = [(email, data) for email, data in users.items() if data['role'] == 'patient']
    
    if not patients:
        print("  ⚠ No patients found")
        return
    
    patient_email, patient_data = patients[0]
    
    for idx, med_data in enumerate(SAMPLE_MEDICINES):
        print(f"\nCreating medicine {idx + 1}: {med_data['medicine_name']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/medications",
                json=med_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {patient_data['token']}"
                }
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"  ✓ Medicine created: {result.get('medicine_name')}")
            else:
                print(f"  ⚠ Status: {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def create_health_records(users):
    """Create sample health records"""
    print("\n" + "=" * 60)
    print("📋 Creating Sample Health Records...")
    print("=" * 60)
    
    patients = [(email, data) for email, data in users.items() if data['role'] == 'patient']
    
    if not patients:
        print("  ⚠ No patients found")
        return
    
    patient_email, patient_data = patients[0]
    
    for idx, record_data in enumerate(SAMPLE_HEALTH_RECORDS):
        print(f"\nCreating health record {idx + 1}: {record_data['record_type']}")
        
        # Add patient_id to the record
        record_data['patient_id'] = patient_data['user_id']
        
        try:
            response = requests.post(
                f"{API_BASE}/health-records",
                json=record_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {patient_data['token']}"
                }
            )
            
            if response.status_code == 201:
                print(f"  ✓ Health record created")
            else:
                print(f"  ⚠ Status: {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def print_summary():
    """Print summary of test accounts"""
    print("\n" + "=" * 80)
    print("✅ SAMPLE DATA CREATION COMPLETE!")
    print("=" * 80)
    print("\n📋 TEST ACCOUNTS")
    print("\n👤 PATIENTS:")
    print("  1. Email: john.patient@test.com     | Password: Patient123!")
    print("     - Has appointments, medicines, and health records")
    print("  2. Email: sarah.patient@test.com   | Password: Patient123!")
    print("\n🩺 DOCTORS:")
    print("  1. Email: dr.smith@test.com        | Password: Doctor123!")
    print("     - General Practitioner")
    print("  2. Email: dr.williams@test.com     | Password: Doctor123!")
    print("     - Cardiologist")
    print("\n⚙️  ADMIN:")
    print("  1. Email: admin@medinova.com       | Password: Admin123!")
    print("\n" + "=" * 80)
    print("\n📊 SAMPLE DATA INCLUDED:")
    print("  ✓ 5 Medicines (Amoxicillin, Metformin, Lisinopril, Vitamin D3, Ibuprofen)")
    print("  ✓ 3 Appointments (past, upcoming)")
    print("  ✓ 3 Health Records (CBC, Vitals, Lipid Panel)")
    print("  ✓ 2 Doctor Profiles")
    print("\n💡 TIP: Login as john.patient@test.com to see all the sample data!")
    print("=" * 80 + "\n")

def main():
    """Main function to create all sample data"""
    print("\n" + "🏥" * 30)
    print(" " * 20 + "MediNova AI")
    print(" " * 15 + "Sample Data Creator")
    print("🏥" * 30 + "\n")
    
    print("This will create:")
    print("  • 5 test user accounts (2 patients, 2 doctors, 1 admin)")
    print("  • 2 doctor profiles")
    print("  • 3 sample appointments")
    print("  • 5 medicine reminders")
    print("  • 3 health records")
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Create users first
    users = create_users()
    
    if not users:
        print("\n❌ No users created. Exiting.")
        return
    
    # Create doctor profiles
    create_doctor_profiles(users)
    
    # Create appointments
    create_appointments(users)
    
    # Create medicines
    create_medicines(users)
    
    # Create health records
    create_health_records(users)
    
    # Print summary
    print_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
