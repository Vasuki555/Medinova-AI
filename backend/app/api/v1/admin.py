"""
Admin Router
FastAPI endpoints for overall system administration, user management, and metrics
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.database import get_database
from app.core.dependencies import require_admin
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

@router.get("/stats")
async def get_system_stats(
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Retrieve high-level metrics for patient, doctor, and booking collections"""
    total_users = await db.users.count_documents({})
    total_patients = await db.users.count_documents({"role": "patient"})
    total_doctors = await db.users.count_documents({"role": "doctor"})
    
    total_appointments = await db.appointments.count_documents({})
    completed_appointments = await db.appointments.count_documents({"status": "completed"})
    active_medications = await db.medications.count_documents({"is_active": True})
    
    verified_doctors = await db.doctor_profiles.count_documents({"is_verified": True})
    unverified_doctors = await db.doctor_profiles.count_documents({"is_verified": False})

    # Recent signups helper
    recent_users_cursor = db.users.find({}, {"password_hash": 0}).sort("created_at", -1).limit(5)
    recent_users = await recent_users_cursor.to_list(5)
    for u in recent_users:
        u["id"] = str(u["_id"])
        del u["_id"]

    return {
        "metrics": {
            "total_users": total_users,
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "active_medications": active_medications,
            "verified_doctors": verified_doctors,
            "unverified_doctors": unverified_doctors
        },
        "recent_signups": recent_users
    }

@router.get("/users")
async def list_all_users(
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List all user profiles in the database (admin view)"""
    cursor = db.users.find({}, {"password_hash": 0}).sort("created_at", -1)
    users = await cursor.to_list(100)
    for u in users:
        u["id"] = str(u["_id"])
        del u["_id"]
    return users

@router.get("/doctors", response_model=List[Dict[str, Any]])
async def list_doctors_verification(
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List all doctor accounts alongside their professional license profiles"""
    doctor_service = DoctorService(db)
    doctors = await doctor_service.get_doctors_list()
    return doctors

@router.post("/verify-doctor/{doctor_user_id}")
async def verify_doctor_license(
    doctor_user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Verify doctor credentials to authorize appointment booking"""
    doctor_service = DoctorService(db)
    profile = await doctor_service.verify_doctor(doctor_user_id, current_user["_id"])
    return {"message": "Doctor verified successfully", "profile": profile}
