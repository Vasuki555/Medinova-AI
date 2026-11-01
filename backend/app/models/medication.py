"""
Medication Model
MongoDB document structure for patient medications and reminders
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class TimeSlot(BaseModel):
    time: str  # "HH:MM" (e.g. "08:00")
    with_meal: str = "anytime"  # "before" | "after" | "with" | "anytime"

class MedicationSchedule(BaseModel):
    frequency: str  # "daily" | "specific_days" | "as_needed"
    times_per_day: int = 1
    time_slots: List[TimeSlot] = []
    days_of_week: List[int] = []  # 0=Monday, 1=Tuesday... 6=Sunday
    start_date: datetime
    end_date: Optional[datetime] = None
    is_ongoing: bool = True

class AdherenceEntry(BaseModel):
    scheduled_time: datetime
    taken: bool = False
    taken_at: Optional[datetime] = None
    skipped: bool = False
    skip_reason: Optional[str] = None
    noted_by: str = "user"  # "user" | "caregiver"

class Medication(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str  # Reference to User ID of patient
    
    medicine_name: str
    generic_name: Optional[str] = None
    dosage: str  # e.g., "500mg" or "1 spoon"
    form: str = "tablet"  # "tablet" | "capsule" | "syrup" | "injection" | "inhaler" | "other"
    
    schedule: MedicationSchedule
    instructions: Optional[str] = None
    special_instructions: Optional[str] = None
    
    # Stock Management
    initial_quantity: Optional[int] = None
    current_quantity: Optional[int] = None
    refill_reminder_at: Optional[int] = None
    last_refilled_date: Optional[datetime] = None
    
    adherence_log: List[AdherenceEntry] = []
    
    reminder_enabled: bool = True
    reminder_advance_minutes: int = 0
    reminder_channels: List[str] = ["push"]  # ["push", "sms", "email"]
    
    prescribed_by: Optional[str] = None  # Reference to Doctor User ID
    prescription_id: Optional[str] = None
    
    is_active: bool = True
    paused: bool = False
    pause_reason: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "patient_id": "507f1f77bcf86cd799439011",
                "medicine_name": "Paracetamol",
                "dosage": "500mg",
                "form": "tablet",
                "schedule": {
                    "frequency": "daily",
                    "times_per_day": 2,
                    "time_slots": [
                        {"time": "08:00", "with_meal": "after"},
                        {"time": "20:00", "with_meal": "after"}
                    ],
                    "start_date": "2026-07-09T00:00:00",
                    "is_ongoing": True
                },
                "instructions": "Take after meals"
            }
        }
