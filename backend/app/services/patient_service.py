"""
Patient Profile Service
Business logic for patient profile management
"""

from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.patient_profile import PatientProfile
from app.schemas.patient_profile import PatientProfileCreate, PatientProfileUpdate

class PatientService:
    """Service for patient profile operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.patient_collection = db.patient_profiles
        self.users_collection = db.users

    def _calculate_bmi(self, height_cm: Optional[float], weight_kg: Optional[float]) -> Optional[float]:
        """Helper to calculate BMI"""
        if not height_cm or not weight_kg or height_cm <= 0:
            return None
        height_m = height_cm / 100.0
        return round(weight_kg / (height_m * height_m), 2)

    async def get_patient_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get patient profile. If it doesn't exist, create a blank one.
        """
        profile = await self.patient_collection.find_one({"user_id": user_id})
        
        if not profile:
            # Create a default blank profile
            default_profile = {
                "user_id": user_id,
                "blood_group": None,
                "height_cm": None,
                "weight_kg": None,
                "bmi": None,
                "allergies": [],
                "chronic_conditions": [],
                "past_surgeries": [],
                "family_history": [],
                "emergency_contact": None,
                "insurance": None,
                "preferences": {
                    "preferred_hospital_id": None,
                    "preferred_pharmacy": None,
                    "language": "en",
                    "communication_preference": "both"
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_health_check": None
            }
            result = await self.patient_collection.insert_one(default_profile)
            profile = await self.patient_collection.find_one({"_id": result.inserted_id})
        
        # Hydrate user details
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            profile["first_name"] = user.get("first_name", "")
            profile["last_name"] = user.get("last_name", "")
            profile["email"] = user.get("email", "")
            profile["phone"] = user.get("phone", "")
            profile["gender"] = user.get("gender", "")
            profile["date_of_birth"] = user.get("date_of_birth")
            profile["profile_picture_url"] = user.get("profile_picture_url")

        profile["id"] = str(profile["_id"])
        return profile

    async def update_patient_profile(self, user_id: str, profile_data: PatientProfileUpdate) -> Dict[str, Any]:
        """Update patient profile and recalculate BMI"""
        # Ensure profile exists
        await self.get_patient_profile(user_id)
        
        update_dict = {}
        data = profile_data.dict(exclude_unset=True)
        
        # Calculate BMI if height or weight is updated
        if "height_cm" in data or "weight_kg" in data:
            current_profile = await self.patient_collection.find_one({"user_id": user_id})
            height = data.get("height_cm", current_profile.get("height_cm"))
            weight = data.get("weight_kg", current_profile.get("weight_kg"))
            data["bmi"] = self._calculate_bmi(height, weight)
            data["last_health_check"] = datetime.utcnow()

        for key, val in data.items():
            if val is not None:
                update_dict[key] = val
                
        update_dict["updated_at"] = datetime.utcnow()

        await self.patient_collection.update_one(
            {"user_id": user_id},
            {"$set": update_dict}
        )
        
        return await self.get_patient_profile(user_id)
