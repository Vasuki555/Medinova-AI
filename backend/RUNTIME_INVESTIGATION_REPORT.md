# RUNTIME INVESTIGATION REPORT: HTTP 500 Error Analysis
**Date:** 2026-10-31  
**Issue:** GET `/api/v1/health-records` returns HTTP 500 without CORS headers  
**Status:** READ-ONLY INVESTIGATION COMPLETE

---

## EXECUTIVE SUMMARY

**ROOT CAUSE IDENTIFIED:**  
Pydantic `ValidationError` during FastAPI response serialization, occurring **AFTER** endpoint execution but **BEFORE** CORS middleware can add headers.

**WHY HTTP 500 HAS NO CORS HEADERS:**  
FastAPI's exception handling for `ValidationError` during response serialization bypasses CORS middleware, resulting in browser blocking the error response.

**WHY NO BACKEND TRACEBACK:**  
ValidationErrors during response model serialization are handled by FastAPI's internal error handling and may not trigger standard Python exception logging at the application level, especially if the error occurs in Pydantic's C-optimized validation code.

---

## CONFIRMED FACTS

### 1. Route Configuration
**File:** `backend/app/api/v1/health_records.py`  
**Line 36:** 
```python
@router.get("", response_model=List[HealthRecordResponse])
async def list_records(...)
```

**Dependency Chain:**
1. `get_current_user` → `security` (HTTP Bearer) → `verify_token` → `AuthService.get_current_user`
2. `get_database` → `Database.get_database()` → Returns active MongoDB connection
3. Line 90: `records = await service.get_patient_records(target_patient_id, record_type)`

### 2. Database Query Filtering
**File:** `backend/app/services/health_record_service.py`  
**Lines 26-34:**
```python
async def get_patient_records(self, patient_id: str, record_type: Optional[str] = None) -> List[Dict[str, Any]]:
    query = {"patient_id": patient_id}
    if record_type:
        query["record_type"] = record_type
        
    records = await self.records_collection.find(query).sort("recorded_at", -1).to_list(200)
    for record in records:
        record["id"] = str(record["_id"])
    return records
```

✅ **CONFIRMED:** Query filters by authenticated user's patient_id  
✅ **CONFIRMED:** Returns raw MongoDB documents as Python dicts

### 3. Response Model Schema Requirements
**File:** `backend/app/schemas/health_record.py`  
**Lines 22-36:**
```python
class HealthRecordResponse(BaseModel):
    id: str
    patient_id: str
    record_type: str
    recorded_at: datetime
    vitals: Optional[VitalSigns] = None
    lab_test: Optional[LabTestDetails] = None
    diagnosis: Optional[DiagnosisDetails] = None  # ← MUST BE OBJECT OR None
    note: Optional[GeneralNoteDetails] = None
    recorded_by: str  # ← REQUIRED FIELD
    source: str
    device_name: Optional[str] = None
    appointment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
```

**File:** `backend/app/models/health_record.py`  
**Lines 30-35:**
```python
class DiagnosisDetails(BaseModel):
    condition: str
    icd10_code: Optional[str] = None
    diagnosed_by: Optional[str] = None
    severity: str = "moderate"
    notes: Optional[str] = None
```

✅ **CONFIRMED:** `diagnosis` field expects `DiagnosisDetails` object (dict) or `None`  
✅ **CONFIRMED:** String values will trigger `ValidationError`  
✅ **CONFIRMED:** `recorded_by` field is **REQUIRED** (not Optional)

### 4. Malformed Record Source
**File:** `backend/app/api/v1/document_upload.py`  
**Lines 377-410:**
```python
# Direct MongoDB insert - BYPASSES Pydantic validation
health_record = {
    "patient_id": current_user["_id"],
    "record_type": extracted_data.get("record_type", "consultation_notes"),
    "recorded_at": datetime.utcnow(),
    "diagnosis": extracted_data.get("diagnosis"),  # ← May be STRING from AI extraction
    "source": "document_upload",
    # recorded_by field MISSING
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

result = await db.health_records.insert_one(health_record)
```

❌ **CONFIRMED:** Direct DB insert bypasses all Pydantic validation  
❌ **CONFIRMED:** `diagnosis` can be inserted as string  
❌ **CONFIRMED:** `recorded_by` field is omitted entirely

### 5. CORS Middleware Configuration
**File:** `backend/app/main.py`  
**Lines 67-74:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Includes localhost:5173
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

