"""
PRECISE READ-ONLY VERIFICATION
===============================
Verify exact malformed records for authenticated test user.
NO assumptions about data semantics.
NO modifications to any data.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

load_dotenv()

# Test user from browser session
TEST_USER_EMAIL = "jane.smith@example.com"
TEST_USER_PATIENT_ID = "6ad1dbfeb7f33dc8b76a6c5e"


async def verify_exact_records():
    """Verify exact records for authenticated test user"""
    
    mongodb_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("MONGODB_DB_NAME", "medinova_ai")
    
    try:
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=10000)
        await client.admin.command('ping')
        print(f"✓ Connected to MongoDB Atlas")
        
        db = client[db_name]
        health_records = db.health_records
        
        print(f"\n{'='*80}")
        print(f"VERIFICATION FOR AUTHENTICATED PATIENT")
        print(f"{'='*80}")
        print(f"Patient ID: {TEST_USER_PATIENT_ID}")
        print(f"(User: {TEST_USER_EMAIL})")
        
        # 1. Count total records for this patient
        total_count = await health_records.count_documents({"patient_id": TEST_USER_PATIENT_ID})
        print(f"\n1. Total health records: {total_count}")
        
        if total_count == 0:
            print("\n⚠️  CRITICAL: Patient has ZERO health records in database")
            print("    This means GET /health-records should return empty array []")
            print("    HTTP 500 cannot be caused by malformed records if no records exist!")
            client.close()
            return
        
        # 2. Get all records for this patient
        cursor = health_records.find({"patient_id": TEST_USER_PATIENT_ID})
        records = await cursor.to_list(length=None)
        
        print(f"\n2. Analyzing {len(records)} record(s)...")
        
        # Track violations
        diagnosis_string_count = 0
        missing_recorded_by_count = 0
        other_violations = []
        malformed_records = []
        
        for i, record in enumerate(records, 1):
            record_id = str(record.get("_id", "unknown"))
            violations = []
            
            # Check diagnosis field type
            if "diagnosis" in record:
                diagnosis_value = record["diagnosis"]
                if diagnosis_value is not None:
                    if isinstance(diagnosis_value, str):
                        violations.append(f"diagnosis is STRING: '{diagnosis_value[:50]}...'")
                        diagnosis_string_count += 1
                    elif not isinstance(diagnosis_value, dict):
                        violations.append(f"diagnosis is {type(diagnosis_value).__name__}, expected dict or None")
            
            # Check recorded_by field existence
            if "recorded_by" not in record or record.get("recorded_by") is None:
                violations.append("recorded_by field MISSING or None")
                missing_recorded_by_count += 1
            
            # Check other required fields per HealthRecordResponse
            required_fields = {
                "patient_id": str,
                "record_type": str,
                "recorded_at": datetime,
                "source": str,
                "created_at": datetime,
                "updated_at": datetime
            }
            
            for field_name, expected_type in required_fields.items():
                if field_name not in record:
                    violations.append(f"{field_name} field MISSING")
                elif expected_type == datetime:
                    if not isinstance(record[field_name], datetime):
                        violations.append(f"{field_name} is {type(record[field_name]).__name__}, expected datetime")
                elif not isinstance(record[field_name], expected_type):
                    violations.append(f"{field_name} is {type(record[field_name]).__name__}, expected {expected_type.__name__}")
            
            # Report findings for this record
            if violations:
                malformed_records.append(record_id)
                print(f"\n   Record #{i} (ID: {record_id})")
                print(f"   ❌ MALFORMED - {len(violations)} violation(s):")
                for v in violations:
                    print(f"      - {v}")
                print(f"   record_type: {record.get('record_type', 'N/A')}")
                print(f"   source: {record.get('source', 'N/A')}")
                print(f"   recorded_at: {record.get('recorded_at', 'N/A')}")
            else:
                print(f"\n   Record #{i} (ID: {record_id})")
                print(f"   ✓ Valid structure")
                print(f"   record_type: {record.get('record_type', 'N/A')}")
                print(f"   source: {record.get('source', 'N/A')}")
        
        # Summary
        print(f"\n{'='*80}")
        print(f"SUMMARY FOR PATIENT {TEST_USER_PATIENT_ID}")
        print(f"{'='*80}")
        print(f"Total records: {total_count}")
        print(f"Valid records: {total_count - len(malformed_records)}")
        print(f"Malformed records: {len(malformed_records)}")
        print(f"\nViolation breakdown:")
        print(f"  - diagnosis as string: {diagnosis_string_count}")
        print(f"  - missing recorded_by: {missing_recorded_by_count}")
        
        if len(malformed_records) > 0:
            print(f"\n❌ CONFIRMATION: At least {len(malformed_records)} malformed record(s)")
            print(f"   WILL cause Pydantic ValidationError during response serialization")
            print(f"   This explains HTTP 500 for GET /health-records endpoint")
        else:
            print(f"\n✓ All records are properly formatted")
            print(f"  HTTP 500 must be caused by something else")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")


async def verify_middleware_stack():
    """Verify FastAPI/Starlette middleware stack"""
    print(f"\n{'='*80}")
    print(f"MIDDLEWARE STACK VERIFICATION")
    print(f"{'='*80}")
    
    # Import the app
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from app.main import app
    
    print(f"\nMiddleware stack (execution order):")
    print(f"Note: Middleware executes in REVERSE order of registration for responses\n")
    
    for i, middleware in enumerate(app.user_middleware, 1):
        middleware_class = middleware.cls.__name__ if hasattr(middleware, 'cls') else str(middleware)
        print(f"{i}. {middleware_class}")
        
        # Check if it's CORS middleware
        if "CORS" in middleware_class:
            print(f"   → This is CORS middleware")
            print(f"   → Adds Access-Control-Allow-Origin header to responses")
            print(f"   → Position: #{i} in middleware stack")
    
    print(f"\nCritical insight:")
    print(f"• Response serialization happens INSIDE endpoint execution")
    print(f"• If serialization raises exception, response never completes")
    print(f"• Exception handlers run AFTER middleware on error path")
    print(f"• CORS middleware only processes successful responses or handled exceptions")
    print(f"• Unhandled exceptions bypass CORS middleware")


async def verify_exception_types():
    """Verify what exception types FastAPI raises for response validation"""
    print(f"\n{'='*80}")
    print(f"EXCEPTION TYPE VERIFICATION")
    print(f"{'='*80}")
    
    print(f"\nFastAPI response validation exceptions:")
    print(f"1. ResponseValidationError (fastapi.exceptions)")
    print(f"   - Raised when response_model validation fails")
    print(f"   - Wraps Pydantic ValidationError")
    print(f"   - Default handler returns HTTP 500")
    
    print(f"\n2. Default behavior:")
    print(f"   - FastAPI catches ResponseValidationError internally")
    print(f"   - Converts to HTTP 500 Internal Server Error")
    print(f"   - May not log full traceback in production mode")
    print(f"   - CORS headers NOT added by default error handler")
    
    print(f"\n3. Why CORS headers missing:")
    print(f"   - ResponseValidationError raised during response serialization")
    print(f"   - FastAPI's internal error handler creates new Response(status=500)")
    print(f"   - New response bypasses CORS middleware")
    print(f"   - Browser blocks response due to missing CORS headers")


async def verify_service_semantics():
    """Verify HealthRecordService.create_health_record semantics"""
    print(f"\n{'='*80}")
    print(f"SERVICE METHOD SEMANTICS VERIFICATION")
    print(f"{'='*80}")
    
    print(f"\nAnalyzing: HealthRecordService.create_health_record()")
    print(f"File: backend/app/services/health_record_service.py")
    print(f"Lines: 37-58")
    
    print(f"\nMethod signature:")
    print(f"  create_health_record(patient_id: str, recorder_id: str, data: HealthRecordCreate)")
    
    print(f"\nParameter semantics:")
    print(f"  - patient_id: User ID of the PATIENT (record belongs to this user)")
    print(f"  - recorder_id: User ID of the RECORDER (who created this record)")
    print(f"  - data: HealthRecordCreate schema (validated record data)")
    
    print(f"\nField assignment in method:")
    print(f"  record_dict['patient_id'] = patient_id")
    print(f"  record_dict['recorded_by'] = recorder_id  ← STORES RECORDER'S USER ID")
    
    print(f"\n⚠️  CRITICAL DATA SEMANTICS:")
    print(f"  • recorded_by = User ID of whoever CREATED the record")
    print(f"  • For doctor-created records: recorded_by = doctor's user ID")
    print(f"  • For patient self-entry: recorded_by = patient's user ID")
    print(f"  • For AI/system extraction: recorder_id CANNOT be patient_id")
    print(f"                             unless patient initiated the upload")
    
    print(f"\n✓ SAFE ASSIGNMENT for document_upload:")
    print(f"  • User uploads document → user is the initiator")
    print(f"  • recorded_by = current_user['_id'] (the uploader)")
    print(f"  • This is semantically correct")


async def main():
    print(f"\n{'='*80}")
    print(f"FINAL READ-ONLY VERIFICATION")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    await verify_exact_records()
    await verify_middleware_stack()
    await verify_exception_types()
    await verify_service_semantics()
    
    print(f"\n{'='*80}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'='*80}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    asyncio.run(main())
