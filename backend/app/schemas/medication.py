"""
Medication Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.medication import MedicationSchedule, AdherenceEntry

class MedicationCreate(BaseModel):
    medicine_name: str
    generic_name: Optional[str] = None
    dosage: str
    form: str = "tablet"
    schedule: MedicationSchedule
    instructions: Optional[str] = None
    special_instructions: Optional[str] = None
    initial_quantity: Optional[int] = None
    current_quantity: Optional[int] = None
    refill_reminder_at: Optional[int] = None
    reminder_enabled: bool = True
    reminder_advance_minutes: int = 0
    reminder_channels: List[str] = ["push"]

class MedicationUpdate(BaseModel):
    medicine_name: Optional[str] = None
    generic_name: Optional[str] = None
    dosage: Optional[str] = None
    form: Optional[str] = None
    schedule: Optional[MedicationSchedule] = None
    instructions: Optional[str] = None
    special_instructions: Optional[str] = None
    current_quantity: Optional[int] = None
    reminder_enabled: Optional[bool] = None
    paused: Optional[bool] = None
    pause_reason: Optional[str] = None

class LogIntakeRequest(BaseModel):
    scheduled_time: datetime
    taken: bool
    skipped: bool = False
    skip_reason: Optional[str] = None

class MedicationResponse(BaseModel):
    id: str
    patient_id: str
    medicine_name: str
    generic_name: Optional[str] = None
    dosage: str
    form: str
    schedule: MedicationSchedule
    instructions: Optional[str] = None
    special_instructions: Optional[str] = None
    initial_quantity: Optional[int] = None
    current_quantity: Optional[int] = None
    refill_reminder_at: Optional[int] = None
    last_refilled_date: Optional[datetime] = None
    adherence_log: List[AdherenceEntry] = []
    reminder_enabled: bool
    is_active: bool
    paused: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
