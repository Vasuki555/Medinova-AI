"""
Appointment Service
Business logic for bookings and consultations management
"""

import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentStatusUpdate
from app.services.notification_service import NotificationService

class AppointmentService:
    """Service for managing appointment bookings and status updates"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.appointments_collection = db.appointments
        self.users_collection = db.users
        self.doctor_profiles = db.doctor_profiles
        self.notification_service = NotificationService(db)

    async def _generate_appointment_number(self) -> str:
        """
        Generate unique human-readable appointment number APT-YYYYMMDD-XXXX
        Includes collision detection with retry logic
        """
        date_str = datetime.utcnow().strftime("%Y%m%d")
        max_attempts = 10
        
        for attempt in range(max_attempts):
            rand_num = random.randint(1000, 9999)
            appointment_number = f"APT-{date_str}-{rand_num}"
            
            # Check if this number already exists
            existing = await self.appointments_collection.find_one(
                {"appointment_number": appointment_number}
            )
            
            if not existing:
                return appointment_number
        
        # Fallback to timestamp-based unique number if all retries fail
        timestamp = int(datetime.utcnow().timestamp() * 1000) % 10000
        return f"APT-{date_str}-{timestamp}"

    async def create_appointment(self, patient_id: str, data: AppointmentCreate) -> Dict[str, Any]:
        """Book a new appointment"""
        # Verify doctor exists
        doctor_user = await self.users_collection.find_one({"_id": ObjectId(data.doctor_id), "role": "doctor"})
        if not doctor_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found",
                headers={"error_code": "DOCTOR_NOT_FOUND"}
            )
            
        patient_user = await self.users_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        # Retrieve consultation fee
        doctor_prof = await self.doctor_profiles.find_one({"user_id": data.doctor_id})
        fee = doctor_prof.get("consultation_fee", 50.0) if doctor_prof else 50.0

        appointment_dict = {
            "appointment_number": await self._generate_appointment_number(),  # Now async
            "patient_id": patient_id,
            "doctor_id": data.doctor_id,
            "appointment_date": data.appointment_date,
            "duration_minutes": data.duration_minutes,
            "type": data.type,
            "status": "scheduled",
            "reason": data.reason,
            "symptoms": data.symptoms,
            "symptom_report_id": None,
            "consultation": None,
            "prescription_id": None,
            "video_call": {
                "room_id": f"room-{random.randint(100000, 999999)}",
                "join_url_patient": f"/telehealth/join/{patient_id}",
                "join_url_doctor": f"/telehealth/join/{data.doctor_id}",
                "recording_url": None,
                "duration_seconds": None
            },
            "payment": {
                "amount": fee,
                "currency": "USD",
                "status": "pending",
                "payment_method": None,
                "transaction_id": None,
                "paid_at": None
            },
            "cancellation": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await self.appointments_collection.insert_one(appointment_dict)
        inserted_id = result.inserted_id
        
        # Create notifications
        await self.notification_service.create_notification(
            user_id=data.doctor_id,
            type="appointment",
            category="info",
            title="New Appointment Scheduled",
            message=f"Patient {patient_user.get('first_name')} booked a session on {data.appointment_date.strftime('%Y-%m-%d %H:%M')}.",
            action_url="/doctor/dashboard",
            action_text="View Queue"
        )
        
        await self.notification_service.create_notification(
            user_id=patient_id,
            type="appointment",
            category="success",
            title="Appointment Booked Successfully",
            message=f"Your appointment with Dr. {doctor_user.get('last_name')} is scheduled for {data.appointment_date.strftime('%Y-%m-%d %H:%M')}.",
            action_url="/patient/dashboard",
            action_text="View Details"
        )

        created_apt = await self.appointments_collection.find_one({"_id": inserted_id})
        created_apt["id"] = str(created_apt["_id"])
        return created_apt

    async def get_user_appointments(self, user_id: str, role: str) -> List[Dict[str, Any]]:
        """Retrieve patient or doctor bookings log"""
        query = {"patient_id": user_id} if role == "patient" else {"doctor_id": user_id}
        
        appointments = await self.appointments_collection.find(query).sort("appointment_date", -1).to_list(200)
        
        hydrated = []
        for apt in appointments:
            apt["id"] = str(apt["_id"])
            
            # Fetch doctor details
            doc_user = await self.users_collection.find_one({"_id": ObjectId(apt["doctor_id"])})
            if doc_user:
                apt["doctor_name"] = f"Dr. {doc_user.get('first_name')} {doc_user.get('last_name')}"
                doc_prof = await self.doctor_profiles.find_one({"user_id": apt["doctor_id"]})
                if doc_prof:
                    apt["doctor_specialization"] = doc_prof.get("specialization", "General Practitioner")
                    
            # Fetch patient details
            pat_user = await self.users_collection.find_one({"_id": ObjectId(apt["patient_id"])})
            if pat_user:
                apt["patient_name"] = f"{pat_user.get('first_name')} {pat_user.get('last_name')}"

            hydrated.append(apt)
            
        return hydrated

    async def update_appointment_status(self, appointment_id: str, user_id: str, role: str, data: AppointmentStatusUpdate) -> Dict[str, Any]:
        """State transitions for appointments"""
        apt = await self.appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        if not apt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

        # Authorization checks
        if role == "patient" and apt["patient_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        if role == "doctor" and apt["doctor_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        update_fields = {
            "status": data.status,
            "updated_at": datetime.utcnow()
        }

        if data.status == "cancelled":
            update_fields["cancellation"] = {
                "cancelled_by": user_id,
                "cancelled_at": datetime.utcnow(),
                "reason": data.cancellation_reason or "Cancelled by user",
                "refund_amount": apt["payment"].get("amount", 0.0) if apt["payment"].get("status") == "paid" else 0.0
            }
        elif data.status == "completed":
            update_fields["completed_at"] = datetime.utcnow()

        await self.appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": update_fields}
        )

        # Notify the counter-party
        notify_user_id = apt["doctor_id"] if role == "patient" else apt["patient_id"]
        status_label = data.status.capitalize()
        await self.notification_service.create_notification(
            user_id=notify_user_id,
            type="appointment",
            category="warning" if data.status == "cancelled" else "success",
            title=f"Appointment {status_label}",
            message=f"Appointment {apt['appointment_number']} has been {data.status}.",
            action_url="/patient/dashboard" if role == "doctor" else "/doctor/dashboard",
            action_text="View Session"
        )

        updated_apt = await self.appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        updated_apt["id"] = str(updated_apt["_id"])
        return updated_apt

    async def update_consultation(self, appointment_id: str, doctor_id: str, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Doctor writes notes, vital logs, and diagnoses"""
        apt = await self.appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        if not apt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        if apt["doctor_id"] != doctor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        # Set default values for consultation details
        consultation_fields = {
            "started_at": consultation_data.get("started_at", datetime.utcnow()),
            "ended_at": datetime.utcnow(),
            "actual_duration": consultation_data.get("actual_duration", 30),
            "notes": consultation_data.get("notes"),
            "diagnosis": consultation_data.get("diagnosis"),
            "icd10_codes": consultation_data.get("icd10_codes", []),
            "lab_tests_ordered": consultation_data.get("lab_tests_ordered", []),
            "imaging_ordered": consultation_data.get("imaging_ordered", []),
            "follow_up_required": consultation_data.get("follow_up_required", False),
            "follow_up_days": consultation_data.get("follow_up_days"),
            "vitals": consultation_data.get("vitals")
        }

        await self.appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {
                "$set": {
                    "consultation": consultation_fields,
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )

        # Increment total consultations for doctor
        await self.doctor_profiles.update_one(
            {"user_id": doctor_id},
            {"$inc": {"total_consultations": 1}}
        )

        # Auto-generate a health record for this consultation in patient history
        if consultation_data.get("vitals"):
            db_vitals = consultation_data["vitals"]
            vitals_record = {
                "patient_id": apt["patient_id"],
                "record_type": "vitals",
                "recorded_at": datetime.utcnow(),
                "vitals": {
                    "blood_pressure_systolic": float(db_vitals.get("blood_pressure", "120/80").split("/")[0]) if "/" in db_vitals.get("blood_pressure", "") else 120.0,
                    "blood_pressure_diastolic": float(db_vitals.get("blood_pressure", "120/80").split("/")[1]) if "/" in db_vitals.get("blood_pressure", "") else 80.0,
                    "heart_rate": db_vitals.get("heart_rate"),
                    "temperature": db_vitals.get("temperature"),
                    "oxygen_saturation": db_vitals.get("oxygen_saturation"),
                    "weight": db_vitals.get("weight"),
                    "height": db_vitals.get("height")
                },
                "recorded_by": doctor_id,
                "source": "doctor",
                "appointment_id": appointment_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            await self.db.health_records.insert_one(vitals_record)

        updated_apt = await self.appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        updated_apt["id"] = str(updated_apt["_id"])
        return updated_apt
