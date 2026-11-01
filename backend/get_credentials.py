"""
Get Doctor and Admin credentials from MongoDB
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def get_credentials():
    MONGODB_URL = os.getenv("MONGODB_URL")
    
    print("="*70)
    print("MEDINOVA AI - USER CREDENTIALS")
    print("="*70)
    
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.medinova_ai
        
        # Test connection
        await client.admin.command('ping')
        print("\n✅ Connected to MongoDB Atlas")
        
        # Get admin users
        print("\n" + "="*70)
        print("ADMIN ACCOUNTS:")
        print("="*70)
        
        admins = await db.users.find({"role": "admin"}).to_list(10)
        if admins:
            for admin in admins:
                print(f"\n📧 Email: {admin.get('email')}")
                print(f"   Name: {admin.get('first_name')} {admin.get('last_name')}")
                print(f"   Role: {admin.get('role')}")
                print(f"   Password: Check the password you used during registration")
                print(f"   (Common test passwords: Admin@123, admin123, Test@1234)")
        else:
            print("\n❌ No admin accounts found")
            print("   You can register a new admin at: http://localhost:5173/register")
        
        # Get doctor users
        print("\n" + "="*70)
        print("DOCTOR ACCOUNTS:")
        print("="*70)
        
        doctors = await db.users.find({"role": "doctor"}).to_list(10)
        if doctors:
            for doctor in doctors:
                print(f"\n📧 Email: {doctor.get('email')}")
                print(f"   Name: {doctor.get('first_name')} {doctor.get('last_name')}")
                print(f"   Role: {doctor.get('role')}")
                print(f"   Password: Check the password you used during registration")
                print(f"   (Common test passwords: Doctor@123, doctor123, Test@1234)")
        else:
            print("\n❌ No doctor accounts found")
            print("   You can register a new doctor at: http://localhost:5173/register")
        
        # Get patient users (for reference)
        print("\n" + "="*70)
        print("PATIENT ACCOUNTS (Sample):")
        print("="*70)
        
        patients = await db.users.find({"role": "patient"}).limit(5).to_list(5)
        if patients:
            for patient in patients:
                print(f"\n📧 Email: {patient.get('email')}")
                print(f"   Name: {patient.get('first_name')} {patient.get('last_name')}")
                print(f"   Role: {patient.get('role')}")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY:")
        print("="*70)
        admin_count = await db.users.count_documents({"role": "admin"})
        doctor_count = await db.users.count_documents({"role": "doctor"})
        patient_count = await db.users.count_documents({"role": "patient"})
        
        print(f"\n👥 Total Users: {admin_count + doctor_count + patient_count}")
        print(f"   - Admins: {admin_count}")
        print(f"   - Doctors: {doctor_count}")
        print(f"   - Patients: {patient_count}")
        
        print("\n" + "="*70)
        print("NOTE: Passwords are hashed in database for security.")
        print("Use the password you set during registration.")
        print("Common test passwords: Admin@123, Doctor@123, Test@1234")
        print("="*70)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_credentials())
