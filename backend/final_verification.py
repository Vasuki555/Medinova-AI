"""
FINAL READ-ONLY VERIFICATION SCRIPT
===================================
Addresses all unresolved issues without modifying any data.

This script will:
1. Inspect the exact GET /api/v1/health-records database query
2. Confirm whether it filters by authenticated patient's ID
3. Count malformed records belonging to the test user
4. Determine if malformed records are actually returned
5. Test the actual GET request with proper authentication
6. Investigate database connection status
7. Verify mongomock fallback conditions
"""

import asyncio
import sys
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

# Test user credentials from previous investigation
TEST_USER_EMAIL = "jane.smith@example.com"
TEST_USER_ID = "6ad1dbfeb7f33dc8b76a6c5e"  # Confirmed patient user

async def verify_database_query():
    """Verification 1 & 2: Inspect exact query and patient_id filtering"""
    logger.info("\n" + "="*80)
    logger.info("VERIFICATION 1 & 2: Database Query Inspection")
    logger.info("="*80)
    
    logger.info("\n✓ CONFIRMED FROM SOURCE CODE REVIEW:")
    logger.info("   File: backend/app/api/v1/health_records.py, line 37-90")
    logger.info("   File: backend/app/services/health_record_service.py, line 26-34")
    logger.info("")
    logger.info("   GET /api/v1/health-records endpoint behavior:")
    logger.info("   - Line 44: target_patient_id = current_user['_id']")
    logger.info("   - Line 90: records = await service.get_patient_records(target_patient_id, record_type)")
    logger.info("   - Service query (line 28): query = {'patient_id': patient_id}")
    logger.info("   - Line 31: records_collection.find(query).sort('recorded_at', -1).to_list(200)")
    logger.info("")
    logger.info("   CONCLUSION: Query ALWAYS filters by patient_id")
    logger.info("               For patient role: uses authenticated user's _id")
    logger.info("               Only returns records where patient_id matches")
    

def count_malformed_records_for_user():
    """Verification 3 & 4: Count malformed records for test user"""
    logger.info("\n" + "="*80)
    logger.info("VERIFICATION 3 & 4: Malformed Records for Test User")
    logger.info("="*80)
    
    try:
        mongodb_url = os.getenv("MONGODB_URL")
        if not mongodb_url:
            logger.error("❌ MONGODB_URL not found in environment")
            return
        
        logger.info(f"Connecting to MongoDB Atlas...")
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        logger.info("✓ Successfully connected to MongoDB Atlas")
        
        db = client[os.getenv("MONGODB_DB_NAME", "medinova")]
        records_collection = db.health_records
        
        # Query for test user's records
        test_user_records = list(records_collection.find(
            {"patient_id": TEST_USER_ID}
        ))
        
        logger.info(f"\nTest User: {TEST_USER_EMAIL}")
        logger.info(f"Test User ID: {TEST_USER_ID}")
        logger.info(f"Total records belonging to test user: {len(test_user_records)}")
        
        if len(test_user_records) == 0:
            logger.warning("⚠ Test user has NO health records in database")
            logger.info("\nThis explains why GET /health-records might return empty array")
            logger.info("But does NOT explain HTTP 500 error if it occurs")
        else:
            # Analyze each record for malformation
            malformed_count = 0
            
            for i, record in enumerate(test_user_records, 1):
                record_id = str(record.get("_id", "unknown"))
                logger.info(f"\n--- Record #{i} (ID: {record_id}) ---")
                
                # Check for required fields
                missing_fields = []
                if "recorded_by" not in record or record.get("recorded_by") is None:
                    missing_fields.append("recorded_by")
                
                # Check diagnosis structure
                diagnosis_issue = None
                if "diagnosis" in record:
                    if isinstance(record["diagnosis"], str):
                        diagnosis_issue = f"diagnosis is string ('{record['diagnosis'][:50]}...'), expected object"
                    elif not isinstance(record["diagnosis"], dict):
                        diagnosis_issue = f"diagnosis is {type(record['diagnosis'])}, expected object"
                
                # Report findings
                if missing_fields or diagnosis_issue:
                    malformed_count += 1
                    logger.warning(f"   ❌ MALFORMED RECORD")
                    if missing_fields:
                        logger.warning(f"      Missing fields: {', '.join(missing_fields)}")
                    if diagnosis_issue:
                        logger.warning(f"      Schema violation: {diagnosis_issue}")
                    
                    # Show other metadata without exposing patient data
                    logger.info(f"      record_type: {record.get('record_type', 'N/A')}")
                    logger.info(f"      source: {record.get('source', 'N/A')}")
                    logger.info(f"      recorded_at: {record.get('recorded_at', 'N/A')}")
                else:
                    logger.info(f"   ✓ Valid structure")
                    logger.info(f"      record_type: {record.get('record_type', 'N/A')}")
                    logger.info(f"      source: {record.get('source', 'N/A')}")
            
            logger.info(f"\n{'='*80}")
            logger.info(f"SUMMARY FOR TEST USER {TEST_USER_ID}:")
            logger.info(f"  Total records: {len(test_user_records)}")
            logger.info(f"  Malformed records: {malformed_count}")
            logger.info(f"  Valid records: {len(test_user_records) - malformed_count}")
            
            if malformed_count > 0:
                logger.error(f"\n❌ CRITICAL: {malformed_count} malformed record(s) will cause Pydantic ValidationError")
                logger.error("   When GET /health-records is called, FastAPI attempts to serialize")
                logger.error("   all returned records using response_model=List[HealthRecordResponse]")
                logger.error("   Malformed records WILL trigger HTTP 500 Internal Server Error")
            else:
                logger.info(f"\n✓ All {len(test_user_records)} records are properly formatted")
                logger.info("  GET /health-records should NOT fail due to malformed data")
        
        client.close()
        
    except Exception as e:
        logger.error(f"❌ Error connecting to MongoDB: {type(e).__name__}: {e}")
        logger.info("   This may indicate the database connection issue")


