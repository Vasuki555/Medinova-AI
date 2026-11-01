#!/usr/bin/env python3
"""
Investigation for Sharma333@test.com
Check user existence, health records, and authentication flow
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from bson import ObjectId

async def investigate():
    print("=" * 80)
    print("INVESTIGATION: Sharma333@test.com")
    print("=" * 80)
    print()
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    try:
        # Step 1: Find user with exact email
        print("Step 1: Verify user account")
        print("-" * 80)
        
        user = await db.users.find_one({"email": "Sharma333@test.com"})
        
        if not user:
            print("✗ User NOT FOUND with email: Sharma333@test.com")
            print()
            print("Checking case-insensitive match...")
            user = await db.users.find_one({"email": {"$regex": "^sharma333@test\\.com$", "$options": "i"}})
            
            if user:
                print(f"✓ Found with different case: {user['email']}")
            else:
                print("✗ No match even with case-insensitive search")
                print()
                print("Checking for similar emails...")
                cursor = db.users.find({"email": {"$regex": "sharma", "$options": "i"}})
                similar = await cursor.to_list(10)
                if similar:
                    for u in similar:
                        print(f"  - {u['email']}")
                else:
                    print("  No similar emails found")
                return
        else:
            print("✓ User FOUND")
        
        user_id = user["_id"]
        print(f"  Email: {user['email']}")
        print(f"  User ID (ObjectId): {user_id}")
        print(f"  User ID (string): {str(user_id)}")
        print(f"  Role: {user.get('role')}")
        print(f"  Full Name: {user.get('full_name', 'N/A')}")
        print(f"  Created: {user.get('created_at', 'N/A')}")
        print()
        
        # Step 2: Check health records
        print("Step 2: Check health records for this user")
        print("-" * 80)
        
        # Try both ObjectId and string formats
        records_by_objectid = await db.health_records.find({"patient_id": user_id}).to_list(100)
        records_by_string = await db.health_records.find({"patient_id": str(user_id)}).to_list(100)
        
        print(f"Records with patient_id as ObjectId: {len(records_by_objectid)}")
        print(f"Records with patient_id as string: {len(records_by_string)}")
        print()
        
        all_records = records_by_objectid + records_by_string
        
        if all_records:
            print(f"Total records found: {len(all_records)}")
            for idx, rec in enumerate(all_records[:3], 1):
                print(f"\nRecord #{idx}:")
                print(f"  _id: {rec['_id']}")
                print(f"  patient_id: {rec.get('patient_id')} (type: {type(rec.get('patient_id')).__name__})")
                print(f"  record_type: {rec.get('record_type')}")
                print(f"  source: {rec.get('source')}")
                print(f"  recorded_by: {rec.get('recorded_by', 'MISSING')}")
                print(f"  created_at: {rec.get('created_at')}")
        else:
            print("✓ No records found (expected for new user)")
        print()
        
        # Step 3: Check authentication flow
        print("Step 3: Simulate authentication flows")
        print("-" * 80)
        
        # Simulate get_current_user (used by /health-records)
        print("A. GET /health-records authentication:")
        print("   Uses: get_current_user() dependency")
        print("   Query: db.users.find_one({'_id': ObjectId(user_id)})")
        
        # Try lookup with ObjectId
        auth_user = await db.users.find_one({"_id": user_id})
        if auth_user:
            print(f"   Result: ✓ User FOUND")
            print(f"   Returned: {auth_user['email']}")
        else:
            print(f"   Result: ✗ User NOT FOUND")
        print()
        
        # Simulate /me endpoint (if it exists)
        print("B. GET /me authentication (if different):")
        print("   May use different lookup logic")
        
        # Check if there's any difference in stored vs. queried ID format
        print()
        print("C. ID Format Check:")
        print(f"   Stored _id type: {type(user['_id'])}")
        print(f"   Stored _id value: {user['_id']}")
        
        # Try string conversion
        try:
            from_string = ObjectId(str(user_id))
            print(f"   Roundtrip ObjectId(str(id)): {from_string}")
            print(f"   Equals original: {from_string == user_id}")
        except Exception as e:
            print(f"   Conversion error: {e}")
        print()
        
        # Step 4: Check what service returns
        print("Step 4: Test HealthRecordService.get_patient_records()")
        print("-" * 80)
        
        from app.services.health_record_service import HealthRecordService
        service = HealthRecordService(db)
        
        try:
            # This is what GET /health-records calls
            records = await service.get_patient_records(str(user_id))
            print(f"✓ Service returned {len(records)} records")
            if records:
                print(f"  First record ID: {records[0].get('id')}")
        except Exception as e:
            print(f"✗ Service failed: {type(e).__name__}: {e}")
        print()
        
        # Step 5: Database connection info
        print("Step 5: Database connection details")
        print("-" * 80)
        print(f"MongoDB URL: {settings.MONGODB_URL[:50]}...")
        print(f"Database Name: {settings.MONGODB_DB_NAME}")
        print(f"Collections:")
        collections = await db.list_collection_names()
        print(f"  - users: {'✓' if 'users' in collections else '✗'}")
        print(f"  - health_records: {'✓' if 'health_records' in collections else '✗'}")
        print()
        
        # Step 6: Check for patient_id type mismatch
        print("Step 6: Check for patient_id type inconsistency")
        print("-" * 80)
        
        all_patient_ids = await db.health_records.distinct("patient_id")
        print(f"Unique patient_id values in health_records: {len(all_patient_ids)}")
        
        objectid_count = sum(1 for pid in all_patient_ids if isinstance(pid, ObjectId))
        string_count = sum(1 for pid in all_patient_ids if isinstance(pid, str))
        
        print(f"  ObjectId format: {objectid_count}")
        print(f"  String format: {string_count}")
        print()
        
        if string_count > 0:
            print("⚠️  WARNING: Some records use STRING patient_id")
            print("   This may cause query mismatches!")
        
    finally:
        client.close()
        print("=" * 80)

if __name__ == "__main__":
    asyncio.run(investigate())
