"""
QR Code Router
FastAPI endpoints for Smart QR Health ID generation and scanning
"""

import os
import io
import uuid
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

from app.database import get_database
from app.core.dependencies import get_current_user
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/qr", tags=["QR Health ID"])


class ScanQRRequest(BaseModel):
    qr_data: str  # The decoded string from the QR code


def _generate_qr_png(data: dict) -> bytes:
    """Generate a QR code PNG image from a data dict."""
    try:
        import qrcode
        from PIL import Image, ImageDraw

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(data))
        qr.make(fit=True)

        # Create QR image with brand color
        img = qr.make_image(fill_color="#0ea5e9", back_color="white")  # Primary blue

        # Convert to bytes
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf.read()

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="qrcode library not installed. Run: pip install qrcode[pil]"
        )


@router.get("/patient/{patient_id}")
async def get_patient_qr(
    patient_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Generate a QR code PNG for a patient's Smart Health ID.
    
    **Access Rules:**
    - Patient can view their own QR
    - Doctor can view any patient's QR
    - Admin can view any QR
    
    **QR contains:** patient_id, name, and medinova URL
    **Doctor scans QR → Opens Patient Profile**
    """
    user_role = current_user.get("role")

    # Permission check: only patient themselves, doctors, or admin
    if user_role == "patient" and current_user["_id"] != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only view their own QR code"
        )

    # Fetch patient user record
    try:
        user_doc = await db.users.find_one(
            {"_id": ObjectId(patient_id)},
            {"password_hash": 0}
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient ID")

    if not user_doc or user_doc.get("role") != "patient":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Build QR payload
    qr_data = {
        "type": "medinova_patient",
        "patient_id": patient_id,
        "name": f"{user_doc.get('first_name', '')} {user_doc.get('last_name', '')}".strip(),
        "url": f"{settings.FRONTEND_URL}/patient/{patient_id}/profile",
        "version": "1.0"
    }

    png_bytes = _generate_qr_png(qr_data)
    return StreamingResponse(
        io.BytesIO(png_bytes),
        media_type="image/png",
        headers={
            "Content-Disposition": f'attachment; filename="patient_qr_{patient_id}.png"',
            "Cache-Control": "no-cache"
        }
    )


@router.get("/doctor/{doctor_id}")
async def get_doctor_qr(
    doctor_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Generate a QR code PNG for a doctor's Smart Health ID.
    
    **Doctor scans: Patient scans Doctor QR → Opens Doctor Profile + Appointment Booking**
    """
    user_role = current_user.get("role")

    # Permission: doctor views own, admin views all, patients view any (for booking)
    if user_role == "doctor" and current_user["_id"] != doctor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctors can only view their own QR code"
        )

    try:
        user_doc = await db.users.find_one(
            {"_id": ObjectId(doctor_id)},
            {"password_hash": 0}
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid doctor ID")

    if not user_doc or user_doc.get("role") != "doctor":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    # Get doctor profile for specialization
    doctor_profile = await db.doctor_profiles.find_one({"user_id": doctor_id})
    specialization = doctor_profile.get("specialization", "General Practitioner") if doctor_profile else "General Practitioner"

    qr_data = {
        "type": "medinova_doctor",
        "doctor_id": doctor_id,
        "name": f"Dr. {user_doc.get('first_name', '')} {user_doc.get('last_name', '')}".strip(),
        "specialization": specialization,
        "url": f"{settings.FRONTEND_URL}/patient/booking?doctor_id={doctor_id}",
        "version": "1.0"
    }

    png_bytes = _generate_qr_png(qr_data)
    return StreamingResponse(
        io.BytesIO(png_bytes),
        media_type="image/png",
        headers={
            "Content-Disposition": f'attachment; filename="doctor_qr_{doctor_id}.png"',
            "Cache-Control": "no-cache"
        }
    )


@router.post("/scan")
async def scan_qr_code(
    request: ScanQRRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Decode and validate a scanned QR code string.
    
    **Input:** Raw string decoded from QR camera scan
    **Returns:** Profile data and redirect URL based on QR type
    """
    try:
        qr_data = json.loads(request.qr_data)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid QR code format — not a valid MediNova QR code"
        )

    qr_type = qr_data.get("type")

    if qr_type == "medinova_patient":
        patient_id = qr_data.get("patient_id")
        if not patient_id:
            raise HTTPException(status_code=400, detail="Invalid QR data: missing patient_id")

        user_doc = await db.users.find_one(
            {"_id": ObjectId(patient_id)},
            {"password_hash": 0, "email": 0}
        )
        if not user_doc:
            raise HTTPException(status_code=404, detail="Patient not found")

        return {
            "type": "patient",
            "patient_id": patient_id,
            "name": f"{user_doc.get('first_name', '')} {user_doc.get('last_name', '')}".strip(),
            "redirect_url": f"/patient/{patient_id}/profile",
            "action": "view_profile"
        }

    elif qr_type == "medinova_doctor":
        doctor_id = qr_data.get("doctor_id")
        if not doctor_id:
            raise HTTPException(status_code=400, detail="Invalid QR data: missing doctor_id")

        user_doc = await db.users.find_one(
            {"_id": ObjectId(doctor_id)},
            {"password_hash": 0, "email": 0}
        )
        if not user_doc:
            raise HTTPException(status_code=404, detail="Doctor not found")

        doctor_profile = await db.doctor_profiles.find_one({"user_id": doctor_id})

        return {
            "type": "doctor",
            "doctor_id": doctor_id,
            "name": f"Dr. {user_doc.get('first_name', '')} {user_doc.get('last_name', '')}".strip(),
            "specialization": doctor_profile.get("specialization") if doctor_profile else "General Practitioner",
            "redirect_url": f"/patient/booking?doctor_id={doctor_id}",
            "action": "book_appointment"
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown QR type: {qr_type}. This is not a valid MediNova QR code."
        )
