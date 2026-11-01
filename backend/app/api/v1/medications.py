"""
Medications Router
FastAPI endpoints for daily medication schedules and logs
"""

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.core.dependencies import require_patient
from app.schemas.medication import MedicationCreate, MedicationUpdate, LogIntakeRequest, MedicationResponse
from app.services.medication_service import MedicationService

router = APIRouter(prefix="/medications", tags=["Medications"])

@router.get("", response_model=List[MedicationResponse])
async def get_my_medications(
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Retrieve all reminders and stock levels for the patient"""
    service = MedicationService(db)
    meds = await service.get_patient_medications(current_user["_id"])
    return meds

@router.post("", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    data: MedicationCreate,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Register a new pill or syrup intake schedule"""
    service = MedicationService(db)
    med = await service.create_medication(current_user["_id"], data)
    return med

@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_reminder(
    medication_id: str,
    data: MedicationUpdate,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Modify doses, hours, pause reminders, or update stock details"""
    service = MedicationService(db)
    med = await service.update_medication(current_user["_id"], medication_id, data)
    return med

@router.post("/{medication_id}/log", response_model=MedicationResponse)
async def log_intake(
    medication_id: str,
    data: LogIntakeRequest,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Record a taken/skipped dose to update compliance logs and decrement inventory"""
    service = MedicationService(db)
    med = await service.log_medication_intake(current_user["_id"], medication_id, data)
    return med

@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reminder(
    medication_id: str,
    current_user: dict = Depends(require_patient),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Remove a medicine tracker permanently"""
    service = MedicationService(db)
    deleted = await service.delete_medication(current_user["_id"], medication_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found or access denied"
        )
    return None

