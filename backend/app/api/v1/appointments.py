"""
Appointments Router
FastAPI endpoints for bookings and telehealth consultation logs
"""

from typing import List
from fastapi import APIRouter, Depends, status, Body
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.core.dependencies import get_current_user, require_patient, require_doctor
from app.schemas.appointment import AppointmentCreate, AppointmentStatusUpdate, AppointmentResponse, AppointmentConsultationUpdate
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def book_appointment(
    data: AppointmentCreate,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new booking slot"""
    service = AppointmentService(db)
    appointment = await service.create_appointment(current_user["_id"], data)
    return appointment

@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all appointments for the logged-in user (patient or doctor)"""
    service = AppointmentService(db)
    appointments = await service.get_user_appointments(current_user["_id"], current_user["role"])
    return appointments

@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_status(
    appointment_id: str,
    data: AppointmentStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Cancel, confirm, complete, or reject a booking"""
    service = AppointmentService(db)
    appointment = await service.update_appointment_status(
        appointment_id, current_user["_id"], current_user["role"], data
    )
    return appointment

@router.patch("/{appointment_id}/consultation", response_model=AppointmentResponse)
async def write_consultation(
    appointment_id: str,
    data: AppointmentConsultationUpdate,
    current_user: dict = Depends(require_doctor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Log vitals, write diagnosis notes, and finalize session (doctors only)"""
    service = AppointmentService(db)
    appointment = await service.update_consultation(
        appointment_id, current_user["_id"], data.consultation.model_dump()
    )
    return appointment
