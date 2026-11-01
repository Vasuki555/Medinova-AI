"""
Doctor Profile Service
Business logic for doctor profile management
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.doctor_profile import DoctorProfile
from app.schemas.doctor_profile import DoctorProfileCreate, DoctorProfileUpdate

class DoctorService:
    """Service for doctor profile operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.doctor_collection = db.doctor_profiles
        self.users_collection = db.users

    async def get_doctor_profile(self, user_id: str) -> Dict[str, Any]:
        """Get doctor profile. Creates default one if not found."""
        profile = await self.doctor_collection.find_one({"user_id": user_id})
        
        if not profile:
            default_profile = {
                "user_id": user_id,
                "license_number": "PENDING-" + str(user_id)[-6:],
                "license_state": "",
                "license_country": "",
                "license_expiry": None,
                "license_document_url": "",
                "specialization": "General Practitioner",
                "sub_specializations": [],
                "qualifications": [],
                "years_of_experience": 0,
                "total_consultations": 0,
                "consultation_fee": 50.0,
                "consultation_duration": 30,
                "accepts_insurance": True,
                "languages_spoken": ["English"],
                "bio": "",
                "primary_hospital_id": "",
                "affiliated_hospitals": [],
                "availability": [
                    {"day": "monday", "is_available": True, "time_slots": [{"start_time": "09:00", "end_time": "12:00", "slot_duration": 30}, {"start_time": "14:00", "end_time": "17:00", "slot_duration": 30}]},
                    {"day": "tuesday", "is_available": True, "time_slots": [{"start_time": "09:00", "end_time": "12:00", "slot_duration": 30}, {"start_time": "14:00", "end_time": "17:00", "slot_duration": 30}]},
                    {"day": "wednesday", "is_available": True, "time_slots": [{"start_time": "09:00", "end_time": "12:00", "slot_duration": 30}, {"start_time": "14:00", "end_time": "17:00", "slot_duration": 30}]},
                    {"day": "thursday", "is_available": True, "time_slots": [{"start_time": "09:00", "end_time": "12:00", "slot_duration": 30}, {"start_time": "14:00", "end_time": "17:00", "slot_duration": 30}]},
                    {"day": "friday", "is_available": True, "time_slots": [{"start_time": "09:00", "end_time": "12:00", "slot_duration": 30}, {"start_time": "14:00", "end_time": "17:00", "slot_duration": 30}]}
                ],
                "rating": 5.0,
                "review_count": 0,
                "is_verified": False,
                "verified_at": None,
                "verified_by": "",
                "is_accepting_patients": True,
                "awards": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = await self.doctor_collection.insert_one(default_profile)
            profile = await self.doctor_collection.find_one({"_id": result.inserted_id})
            
        # Hydrate user details
        try:
            # Try converting to ObjectId if it's a string
            user_oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
            user = await self.users_collection.find_one({"_id": user_oid})
            if not user:
                # If not found, try searching by string _id (mongomock might store as string)
                user = await self.users_collection.find_one({"_id": user_id})
        except Exception as e:
            # If conversion fails, try as-is
            user = await self.users_collection.find_one({"_id": user_id})
            
        if user:
            profile["first_name"] = user.get("first_name", "")
            profile["last_name"] = user.get("last_name", "")
            profile["email"] = user.get("email", "")
            profile["phone"] = user.get("phone", "")
            profile["profile_picture_url"] = user.get("profile_picture_url")

        profile["id"] = str(profile["_id"])
        return profile

    async def update_doctor_profile(self, user_id: str, profile_data: DoctorProfileUpdate) -> Dict[str, Any]:
        """Update doctor professional attributes and slots"""
        await self.get_doctor_profile(user_id)
        
        update_dict = {}
        data = profile_data.dict(exclude_unset=True)
        
        for key, val in data.items():
            if val is not None:
                update_dict[key] = val
                
        update_dict["updated_at"] = datetime.utcnow()

        await self.doctor_collection.update_one(
            {"user_id": user_id},
            {"$set": update_dict}
        )
        
        return await self.get_doctor_profile(user_id)

    async def get_doctors_list(self, specialization: Optional[str] = None, search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        """List and search verified doctors with batch user lookups"""
        # Build match query
        query = {"is_verified": True}
        if specialization:
            query["specialization"] = {"$regex": specialization, "$options": "i"}
        
        # Get verified doctor profiles
        docs = await self.doctor_collection.find(query).to_list(100)
        
        if not docs:
            return []
        
        # Collect all user_ids and convert to ObjectId
        user_ids = []
        for doc in docs:
            user_id = doc.get("user_id")
            try:
                user_oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
                user_ids.append(user_oid)
            except:
                user_ids.append(user_id)
        
        # Batch fetch all users in one query
        users = await self.users_collection.find({"_id": {"$in": user_ids}}).to_list(200)
        user_map = {str(u["_id"]): u for u in users}
        
        # Hydrate doctor docs with user info
        hydrated_docs = []
        for doc in docs:
            user_id_str = str(doc.get("user_id"))
            # Try with and without ObjectId conversion
            user = user_map.get(user_id_str)
            
            if not user:
                # Try original user_id if it's already ObjectId format
                try:
                    user_oid = ObjectId(doc.get("user_id"))
                    user_id_str = str(user_oid)
                    user = user_map.get(user_id_str)
                except:
                    pass
            
            if user:
                # Filter by search query if provided
                if search_query:
                    full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}"
                    if search_query.lower() not in full_name.lower():
                        continue
                
                # Add user fields to doctor doc
                doc["first_name"] = user.get("first_name", "")
                doc["last_name"] = user.get("last_name", "")
                doc["email"] = user.get("email", "")
                doc["phone"] = user.get("phone", "")
                doc["profile_picture_url"] = user.get("profile_picture_url")
                doc["id"] = str(doc["_id"])
                hydrated_docs.append(doc)
        
        return hydrated_docs

    async def verify_doctor(self, doctor_user_id: str, admin_user_id: str) -> Dict[str, Any]:
        """Admin action to verify a doctor"""
        await self.get_doctor_profile(doctor_user_id)
        
        await self.doctor_collection.update_one(
            {"user_id": doctor_user_id},
            {
                "$set": {
                    "is_verified": True,
                    "verified_at": datetime.utcnow(),
                    "verified_by": admin_user_id,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return await self.get_doctor_profile(doctor_user_id)
