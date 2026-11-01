"""
Doctors Router
FastAPI endpoints for doctors and patients looking for doctors
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.core.dependencies import get_current_user, require_doctor
from app.schemas.doctor_profile import DoctorProfileUpdate, DoctorProfileResponse
from app.services.doctor_service import DoctorService
from app.utils.validators import validate_object_id, sanitize_string

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("", response_model=List[DoctorProfileResponse])
async def get_doctors(
    specialization: Optional[str] = Query(None, description="Filter doctors by specialty", max_length=100),
    search: Optional[str] = Query(None, description="Search doctors by name", max_length=200),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Search and filter the list of verified doctors"""
    # Sanitize search inputs to prevent injection attacks
    if specialization:
        specialization = sanitize_string(specialization, max_length=100)
    if search:
        search = sanitize_string(search, max_length=200)
    
    doctor_service = DoctorService(db)
    doctors = await doctor_service.get_doctors_list(specialization, search)
    return doctors

@router.get("/profile", response_model=DoctorProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(require_doctor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Retrieve doctor professional profile and availability days"""
    doctor_service = DoctorService(db)
    profile = await doctor_service.get_doctor_profile(current_user["_id"])
    return profile

@router.put("/profile", response_model=DoctorProfileResponse)
async def update_my_profile(
    profile_data: DoctorProfileUpdate,
    current_user: dict = Depends(require_doctor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Modify details, fee, bios, and office hours"""
    doctor_service = DoctorService(db)
    profile = await doctor_service.update_doctor_profile(current_user["_id"], profile_data)
    return profile

@router.get("/{doctor_id}", response_model=DoctorProfileResponse)
async def get_doctor_by_id(
    doctor_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get professional profile of specific doctor by user ID"""
    # Validate ObjectId format
    validate_object_id(doctor_id, "Doctor ID")
    
    doctor_service = DoctorService(db)
    profile = await doctor_service.get_doctor_profile(doctor_id)
    return profile
