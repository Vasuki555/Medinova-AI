"""
Seed sample doctors into MongoDB Atlas
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Sample doctors with various specializations
sample_doctors = [
    {
        "email": "dr.john.cardiologist@medinova.com",
        "password": "Doctor@123",
        "first_name": "John",
        "last_name": "Anderson",
        "phone": "+1234567001",
        "date_of_birth": "1980-03-15",
        "role": "doctor",
        "specialization": "Cardiologist",
        "license_number": "CARD001",
        "years_of_experience": 15,
        "qualification": "MBBS, MD (Cardiology)",
        "consultation_fee": 150.0,
        "hospital_affiliation": "City Heart Hospital",
        "bio": "Experienced cardiologist specializing in heart disease prevention and treatment."
    },
    {
        "email": "dr.sarah.neurologist@medinova.com",
        "password": "Doctor@123",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "phone": "+1234567002",
        "date_of_birth": "1982-07-20",
        "role": "doctor",
        "specialization": "Neurologist",
        "license_number": "NEUR001",
        "years_of_experience": 12,
        "qualification": "MBBS, MD (Neurology)",
        "consultation_fee": 140.0,
        "hospital_affiliation": "Brain & Spine Institute",
        "bio": "Specialist in neurological disorders, migraines, and brain health."
    },
    {
        "email": "dr.michael.dermatologist@medinova.com",
        "password": "Doctor@123",
        "first_name": "Michael",
        "last_name": "Brown",
        "phone": "+1234567003",
        "date_of_birth": "1985-05-10",
        "role": "doctor",
        "specialization": "Dermatologist",
        "license_number": "DERM001",
        "years_of_experience": 8,
        "qualification": "MBBS, MD (Dermatology)",
        "consultation_fee": 120.0,
        "hospital_affiliation": "Skin Care Center",
        "bio": "Expert in skin conditions, acne treatment, and cosmetic dermatology."
    },
    {
        "email": "dr.emily.pediatrician@medinova.com",
        "password": "Doctor@123",
        "first_name": "Emily",
        "last_name": "Davis",
        "phone": "+1234567004",
        "date_of_birth": "1983-09-25",
        "role": "doctor",
        "specialization": "Pediatrician",
        "license_number": "PEDI001",
        "years_of_experience": 10,
        "qualification": "MBBS, MD (Pediatrics)",
        "consultation_fee": 110.0,
        "hospital_affiliation": "Children's Hospital",
        "bio": "Pediatrician specialized in child health, vaccinations, and development."
    },
    {
        "email": "dr.robert.orthopedic@medinova.com",
        "password": "Doctor@123",
        "first_name": "Robert",
        "last_name": "Wilson",
        "phone": "+1234567005",
        "date_of_birth": "1978-11-30",
        "role": "doctor",
        "specialization": "Orthopedic",
        "license_number": "ORTH001",
        "years_of_experience": 18,
        "qualification": "MBBS, MS (Orthopedics)",
        "consultation_fee": 160.0,
        "hospital_affiliation": "Bone & Joint Clinic",
        "bio": "Orthopedic surgeon specializing in joint replacement and sports injuries."
    },
    {
        "email": "dr.lisa.general@medinova.com",
        "password": "Doctor@123",
        "first_name": "Lisa",
        "last_name": "Martinez",
        "phone": "+1234567006",
        "date_of_birth": "1986-04-18",
        "role": "doctor",
        "specialization": "General Practitioner",
        "license_number": "GP001",
        "years_of_experience": 7,
        "qualification": "MBBS",
        "consultation_fee": 80.0,
        "hospital_affiliation": "Community Health Center",
        "bio": "General practitioner providing comprehensive primary care services."
    },
    {
        "email": "dr.james.psychiatrist@medinova.com",
        "password": "Doctor@123",
        "first_name": "James",
        "last_name": "Taylor",
        "phone": "+1234567007",
        "date_of_birth": "1981-08-12",
        "role": "doctor",
        "specialization": "Psychiatrist",
        "license_number": "PSY001",
        "years_of_experience": 14,
        "qualification": "MBBS, MD (Psychiatry)",
        "consultation_fee": 130.0,
        "hospital_affiliation": "Mental Health Institute",
        "bio": "Psychiatrist specializing in mental health, depression, and anxiety disorders."
    },
    {
        "email": "dr.maria.gynecologist@medinova.com",
        "password": "Doctor@123",
        "first_name": "Maria",
        "last_name": "Garcia",
        "phone": "+1234567008",
        "date_of_birth": "1984-06-22",
        "role": "doctor",
        "specialization": "Gynecologist",
        "license_number": "GYNE001",
        "years_of_experience": 11,
        "qualification": "MBBS, MD (OB/GYN)",
        "consultation_fee": 125.0,
        "hospital_affiliation": "Women's Health Center",
        "bio": "Gynecologist providing women's healthcare and maternity services."
    },
    {
        "email": "dr.david.ent@medinova.com",
        "password": "Doctor@123",
        "first_name": "David",
        "last_name": "Lee",
        "phone": "+1234567009",
        "date_of_birth": "1979-12-05",
        "role": "doctor",
        "specialization": "ENT Specialist",
        "license_number": "ENT001",
        "years_of_experience": 16,
        "qualification": "MBBS, MS (ENT)",
        "consultation_fee": 135.0,
        "hospital_affiliation": "Ear, Nose & Throat Clinic",
        "bio": "ENT specialist treating ear, nose, throat, and sinus conditions."
    },
    {
        "email": "dr.anna.ophthalmologist@medinova.com",
        "password": "Doctor@123",
        "first_name": "Anna",
        "last_name": "White",
        "phone": "+1234567010",
        "date_of_birth": "1987-02-14",
        "role": "doctor",
        "specialization": "Ophthalmologist",
        "license_number": "OPHT001",
        "years_of_experience": 9,
        "qualification": "MBBS, MS (Ophthalmology)",
        "consultation_fee": 115.0,
        "hospital_affiliation": "Eye Care Center",
        "bio": "Ophthalmologist specializing in eye health, cataract surgery, and vision care."
    }
]

print("🚀 Seeding sample doctors into MongoDB Atlas...\n")
print("=" * 70)

success_count = 0
skip_count = 0
error_count = 0

for doctor in sample_doctors:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=doctor,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"✅ {doctor['first_name']} {doctor['last_name']} - {doctor['specialization']}")
            success_count += 1
        elif response.status_code == 400 and "already registered" in response.text.lower():
            print(f"⚠️  {doctor['first_name']} {doctor['last_name']} - Already exists")
            skip_count += 1
        else:
            print(f"❌ {doctor['first_name']} {doctor['last_name']} - Error: {response.status_code}")
            error_count += 1
    except Exception as e:
        print(f"❌ {doctor['first_name']} {doctor['last_name']} - Exception: {str(e)[:50]}")
        error_count += 1

print("=" * 70)
print(f"\n📊 Summary:")
print(f"   ✅ Successfully created: {success_count}")
print(f"   ⚠️  Already existed: {skip_count}")
print(f"   ❌ Errors: {error_count}")
print(f"   📝 Total doctors: {success_count + skip_count}")

print("\n🎉 Doctor seeding complete!")
print("\n💡 Tip: These doctors are now available for appointment booking")
print("   You can login with any doctor account using:")
print("   Password: Doctor@123")