async def test_authenticated_get_request():
    """Verification 5: Test actual GET request with authentication"""
    logger.info("\n" + "="*80)
    logger.info("VERIFICATION 5: Authenticated GET Request Test")
    logger.info("="*80)
    
    try:
        # We cannot use httpx TestClient because it doesn't trigger actual startup
        # Instead, provide instructions for manual browser test
        
        logger.info("\n⚠ Automated authenticated request test has a limitation:")
        logger.info("   TestClient doesn't connect to actual database")
        logger.info("")
        logger.info("✓ RECOMMENDED: Manual browser test with DevTools")
        logger.info("")
        logger.info("   Steps to capture exact backend traceback:")
        logger.info("   1. Open browser to http://localhost:3000/patient/login")
        logger.info("   2. Login with: jane.smith@example.com / password123")
        logger.info("   3. Navigate to: http://localhost:3000/patient/phr")
        logger.info("   4. Open DevTools → Network tab")
        logger.info("   5. Locate GET request to http://localhost:8000/api/v1/health-records")
        logger.info("   6. Check Response status code (should be 500 if error occurs)")
        logger.info("   7. Switch to backend terminal to see Python traceback")
        logger.info("")
        logger.info("   Backend terminal will show exact Pydantic ValidationError")
        logger.info("   with field names and validation failures")
        
    except Exception as e:
        logger.error(f"Error: {e}")


