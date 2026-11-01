"""
Health Records Router
FastAPI endpoints for vitals logging, laboratory results, and clinical history
"""

import os
import uuid
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from app.database import get_database
from app.core.dependencies import get_current_user, require_patient_or_doctor
from app.schemas.health_record import HealthRecordCreate, HealthRecordResponse
from app.services.health_record_service import HealthRecordService
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health-records", tags=["Health Records"])

ALLOWED_UPLOAD_TYPES = [
    "image/jpeg", "image/png", "image/webp", "image/bmp", "application/pdf"
]


def _ensure_upload_dir():
    """Create uploads directory if it doesn't exist."""
    path = settings.upload_dir_path
    os.makedirs(path, exist_ok=True)
    return path


@router.get("", response_model=List[HealthRecordResponse])
async def list_records(
    patient_id: Optional[str] = Query(None, description="Retrieve records of specific patient (doctor use case)"),
    record_type: Optional[str] = Query(None, description="Filter by: vitals, lab_test, diagnosis, note"),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Retrieve full timeline of clinical diaries, diagnostics, and vitals logs"""
    try:
        service = HealthRecordService(db)
        
        # Determine target patient based on role and authorization
        target_patient_id = current_user["_id"]
        
        # If patient_id is specified and user is not a patient
        if patient_id and current_user["role"] != "patient":
            # Admin can access any patient records
            if current_user["role"] == "admin":
                target_patient_id = patient_id
            # Doctor must have an appointment with the patient
            elif current_user["role"] == "doctor":
                # Verify doctor has appointment with this patient
                appointment = await db.appointments.find_one({
                    "doctor_id": current_user["_id"],
                    "patient_id": patient_id,
                    "status": {"$in": ["scheduled", "completed", "in_progress"]}
                })
                
                if not appointment:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied. No active or completed appointments with this patient.",
                        headers={"error_code": "UNAUTHORIZED_PATIENT_ACCESS"}
                    )
                
                target_patient_id = patient_id
        elif patient_id and current_user["role"] == "patient":
            # Patients can only access their own records
            if patient_id != current_user["_id"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. Patients can only access their own health records.",
                    headers={"error_code": "UNAUTHORIZED_ACCESS"}
                )
            
        records = await service.get_patient_records(target_patient_id, record_type)
        return records
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health records endpoint error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    data: HealthRecordCreate,
    patient_id: Optional[str] = Query(None, description="Patient user ID if logged by doctor"),
    current_user: dict = Depends(require_patient_or_doctor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Log a manual vitals sign measurement, lab result parameters, or health diary entry"""
    service = HealthRecordService(db)
    
    # Determine target patient with authorization
    target_patient_id = current_user["_id"]
    
    if patient_id and current_user["role"] != "patient":
        # Admin can create records for any patient
        if current_user["role"] == "admin":
            target_patient_id = patient_id
        # Doctor must have appointment with patient
        elif current_user["role"] == "doctor":
            # Verify doctor has appointment with this patient
            appointment = await db.appointments.find_one({
                "doctor_id": current_user["_id"],
                "patient_id": patient_id,
                "status": {"$in": ["scheduled", "completed", "in_progress"]}
            })
            
            if not appointment:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. No active or completed appointments with this patient.",
                    headers={"error_code": "UNAUTHORIZED_PATIENT_ACCESS"}
                )
            
            target_patient_id = patient_id
    elif patient_id and current_user["role"] == "patient":
        # Patients can only create their own records
        if patient_id != current_user["_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients can only create their own health records.",
                headers={"error_code": "UNAUTHORIZED_ACCESS"}
            )

    record = await service.create_health_record(target_patient_id, current_user["_id"], data)
    return record

