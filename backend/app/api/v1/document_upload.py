"""
Smart Document Upload Router
Automatically extract and process medical documents with AI
"""

import os
import uuid
import logging
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.database import get_database
from app.core.dependencies import get_current_user, require_patient
from app.services.ocr_service import ocr_service
from app.services.document_processor import document_processor
from app.services.medication_service import MedicationService
from app.services.notification_service import NotificationService
from app.services.health_record_service import HealthRecordService
from app.schemas.health_record import HealthRecordCreate, GeneralNoteDetails
from app.config import settings
from app.core.rate_limit import limit_ocr

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["Smart Documents"])

ALLOWED_TYPES = [
    "image/jpeg", "image/png", "image/webp", "image/bmp",
    "application/pdf"
]


def _ensure_upload_dir():
    """Create uploads directory if it doesn't exist."""
    os.makedirs(settings.upload_dir_path, exist_ok=True)
    return settings.upload_dir_path


@router.post(
    "/upload-prescription",
    summary="Smart Prescription Upload",
    description="""
    Upload a prescription or medicine photo and automatically extract medicine information.
    
    **Features:**
    - Automatically extracts medicine names, dosages, frequencies
    - Creates medicine reminders automatically
    - Extracts prescription details (doctor, date, patient)
    - Allows review and edit before saving
    
    **Supported formats:** JPEG, PNG, WEBP, BMP, PDF
    **Max size:** 10 MB
    """,
    responses={
        200: {
            "description": "Document processed and information extracted"
        },
        400: {
            "description": "Invalid file"
        },
        413: {
            "description": "File too large"
        },
        415: {
            "description": "Unsupported file type"
        },
        422: {
            "description": "Processing failed"
        },
        429: {
            "description": "Rate limit exceeded"
        }
    }
)
# @limit_ocr()  # Temporarily disabled for debugging
async def upload_prescription(
    request: Request,
    file: UploadFile = File(..., description="Prescription image or PDF"),
    auto_save: bool = Form(False, description="Automatically save extracted medicines"),
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Smart prescription upload with automatic medicine extraction.
    
    1. Extracts text using OCR
    2. Uses AI to identify medicines and their details
    3. Optionally auto-saves to medicine reminders
    4. Returns extracted data for user review
    """
    # Validate file type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type. Allowed: JPEG, PNG, WEBP, BMP, PDF"
        )

    # Read file with size validation
    max_size = settings.max_upload_size_bytes
    chunk_size = 1024 * 1024  # 1 MB
    file_bytes = bytearray()
    total_size = 0
    
    try:
        while chunk := await file.read(chunk_size):
            total_size += len(chunk)
            if total_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Max: {settings.MAX_UPLOAD_SIZE_MB} MB"
                )
            file_bytes.extend(chunk)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File read error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error reading file"
        )

    if total_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Save temp file
    upload_dir = _ensure_upload_dir()
    ext = ".pdf" if content_type == "application/pdf" else ".png"
    temp_filename = f"prescription_{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(upload_dir, temp_filename)

    try:
        # Write file
        with open(temp_path, 'wb') as f:
            f.write(file_bytes)

        # Step 1: OCR extraction
        ocr_result = await ocr_service.extract_from_file(temp_path, content_type)
        
        if not ocr_result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ocr_result.get("error", "OCR failed")
            )

        extracted_text = ocr_result.get("text", "")
        
        # Step 2: AI-powered information extraction
        medicine_info = await document_processor.extract_medicine_information(extracted_text)
        
        if not medicine_info.get("success"):
            return {
                "success": False,
                "error": medicine_info.get("error"),
                "extracted_text": extracted_text,
                "filename": file.filename
            }

        # Step 3: Auto-save medicines if requested
        saved_medicines = []
        if auto_save and medicine_info.get("medicines"):
            med_service = MedicationService(db)
            notification_service = NotificationService(db)
            
            for med in medicine_info["medicines"]:
                # Check for duplicates based on medicine name
                existing = await db.medications.find_one({
                    "patient_id": current_user["_id"],
                    "medicine_name": {"$regex": f"^{re.escape(med['medicine_name'])}$", "$options": "i"},
                    "is_active": True
                })
                
                if existing:
                    logger.info(f"Skipping duplicate medicine: {med['medicine_name']}")
                    continue
                
                # Calculate schedule times based on time_of_day
                schedule_times = []
                time_mapping = {
                    "morning": "08:00",
                    "afternoon": "14:00",
                    "evening": "18:00",
                    "night": "22:00"
                }
                for tod in med.get("time_of_day", []):
                    if tod in time_mapping:
                        schedule_times.append(time_mapping[tod])
                
                if not schedule_times:
                    schedule_times = ["09:00"]  # Default to morning

                # Prepare medicine data
                from app.schemas.medication import MedicationCreate
                med_data = MedicationCreate(
                    medicine_name=med["medicine_name"],
                    dosage=med["dosage"],
                    frequency=med["frequency"],
                    schedule_times=schedule_times,
                    duration_days=med.get("duration_days"),
                    instructions=med["instructions"],
                    meal_timing=med.get("meal_timing", "anytime"),
                    current_quantity=med.get("current_quantity"),
                    refill_reminder_at=5 if med.get("current_quantity") else None
                )
                
                # Create medicine reminder
                try:
                    created_med = await med_service.create_medication(
                        current_user["_id"],
                        med_data
                    )
                    saved_medicines.append({
                        "id": created_med["id"],
                        "name": created_med["medicine_name"],
                        "confidence": med.get("confidence", "medium")
                    })
                except Exception as e:
                    logger.error(f"Failed to save medicine {med['medicine_name']}: {e}")
            
            # Create summary notification
            if saved_medicines:
                await notification_service.create_notification(
                    user_id=current_user["_id"],
                    type="medication",
                    category="success",
                    title="Prescription Processed",
                    message=f"Added {len(saved_medicines)} medicine(s) from your prescription automatically.",
                    action_url="/patient/dashboard",
                    action_text="View Medicines"
                )

        return {
            "success": True,
            "extracted_text": extracted_text,
            "medicine_info": medicine_info,
            "saved_medicines": saved_medicines if auto_save else None,
            "auto_saved": auto_save,
            "filename": file.filename,
            "word_count": ocr_result.get("word_count", 0)
        }

    finally:
        # Clean up temp file
        try:
            os.remove(temp_path)
        except Exception:
            pass


@router.post(
    "/upload-medical-record",
    summary="Smart Medical Record Upload",
    description="""
    Upload a lab report, test result, or medical document and automatically extract key information.
    
    **Features:**
    - Extracts test results and vitals
    - Identifies abnormal values
    - Creates health records automatically
    - Provides AI analysis
    
    **Supported formats:** JPEG, PNG, WEBP, BMP, PDF
    **Max size:** 10 MB
    """,
)
# @limit_ocr()  # Temporarily disabled for debugging  
async def upload_medical_record(
    request: Request,
    file: UploadFile = File(..., description="Medical report image or PDF"),
    auto_save: bool = Form(False, description="Automatically save as health record"),
    record_type: Optional[str] = Form(None, description="Type of record (lab_report, imaging, vitals, etc.)"),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Smart medical record upload with automatic information extraction.
    """
    # Validate file type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type"
        )

    # Read file
    max_size = settings.max_upload_size_bytes
    chunk_size = 1024 * 1024
    file_bytes = bytearray()
    total_size = 0
    
    try:
        while chunk := await file.read(chunk_size):
            total_size += len(chunk)
            if total_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Max: {settings.MAX_UPLOAD_SIZE_MB} MB"
                )
            file_bytes.extend(chunk)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error reading file"
        )

    if total_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Save temp file
    upload_dir = _ensure_upload_dir()
    ext = ".pdf" if content_type == "application/pdf" else ".png"
    temp_filename = f"medical_record_{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(upload_dir, temp_filename)

    try:
        with open(temp_path, 'wb') as f:
            f.write(file_bytes)

        # OCR extraction
        ocr_result = await ocr_service.extract_from_file(temp_path, content_type)
        
        if not ocr_result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ocr_result.get("error", "OCR failed")
            )

        extracted_text = ocr_result.get("text", "")
        
        # AI extraction
        record_info = await document_processor.extract_medical_record_information(extracted_text)
        
        if not record_info.get("success"):
            return {
                "success": False,
                "error": record_info.get("error"),
                "extracted_text": extracted_text,
                "filename": file.filename
            }

        # Auto-save health record if requested
        saved_record_id = None
        if auto_save:
            # Check for potential duplicates
            import re
            report_name = record_info.get("report_name", "")
            test_date = record_info.get("test_date")
            
            duplicate_check = {
                "patient_id": current_user["_id"],
            }
            
            if report_name:
                duplicate_check["notes"] = {"$regex": re.escape(report_name), "$options": "i"}
            
            if test_date:
                try:
                    date_obj = datetime.fromisoformat(test_date)
                    duplicate_check["recorded_at"] = {
                        "$gte": date_obj,
                        "$lt": date_obj + timedelta(days=1)
                    }
                except:
                    pass
            
            existing = await db.health_records.find_one(duplicate_check)
            
            if not existing:
                # Build note content with extracted information
                note_parts = []
                
                # Add report name
                report_name = record_info.get("report_name", "Medical Report")
                note_parts.append(f"Report: {report_name}")
                
                # Add summary if available
                summary = record_info.get("summary")
                if summary:
                    note_parts.append(f"\nSummary:\n{summary}")
                
                # Add diagnosis text to note (NOT as DiagnosisDetails to avoid auto-severity)
                diagnosis_text = record_info.get("diagnosis")
                if diagnosis_text:
                    note_parts.append(f"\nDiagnosis: {diagnosis_text}")
                
                # Add key findings with defensive iteration
                key_findings = record_info.get("key_findings")
                if key_findings and isinstance(key_findings, list):
                    note_parts.append("\nKey Findings:")
                    for finding in key_findings:
                        if isinstance(finding, str) and finding.strip():
                            note_parts.append(f"• {finding}")
                
                # CRITICAL: Document date limitation for medical integrity
                upload_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
                note_parts.append(f"\n[Clinical date unknown - Record uploaded {upload_timestamp}]")
                note_parts.append(f"[Source document: {file.filename}]")
                
                note_content = "\n".join(note_parts)
                
                # Create validated health record via service
                health_record_service = HealthRecordService(db)
                
                # Build HealthRecordCreate with required fields
                health_record_data = HealthRecordCreate(
                    record_type=record_info.get("record_type", record_type or "other"),
                    note=GeneralNoteDetails(
                        title=record_info.get("report_name") or "Medical Report",
                        content=note_content
                    )
                    # recorded_at omitted: will use schema default (upload time)
                    # This is semantically correct for "date unknown" cases
                )
                
                # Create record through validated service
                created_record = await health_record_service.create_health_record(
                    patient_id=current_user["_id"],
                    recorder_id=current_user["_id"],  # Uploader is the recorder
                    data=health_record_data
                )
                
                saved_record_id = created_record["id"]
                
                # Create notification
                notification_service = NotificationService(db)
                await notification_service.create_notification(
                    user_id=current_user["_id"],
                    type="health_record",
                    category="info",
                    title="Medical Record Added",
                    message=f"New record: {record_info.get('report_name', 'Medical Report')}",
                    action_url="/patient/dashboard",
                    action_text="View Records"
                )

        return {
            "success": True,
            "extracted_text": extracted_text,
            "record_info": record_info,
            "saved_record_id": saved_record_id,
            "auto_saved": auto_save,
            "filename": file.filename,
            "word_count": ocr_result.get("word_count", 0)
        }

    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass


import re
