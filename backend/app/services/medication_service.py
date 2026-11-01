"""
Medication Service
Business logic for medicine schedules, logs, and stock alerts
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.medication import Medication
from app.schemas.medication import MedicationCreate, MedicationUpdate, LogIntakeRequest
from app.services.notification_service import NotificationService

class MedicationService:
    """Service for managing patient medications and reminders"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.medications_collection = db.medications
        self.notification_service = NotificationService(db)

    async def get_patient_medications(self, patient_id: str) -> List[Dict[str, Any]]:
        """Fetch list of medications for a patient"""
        meds = await self.medications_collection.find({"patient_id": patient_id}).to_list(100)
        for med in meds:
            med["id"] = str(med["_id"])
        return meds

    async def create_medication(self, patient_id: str, data: MedicationCreate) -> Dict[str, Any]:
        """Add new medication schedule"""
        med_dict = data.dict()
        med_dict["patient_id"] = patient_id
        med_dict["is_active"] = True
        med_dict["paused"] = False
        med_dict["pause_reason"] = None
        med_dict["adherence_log"] = []
        med_dict["last_refilled_date"] = datetime.utcnow()
        med_dict["created_at"] = datetime.utcnow()
        med_dict["updated_at"] = datetime.utcnow()

        result = await self.medications_collection.insert_one(med_dict)
        
        await self.notification_service.create_notification(
            user_id=patient_id,
            type="medication",
            category="success",
            title="Medication Reminder Configured",
            message=f"Reminder created for {data.medicine_name} ({data.dosage}).",
            action_url="/patient/dashboard",
            action_text="View Reminders"
        )
        
        created_med = await self.medications_collection.find_one({"_id": result.inserted_id})
        created_med["id"] = str(created_med["_id"])
        return created_med

    async def update_medication(self, patient_id: str, medication_id: str, data: MedicationUpdate) -> Dict[str, Any]:
        """Update existing medication details"""
        med = await self.medications_collection.find_one({"_id": ObjectId(medication_id), "patient_id": patient_id})
        if not med:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication record not found")
            
        update_fields = data.dict(exclude_unset=True)
        update_fields["updated_at"] = datetime.utcnow()

        await self.medications_collection.update_one(
            {"_id": ObjectId(medication_id)},
            {"$set": update_fields}
        )
        
        updated_med = await self.medications_collection.find_one({"_id": ObjectId(medication_id)})
        updated_med["id"] = str(updated_med["_id"])
        return updated_med

    async def log_medication_intake(self, patient_id: str, medication_id: str, data: LogIntakeRequest) -> Dict[str, Any]:
        """Log whether medication was taken or skipped"""
        med = await self.medications_collection.find_one({"_id": ObjectId(medication_id), "patient_id": patient_id})
        if not med:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication record not found")

        adherence_entry = {
            "scheduled_time": data.scheduled_time,
            "taken": data.taken,
            "taken_at": datetime.utcnow() if data.taken else None,
            "skipped": data.skipped,
            "skip_reason": data.skip_reason,
            "noted_by": "user"
        }

        # Decrement quantity on intake
        quantity_update = {}
        if data.taken and med.get("current_quantity") is not None:
            current_qty = med["current_quantity"]
            new_qty = max(0, current_qty - 1)
            quantity_update["current_quantity"] = new_qty
            
            # Check stock levels
            refill_threshold = med.get("refill_reminder_at", 5)
            if new_qty <= refill_threshold:
                await self.notification_service.create_notification(
                    user_id=patient_id,
                    type="reminder",
                    category="warning",
                    title="Low Medication Stock",
                    message=f"You only have {new_qty} pills of {med['medicine_name']} left. Please refill soon.",
                    action_url="/patient/dashboard",
                    action_text="Refill Medicine"
                )

        await self.medications_collection.update_one(
            {"_id": ObjectId(medication_id)},
            {
                "$push": {"adherence_log": adherence_entry},
                "$set": {
                    "updated_at": datetime.utcnow(),
                    **quantity_update
                }
            }
        )

        updated_med = await self.medications_collection.find_one({"_id": ObjectId(medication_id)})
        updated_med["id"] = str(updated_med["_id"])
        return updated_med

    async def delete_medication(self, patient_id: str, medication_id: str) -> bool:
        """Deactivate or soft delete a medication"""
        result = await self.medications_collection.delete_one({"_id": ObjectId(medication_id), "patient_id": patient_id})
        return result.deleted_count > 0