@router.get("/trends")
async def get_trends(
    patient_id: Optional[str] = Query(None, description="Patient user ID if queried by doctor"),
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(require_patient_or_doctor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get time-series vital logs sorted chronologically (perfect for graphs)"""
    service = HealthRecordService(db)
    
    # Determine target patient with authorization
    target_patient_id = current_user["_id"]
    
    if patient_id and current_user["role"] != "patient":
        # Admin can access any patient trends
        if current_user["role"] == "admin":
            target_patient_id = patient_id
        # Doctor must have appointment with patient
        elif current_user["role"] == "doctor":
            # Verify doctor has appointment with this patient
            appointment = await db.appointments.find_one({
                "doctor_id": current_user["_id"],
                "patient_id": patient_id,
                "status": {"$in": ["scheduled", "completed", "in_progress"]}
            })
            
            if not appointment:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. No active or completed appointments with this patient.",
                    headers={"error_code": "UNAUTHORIZED_PATIENT_ACCESS"}
                )
            
            target_patient_id = patient_id
    elif patient_id and current_user["role"] == "patient":
        # Patients can only access their own trends
        if patient_id != current_user["_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Patients can only access their own health trends.",
                headers={"error_code": "UNAUTHORIZED_ACCESS"}
            )
        
    trends = await service.get_vitals_trends(target_patient_id, limit)
    return trends


@router.post("/upload")
async def upload_medical_report(
    file: UploadFile = File(..., description="Medical report image (JPEG/PNG) or PDF document"),
    record_type: str = Form(default="lab_test", description="Type: lab_test, xray, mri, prescription, other"),
    notes: str = Form(default="", description="Optional notes about the uploaded report"),
    current_user: dict = Depends(require_patient_or_doctor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Upload a medical report file (image or PDF).
    
    **Supported formats:** JPEG, PNG, WEBP, BMP, PDF
    **Max size:** 10 MB
    
    Returns the stored file URL and record metadata.
    After uploading, use the `/ocr/extract` endpoint to extract text,
    then `/ai/analyze-report` to get AI interpretation.
    """
    # Validate content type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_UPLOAD_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {content_type}. Allowed: JPEG, PNG, WEBP, BMP, PDF"
        )

    # Read file with size validation (streaming approach)
    max_size = settings.max_upload_size_bytes
    chunk_size = 1024 * 1024  # 1 MB chunks
    file_bytes = bytearray()
    total_size = 0
    
    try:
        while chunk := await file.read(chunk_size):
            total_size += len(chunk)
            
            # Check size BEFORE adding to memory
            if total_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Max: {settings.MAX_UPLOAD_SIZE_MB} MB"
                )
            
            file_bytes.extend(chunk)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error reading uploaded file"
        )

    if total_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    # Generate unique filename
    ext_map = {
        "image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
        "image/bmp": ".bmp", "application/pdf": ".pdf"
    }
    ext = ext_map.get(content_type, ".bin")
    unique_name = f"{current_user['_id']}_{uuid.uuid4().hex}{ext}"

    # Save file
    upload_dir = _ensure_upload_dir()
    file_path = os.path.join(upload_dir, unique_name)
    
    try:
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
    except Exception as e:
        logger.error(f"File save error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file"
        )

    # File URL (served via static files)
    file_url = f"/uploads/{unique_name}"

    # Save metadata to DB
    report_doc = {
        "user_id": current_user["_id"],
        "file_name": file.filename,
        "stored_name": unique_name,
        "file_url": file_url,
        "file_size_bytes": total_size,
        "content_type": content_type,
        "record_type": record_type,
        "notes": notes,
        "ocr_text": None,
        "ai_analysis": None,
        "uploaded_at": datetime.utcnow(),
        "created_at": datetime.utcnow()
    }

    result = await db.medical_reports.insert_one(report_doc)
    report_doc["id"] = str(result.inserted_id)
    report_doc.pop("_id", None)

    return {
        "success": True,
        "message": "Report uploaded successfully",
        "report_id": report_doc["id"],
        "file_url": file_url,
        "file_name": file.filename,
        "content_type": content_type,
        "record_type": record_type,
        "uploaded_at": report_doc["uploaded_at"].isoformat()
    }


@router.get("/reports")
async def get_medical_reports(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List all uploaded medical reports for the current user."""
    cursor = db.medical_reports.find(
        {"user_id": current_user["_id"]}
    ).sort("uploaded_at", -1).limit(50)

    reports = await cursor.to_list(50)
    for r in reports:
        r["id"] = str(r.pop("_id", ""))
        # Serialize datetime
        if isinstance(r.get("uploaded_at"), datetime):
            r["uploaded_at"] = r["uploaded_at"].isoformat()
        if isinstance(r.get("created_at"), datetime):
            r["created_at"] = r["created_at"].isoformat()

    return reports