✅ **CONFIRMED:** CORS middleware is configured correctly  
✅ **CONFIRMED:** Middleware is added to app before route registration  
✅ **CONFIRMED:** Origin `http://localhost:5173` is in allowed origins list

### 6. Backend Connection Status
**From Process Logs (21:14:20):**
```
2026-10-31 21:14:20 - app.database - INFO - Connecting to MongoDB Atlas...
2026-10-31 21:14:23 - app.database - INFO - [OK] Connected to MongoDB Atlas -- database: medinova_ai
```

✅ **CONFIRMED:** Backend connected to MongoDB Atlas (not mongomock)  
⚠️ **OBSERVED:** Intermittent SSL handshake errors in background tasks (Python 3.14 + pymongo issue)  
✅ **CONFIRMED:** Initial connection successful, queries can execute

---

## EXECUTION FLOW ANALYSIS

### Normal Success Path:
```
1. Browser → GET /api/v1/health-records
2. FastAPI receives request
3. CORS middleware allows request (preflight/simple)
4. Authentication dependency extracts & validates token ✓
5. Database dependency provides MongoDB connection ✓
6. Endpoint executes: service.get_patient_records() ✓
7. MongoDB returns raw documents as dicts ✓
8. FastAPI serializes response using List[HealthRecordResponse]
9. CORS middleware adds Access-Control-Allow-Origin header
10. Browser receives 200 + JSON + CORS headers ✓
```

### Actual Failure Path:
```
1. Browser → GET /api/v1/health-records
2. FastAPI receives request
3. CORS middleware allows request (preflight/simple)
4. Authentication dependency extracts & validates token ✓
5. Database dependency provides MongoDB connection ✓
6. Endpoint executes: service.get_patient_records() ✓
7. MongoDB returns raw documents (some malformed) ✓
8. FastAPI attempts serialization using List[HealthRecordResponse]
   ├─ Record 1: valid → serializes ✓
   ├─ Record 2: malformed → Pydantic ValidationError ❌
   └─ EXCEPTION RAISED DURING SERIALIZATION
9. FastAPI internal exception handler catches ValidationError
10. Returns 500 Internal Server Error
11. CORS middleware NEVER REACHED (exception short-circuits response pipeline)
12. Browser receives 500 with NO Access-Control-Allow-Origin header ❌
13. Browser blocks response due to CORS policy violation ❌
```

---

## WHY NO BACKEND TRACEBACK IN LOGS

### Possible Explanations:

1. **Pydantic C Extensions:**  
   ValidationError raised in Pydantic's C-optimized code may not trigger Python's standard exception logging hooks.

2. **FastAPI Internal Handling:**  
   FastAPI's `response_model` validation happens in `fastapi.routing.serialize_response()` which has its own error handling that may not log to application logger.

3. **Uvicorn Worker Process:**  
   Error may be logged to a different stream (stderr vs file logger) or suppressed by uvicorn's error handling.

4. **Log Level Configuration:**  
   Validation errors might be logged at DEBUG level, which is below the configured INFO level.

### Evidence:
**File:** `backend/app/core/logging.py` (need to verify logging configuration)  
**Current behavior:** Only SSL background errors visible in logs, no application-level exceptions

---

## BROWSER BEHAVIOR ANALYSIS

### Why CORS Error Appears First:

1. **HTTP 500 returns without `Access-Control-Allow-Origin` header**
2. **Browser's CORS check happens BEFORE JavaScript can access response**
3. **Browser console shows:** "Access to XMLHttpRequest ... has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header"
4. **Actual error (500) is hidden behind CORS violation**

This is a **cascading failure**:
```
Validation Error → HTTP 500 without CORS → Browser blocks response → User sees CORS error
```

The CORS error is a **symptom**, not the cause.

---

## MOST LIKELY ROOT CAUSE

### Hypothesis with Supporting Evidence:

**The authenticated user HAS malformed health records in MongoDB that fail Pydantic validation when FastAPI attempts to serialize the response.**

**Supporting Evidence:**
1. ✅ Direct MongoDB query found 18 total records, 9 from `document_upload` source
2. ✅ At least one record (ID: 6ad4c4714a6ea6e30e382ef5) has:
   - `diagnosis` as string: `"Acute upper respiratory tract infection"`
   - Missing `recorded_by` field
3. ✅ `HealthRecordResponse` schema requires:
   - `diagnosis`: `Optional[DiagnosisDetails]` (expects dict or None, NOT string)
   - `recorded_by`: `str` (required field, NOT Optional)
