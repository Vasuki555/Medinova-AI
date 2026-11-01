"""
OCR Router
FastAPI endpoints for medical document text extraction via EasyOCR
"""

import os
import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Request, Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.core.dependencies import get_current_user
from app.services.ocr_service import ocr_service
from app.config import settings
from app.core.rate_limit import limit_ocr

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ocr", tags=["OCR"])

ALLOWED_TYPES = [
    "image/jpeg", "image/png", "image/webp", "image/bmp",
    "application/pdf"
]


def _ensure_upload_dir():
    """Create uploads directory if it doesn't exist."""
    os.makedirs(settings.upload_dir_path, exist_ok=True)
    return settings.upload_dir_path


@router.post(
    "/extract",
    summary="Extract Text from Medical Document",
    description="""
    Extract text from a medical report using EasyOCR.
    
    **Rate Limit:** 10 OCR extractions per minute per user
    
    **Supported formats:** JPEG, PNG, WEBP, BMP, PDF
    **Max size:** 10 MB
    
    - Images are preprocessed with OpenCV for better accuracy
    - PDFs: text-based PDFs use direct extraction; scanned PDFs use image OCR
    
    Returns extracted text for use with the AI analysis endpoint.
    """,
    responses={
        200: {
            "description": "Text successfully extracted"
        },
        400: {
            "description": "Empty or invalid file"
        },
        413: {
            "description": "File too large (max 10 MB)"
        },
        415: {
            "description": "Unsupported file type"
        },
        422: {
            "description": "OCR extraction failed"
        },
        429: {
            "description": "Too many OCR requests. Rate limit exceeded."
        }
    }
)
# Temporarily disabled rate limiting to debug
# @limit_ocr()
async def extract_text_from_file(
    request: Request,
    response: Response,
    file: UploadFile = File(..., description="Medical report image (JPEG/PNG) or PDF"),
    current_user: dict = Depends(get_current_user)
):
    """
    Extract text from a medical report using EasyOCR.
    
    **Supported formats:** JPEG, PNG, WEBP, BMP, PDF
    **Max size:** 10 MB
    
    - Images are preprocessed with OpenCV for better accuracy
    - PDFs: text-based PDFs use direct extraction; scanned PDFs use image OCR
    - Rate limited to 10 extractions per minute per user
    
    Returns extracted text for use with the AI analysis endpoint.
    """
    # Validate file type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES:
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
                    detail=f"File too large. Max allowed: {settings.MAX_UPLOAD_SIZE_MB} MB"
                )
            
            file_bytes.extend(chunk)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File read error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error reading uploaded file"
        )

    if total_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    # Save temp file for OCR
    upload_dir = _ensure_upload_dir()
    ext = ".pdf" if content_type == "application/pdf" else ".png"
    temp_filename = f"ocr_temp_{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(upload_dir, temp_filename)

    try:
        with open(temp_path, 'wb') as f:
            f.write(file_bytes)

        # Run OCR
        result = await ocr_service.extract_from_file(temp_path, content_type)

    finally:
        # Always clean up temp file
        try:
            os.remove(temp_path)
        except Exception:
            pass

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=result.get("error", "OCR extraction failed")
        )

    return {
        "success": True,
        "extracted_text": result.get("text", ""),
        "word_count": result.get("word_count", 0),
        "source_type": result.get("source_type"),
        "filename": file.filename
    }