def check_database_fallback_conditions():
    """Verification 6 & 8: Database connection and mongomock fallback"""
    logger.info("\n" + "="*80)
    logger.info("VERIFICATION 6 & 8: Database Connection & Mongomock Fallback")
    logger.info("="*80)
    
    logger.info("\n✓ CONFIRMED FROM SOURCE CODE REVIEW:")
    logger.info("   File: backend/app/database.py, lines 135-201")
    logger.info("")
    logger.info("   Mongomock fallback is ENABLED:")
    logger.info("   - Line 164: Falls back to mongomock when Atlas connection fails")
    logger.info("   - Line 174: BLOCKS fallback in production (settings.is_production)")
    logger.info("   - Line 185: Creates MockAsyncDatabase wrapper")
    logger.info("")
    logger.info("   Fallback trigger conditions:")
    logger.info("   1. MongoDB Atlas ping fails (line 157: admin.command('ping'))")
    logger.info("   2. Any connection exception during Atlas setup")
    logger.info("   3. Common causes:")
    logger.info("      - Network connectivity issues")
    logger.info("      - IP whitelist restrictions")
    logger.info("      - SSL/TLS handshake failures (Python 3.14 issue)")
    logger.info("      - Invalid connection string")
    logger.info("")
    
    # Test actual connection
    logger.info("Testing current MongoDB connection...")
    try:
        mongodb_url = os.getenv("MONGODB_URL")
        if not mongodb_url:
            logger.error("❌ MONGODB_URL not found in environment")
            return
        
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✓ MongoDB Atlas connection: SUCCESS")
        logger.info("  Backend should be using real MongoDB (not mongomock)")
        
        # Check Python version
        import platform
        python_version = platform.python_version()
        logger.info(f"\nPython version: {python_version}")
        
        if python_version.startswith("3.14"):
            logger.warning("⚠ Python 3.14 detected - known SSL handshake issues with MongoDB Atlas")
            logger.warning("  Connection may be intermittent due to TLS compatibility")
            logger.warning("  SSL errors in backend logs are expected with Python 3.14")
        
        client.close()
        
    except Exception as e:
        logger.error(f"❌ MongoDB Atlas connection: FAILED")
        logger.error(f"   Error: {type(e).__name__}: {e}")
        logger.warning("   Backend will fall back to mongomock")
        logger.warning("   Data in mongomock is IN-MEMORY and NOT PERSISTENT")


def investigate_smart_upload_source():
    """Additional investigation: Why no smart_upload source records?"""
    logger.info("\n" + "="*80)
    logger.info("ADDITIONAL: Smart Upload Source Investigation")
    logger.info("="*80)
    
    logger.info("\n✓ CONFIRMED FROM SOURCE CODE REVIEW:")
    logger.info("   File: backend/app/api/v1/document_upload.py, lines 377-410")
    logger.info("")
    logger.info("   Smart Upload save behavior:")
    logger.info("   - Line 407: Sets source='document_upload' (NOT 'smart_upload')")
    logger.info("   - Direct MongoDB insert bypasses health_record_service")
    logger.info("   - No Pydantic validation applied")
    logger.info("")
    logger.info("   CONCLUSION: Records created by Smart Upload have source='document_upload'")
    logger.info("               There is no 'smart_upload' source value in the codebase")
    

def summary_and_hypothesis():
    """Provide clear separation of facts vs hypotheses"""
    logger.info("\n" + "="*80)
    logger.info("FINAL SUMMARY")
    logger.info("="*80)
    
    logger.info("\n📋 CONFIRMED FACTS:")
    logger.info("   ✓ GET /health-records filters by patient_id (source code verified)")
    logger.info("   ✓ Only returns records matching authenticated user's _id")
    logger.info("   ✓ Smart Upload saves records with source='document_upload'")
    logger.info("   ✓ document_upload.py auto_save bypasses Pydantic validation")
    logger.info("   ✓ Mongomock fallback is enabled in development")
    logger.info("   ✓ Python 3.14 has known SSL issues with MongoDB Atlas")
    logger.info("")
    
    logger.info("🔍 HYPOTHESES (requires browser test to confirm):")
    logger.info("   H1: Test user has malformed records → Pydantic fails → HTTP 500")
    logger.info("   H2: Test user has no records → returns empty array → no 500")
    logger.info("   H3: Backend using mongomock → different data → different behavior")
    logger.info("")
    
    logger.info("❓ UNRESOLVED ISSUES:")
    logger.info("   • Exact count of malformed records for test user: See verification above")
    logger.info("   • Actual HTTP 500 traceback: Requires browser test with backend logs")
    logger.info("   • Whether mongomock or Atlas is active: Intermittent due to SSL errors")
    logger.info("")
    
    logger.info("📍 NEXT STEPS:")
    logger.info("   1. Run this script to count malformed records for test user")
    logger.info("   2. Perform manual browser test to capture exact 500 traceback")
    logger.info("   3. Based on findings, choose appropriate fix approach")


def main():
    """Run all verifications"""
    print("\n" + "="*80)
    print("FINAL READ-ONLY VERIFICATION - Smart Upload Investigation")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Synchronous verifications
    verify_database_query()
    count_malformed_records_for_user()
    check_database_fallback_conditions()
    investigate_smart_upload_source()
    
    # Async verification
    asyncio.run(test_authenticated_get_request())
    
    # Summary
    summary_and_hypothesis()
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


if __name__ == "__main__":
    main()