4. ✅ Browser test confirms HTTP 500 error
5. ✅ Backend connected to MongoDB Atlas (not mock data)
6. ❌ Cannot confirm malformed record belongs to authenticated test user due to Python 3.14 SSL preventing standalone query

**Confidence Level:** 95%

---

## SECONDARY ISSUE: SSL HANDSHAKE ERRORS

### Observed Error:
```
ssl.SSLError: [SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:1077)
```

**File:** C:\Python314\Lib\ssl.py, line 1372  
**Frequency:** Intermittent, in background MongoDB connection pool maintenance  
**Impact:** Does not prevent initial connection or queries, but causes connection pool instability

**Evidence:**
- Python version: 3.14.0 (confirmed)
- pymongo background tasks encountering SSL errors every 10-40 seconds
- Initial connection succeeds, subsequent pool maintenance fails

**Separation of Concerns:**  
This is a **separate infrastructure issue**, NOT the root cause of HTTP 500. However, it:
- Makes debugging harder (log noise)
- Could cause intermittent failures under load
- Prevents reliable standalone investigation scripts

---

## SAFE, MINIMAL PROPOSED FIX

### Option A: Fix Future Creations (Safest, Recommended)

**File:** `backend/app/api/v1/document_upload.py`  
**Lines:** 377-410

**Change:**
```python
# BEFORE (bypasses validation):
health_record = {
    "patient_id": current_user["_id"],
    "record_type": extracted_data.get("record_type", "consultation_notes"),
    "recorded_at": datetime.utcnow(),
    "diagnosis": extracted_data.get("diagnosis"),  # Problem: can be string
    "source": "document_upload",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}
result = await db.health_records.insert_one(health_record)

# AFTER (uses service with validation):
from app.services.health_record_service import HealthRecordService
from app.schemas.health_record import HealthRecordCreate
from app.models.health_record import DiagnosisDetails

# Convert AI-extracted diagnosis string to proper object
diagnosis_obj = None
if extracted_data.get("diagnosis"):
    diagnosis_obj = DiagnosisDetails(
        condition=extracted_data["diagnosis"],
        diagnosed_by=None,  # AI extraction, not a doctor
        severity="moderate",
        notes="Extracted from document via AI"
    )

record_data = HealthRecordCreate(
    record_type=extracted_data.get("record_type", "consultation_notes"),
    recorded_at=datetime.utcnow(),
    diagnosis=diagnosis_obj,
    source="document_upload"
)

health_record_service = HealthRecordService(db)
record = await health_record_service.create_health_record(
    patient_id=current_user["_id"],
    recorder_id=current_user["_id"],  # Fixes missing recorded_by
    data=record_data
)
```

**Impact:**
- ✅ Prevents future malformed records
- ✅ Ensures Pydantic validation for all new records
- ✅ Adds required `recorded_by` field
- ✅ Converts diagnosis strings to proper DiagnosisDetails objects
- ❌ Does NOT fix existing malformed records

**Risk:** LOW - only affects new record creation

---

### Option B: Handle Legacy Records in Response Schema

**File:** `backend/app/schemas/health_record.py`  
**Lines:** 22-36

**Change:**
```python
from pydantic import BaseModel, Field, field_validator, ValidationInfo

class HealthRecordResponse(BaseModel):
    id: str
    patient_id: str
    record_type: str
    recorded_at: datetime
    vitals: Optional[VitalSigns] = None
    lab_test: Optional[LabTestDetails] = None
    diagnosis: Optional[DiagnosisDetails] = None
    note: Optional[GeneralNoteDetails] = None
    recorded_by: Optional[str] = None  # Changed from str to Optional[str]
    source: str
    device_name: Optional[str] = None
    appointment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @field_validator('diagnosis', mode='before')
    @classmethod
    def convert_diagnosis(cls, v, info: ValidationInfo):
        """Convert legacy string diagnosis to DiagnosisDetails object"""
        if v is None:
            return None
        if isinstance(v, str):
            # Legacy record: diagnosis stored as string
            return DiagnosisDetails(
                condition=v,
                severity="moderate",
                notes="Legacy format"
            )
        return v  # Already a dict/object

    @field_validator('recorded_by', mode='before')
    @classmethod
    def default_recorded_by(cls, v):
        """Provide default for missing recorded_by field"""
        return v if v else "system"

    class Config:
        populate_by_name = True
```

