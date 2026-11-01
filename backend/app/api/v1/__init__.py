"""
API Version 1 Routes
"""

from fastapi import APIRouter
from app.api.v1 import (
    health, auth, patients, doctors, appointments,
    medications, health_records, hospitals, notifications, admin,
    ai, ocr, qr, oauth, document_upload
)

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health Check"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    patients.router,
    prefix="",
    tags=["Patients"]
)

api_router.include_router(
    doctors.router,
    prefix="",
    tags=["Doctors"]
)

api_router.include_router(
    appointments.router,
    prefix="",
    tags=["Appointments"]
)

api_router.include_router(
    medications.router,
    prefix="",
    tags=["Medications"]
)

api_router.include_router(
    health_records.router,
    prefix="",
    tags=["Health Records"]
)

api_router.include_router(
    hospitals.router,
    prefix="",
    tags=["Hospitals"]
)

api_router.include_router(
    notifications.router,
    prefix="",
    tags=["Notifications"]
)

api_router.include_router(
    admin.router,
    prefix="",
    tags=["Admin Operations"]
)

# New feature routers
api_router.include_router(
    ai.router,
    prefix="",
    tags=["AI Assistant"]
)

api_router.include_router(
    ocr.router,
    prefix="",
    tags=["OCR"]
)

api_router.include_router(
    qr.router,
    prefix="",
    tags=["QR Health ID"]
)

api_router.include_router(
    oauth.router,
    prefix="",
    tags=["OAuth"]
)

api_router.include_router(
    document_upload.router,
    prefix="",
    tags=["Smart Documents"]
)
