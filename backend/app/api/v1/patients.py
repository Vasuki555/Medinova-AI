"""
Patients Profile Router
FastAPI endpoints for patients
"""

from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from pydantic import BaseModel, validator
from typing import Optional
import re

from app.database import get_database
from app.core.dependencies import require_patient, get_current_user
from app.schemas.patient_profile import PatientProfileUpdate, PatientProfileResponse
from app.services.patient_service import PatientService
from app.utils.validators import validate_object_id, validate_phone

router = APIRouter(prefix="/patients", tags=["Patients"])


class BasicProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    
    @validator("first_name", "last_name")
    def validate_names(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) < 1 or len(v) > 50:
                raise ValueError("Name must be between 1 and 50 characters")
            if not re.match(r"^[a-zA-Z\s\-']+$", v):
                raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
        return v
    
    @validator("phone")
    def validate_phone_format(cls, v):
        if v is not None and v.strip():
            # Remove spaces, dashes, parentheses for validation
            cleaned = re.sub(r'[\s\-\(\)]', '', v)
            # Allow + prefix and 7-15 digits
            pattern = r'^\+?[0-9]{7,15}$'
            if not re.match(pattern, cleaned):
                raise ValueError("Phone number must contain 7-15 digits and optionally start with +")
        return v
    
    @validator("gender")
    def validate_gender_value(cls, v):
        if v is not None:
            allowed = ["male", "female", "other", "prefer_not_to_say"]
            if v.lower() not in allowed:
                raise ValueError(f"Gender must be one of: {', '.join(allowed)}")
            return v.lower()
        return v


@router.get("/profile", response_model=PatientProfileResponse)
async def get_profile(
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get the patient profile for the active logged in user"""
    patient_service = PatientService(db)
    profile = await patient_service.get_patient_profile(current_user["_id"])
    return profile


@router.put("/profile", response_model=PatientProfileResponse)
async def update_profile(
    profile_data: PatientProfileUpdate,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update patient medical attributes (allergies, contact info, health preferences)"""
    patient_service = PatientService(db)
    profile = await patient_service.update_patient_profile(current_user["_id"], profile_data)
    return profile


@router.put("/profile/basic")
async def update_basic_profile(
    data: BasicProfileUpdate,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update basic personal info (name, phone, DOB, gender) stored in users collection"""
    update_fields = data.dict(exclude_none=True)
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_fields["updated_at"] = datetime.utcnow()

    result = await db.users.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await db.users.find_one(
        {"_id": ObjectId(current_user["_id"])},
        {"password_hash": 0}
    )
    updated_user["id"] = str(updated_user.pop("_id"))

    # Convert datetimes
    for key in ["created_at", "updated_at", "last_login_at"]:
        if updated_user.get(key):
            updated_user[key] = updated_user[key].isoformat()

    return {"success": True, "user": updated_user}