**Impact:**
- ✅ Fixes GET endpoint immediately for all users
- ✅ Handles existing malformed records gracefully
- ✅ No database migration required
- ⚠️ Perpetuates bad data structure
- ⚠️ Makes future schema changes harder

**Risk:** MEDIUM - changes API contract (recorded_by becomes optional)

---

### Option C: Database Migration (Most Complete)

**Create migration script:** `backend/migrations/fix_malformed_health_records.py`

```python
"""
Migration: Fix malformed health_records from document_upload
Fixes:
1. diagnosis field: string → DiagnosisDetails object
2. Add missing recorded_by field
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import os
from dotenv import load_dotenv

load_dotenv()

async def migrate():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client[os.getenv("MONGODB_DB_NAME", "medinova_ai")]
    
    # Find malformed records
    malformed = await db.health_records.find({
        "$or": [
            {"diagnosis": {"$type": "string"}},  # diagnosis is string
            {"recorded_by": {"$exists": False}}   # missing recorded_by
        ]
    }).to_list(1000)
    
    print(f"Found {len(malformed)} malformed records")
    
    for record in malformed:
        update = {}
        
        # Fix diagnosis if it's a string
        if "diagnosis" in record and isinstance(record["diagnosis"], str):
            update["diagnosis"] = {
                "condition": record["diagnosis"],
                "severity": "moderate",
                "notes": "Migrated from legacy string format"
            }
        
        # Add missing recorded_by
        if "recorded_by" not in record:
            # Use patient_id as recorder for self-uploaded documents
            update["recorded_by"] = record.get("patient_id", "system")
        
        if update:
            await db.health_records.update_one(
                {"_id": record["_id"]},
                {"$set": update}
            )
            print(f"Fixed record: {record['_id']}")
    
    print("Migration complete")
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate())
```

**Impact:**
- ✅ Fixes all existing malformed records
- ✅ Combined with Option A, provides complete solution
- ✅ Preserves data integrity
- ⚠️ Modifies production data
- ⚠️ Requires backup before execution
- ⚠️ May take time for large datasets

**Risk:** MEDIUM-HIGH - modifies production database

---

## RECOMMENDED APPROACH

**Implement Option A + Option C in sequence:**

1. **First:** Apply Option A (fix document_upload.py creation logic)
   - Prevents new malformed records
   - Low risk, immediate protection

2. **Second:** Create database backup

3. **Third:** Run Option C migration script
   - Fixes existing malformed records
   - One-time operation

**DO NOT implement Option B** - it perpetuates bad data and makes future changes harder.

---

## MISSING RUNTIME EVIDENCE

### What We Still Cannot Verify:

1. **Exact count of malformed records for authenticated test user**
   - Blocked by: Python 3.14 SSL issues prevent standalone MongoDB queries
   - Alternative: Use MongoDB Compass GUI to query directly

2. **Actual Pydantic ValidationError message**
   - Blocked by: Error not logged to application logs
   - Alternative: Add custom exception handler to FastAPI

3. **Whether multiple records or single record causes failure**
   - Blocked by: Cannot determine which record(s) belong to test user
   - Alternative: Manual query via MongoDB Compass

### How to Collect Missing Evidence (Without Code Changes):

**Method 1: MongoDB Compass Direct Query**
```
mongodb://cluster0-shard-00-01.yaoaa.mongodb.net:27017/medinova_ai
Collection: health_records
Filter: {
  "patient_id": "6ad1dbfeb7f33dc8b76a6c5e",
  "$or": [
    {"diagnosis": {"$type": "string"}},
    {"recorded_by": {"$exists": false}}
  ]
}
```

**Method 2: Temporary Exception Handler (Requires approval)**
Add to `backend/app/main.py`:
```python
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Pydantic ValidationError: {exc.errors()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Response validation failed", "errors": exc.errors()},
        headers={"Access-Control-Allow-Origin": "http://localhost:5173"}
    )
```

---

## CONCLUSION

**ROOT CAUSE:** Malformed health records from `document_upload` auto_save feature fail Pydantic validation during response serialization, causing HTTP 500 without CORS headers.

**CONFIDENCE:** 95% (cannot confirm specific user's records due to infrastructure limitations)

**SAFE FIX:** Option A (prevent future) + Option C (fix existing)

**ESTIMATED TIME:** 30 minutes implementation + 10 minutes testing

**APPROVAL REQUIRED BEFORE:** Any code changes, database modifications, or configuration updates.

---

**Investigation completed:** 2026-10-31 21:XX  
**Status:** Awaiting approval for proposed fix implementation
