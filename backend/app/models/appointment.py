"""
Appointment Model
MongoDB document structure for appointments
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class VitalsRecorded(BaseModel):
    blood_pressure: Optional[str] = None  # e.g., "120/80"
    heart_rate: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None

class ConsultationDetails(BaseModel):
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    actual_duration: Optional[int] = None
    
    notes: Optional[str] = None
    diagnosis: Optional[str] = None
    icd10_codes: List[str] = []
    
    lab_tests_ordered: List[str] = []
    imaging_ordered: List[str] = []
    follow_up_required: bool = False
    follow_up_days: Optional[int] = None
    vitals: Optional[VitalsRecorded] = None

class VideoCallDetails(BaseModel):
    room_id: Optional[str] = None
    join_url_patient: Optional[str] = None
    join_url_doctor: Optional[str] = None
    recording_url: Optional[str] = None
    duration_seconds: Optional[int] = None

class PaymentDetails(BaseModel):
    amount: float = 0.0
    currency: str = "USD"
    status: str = "pending"  # "pending" | "paid" | "refunded"
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None

class CancellationDetails(BaseModel):
    cancelled_by: Optional[str] = None  # User ID
    cancelled_at: Optional[datetime] = None
    reason: Optional[str] = None
    refund_amount: float = 0.0

class Appointment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    appointment_number: str
    
    patient_id: str  # User ID of patient
    doctor_id: str  # User ID of doctor
    
    appointment_date: datetime
    duration_minutes: int = 30
    
    type: str = "video"  # "video" | "in_person" | "chat"
    status: str = "scheduled"  # "scheduled" | "confirmed" | "in_progress" | "completed" | "cancelled" | "no_show"
    
    reason: str
    symptoms: List[str] = []
    symptom_report_id: Optional[str] = None
    
    consultation: Optional[ConsultationDetails] = None
    prescription_id: Optional[str] = None
    video_call: Optional[VideoCallDetails] = None
    payment: PaymentDetails = Field(default_factory=PaymentDetails)
    cancellation: Optional[CancellationDetails] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "appointment_number": "APT-20260709-0001",
                "patient_id": "507f1f77bcf86cd799439011",
                "doctor_id": "507f1f77bcf86cd799439022",
                "appointment_date": "2026-07-09T14:00:00",
                "duration_minutes": 30,
                "type": "video",
                "status": "scheduled",
                "reason": "Routine checkup"
            }
        }
