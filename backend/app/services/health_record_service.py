"""
Health Record Service
Business logic for vitals logging, laboratory results, and health diary
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.health_record import HealthRecord
from app.schemas.health_record import HealthRecordCreate

class HealthRecordService:
    """Service for managing patient health files and vitals tracking"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.records_collection = db.health_records

    async def get_patient_records(self, patient_id: str, record_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch health records of various categories"""
        query = {"patient_id": patient_id}
        if record_type:
            query["record_type"] = record_type
            
        records = await self.records_collection.find(query).sort("recorded_at", -1).to_list(200)
        for record in records:
            record["id"] = str(record["_id"])
        return records

    async def create_health_record(self, patient_id: str, recorder_id: str, data: HealthRecordCreate) -> Dict[str, Any]:
        """Save a new clinical or manual entry"""
        record_dict = data.dict()
        record_dict["patient_id"] = patient_id
        record_dict["recorded_by"] = recorder_id
        record_dict["created_at"] = datetime.utcnow()
        record_dict["updated_at"] = datetime.utcnow()

        # Recalculate BMI if it's vitals and height/weight are logged
        if data.record_type == "vitals" and data.vitals:
            v = data.vitals
            # Standard BMI calculation
            height_m = (v.height or 170.0) / 100.0
            weight = v.weight or 70.0
            record_dict["vitals"]["bmi"] = round(weight / (height_m * height_m), 2)

        result = await self.records_collection.insert_one(record_dict)
        
        created_rec = await self.records_collection.find_one({"_id": result.inserted_id})
        created_rec["id"] = str(created_rec["_id"])
        return created_rec

    async def get_vitals_trends(self, patient_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve vitals measurements sorted chronologically for dashboards"""
        records = await self.records_collection.find(
            {"patient_id": patient_id, "record_type": "vitals"}
        ).sort("recorded_at", 1).to_list(limit)
        
        trends = []
        for r in records:
            if r.get("vitals"):
                trends.append({
                    "recorded_at": r["recorded_at"],
                    "blood_pressure_systolic": r["vitals"].get("blood_pressure_systolic"),
                    "blood_pressure_diastolic": r["vitals"].get("blood_pressure_diastolic"),
                    "heart_rate": r["vitals"].get("heart_rate"),
                    "oxygen_saturation": r["vitals"].get("oxygen_saturation"),
                    "blood_glucose": r["vitals"].get("blood_glucose"),
                    "weight": r["vitals"].get("weight"),
                    "temperature": r["vitals"].get("temperature")
                })
        return trends
