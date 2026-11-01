"""
Appointment Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.appointment import ConsultationDetails, PaymentDetails, CancellationDetails, VideoCallDetails

class AppointmentCreate(BaseModel):
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int = 30
    type: str = "video"  # "video" | "in_person" | "chat"
    reason: str
    symptoms: List[str] = []

class AppointmentStatusUpdate(BaseModel):
    status: str  # "scheduled" | "confirmed" | "in_progress" | "completed" | "cancelled" | "no_show"
    cancellation_reason: Optional[str] = None

class AppointmentConsultationUpdate(BaseModel):
    consultation: ConsultationDetails

class AppointmentResponse(BaseModel):
    id: str
    appointment_number: str
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int
    type: str
    status: str
    reason: str
    symptoms: List[str] = []
    consultation: Optional[ConsultationDetails] = None
    prescription_id: Optional[str] = None
    video_call: Optional[VideoCallDetails] = None
    payment: PaymentDetails
    cancellation: Optional[CancellationDetails] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    # Custom fields for UI display convenience (hydrated by router/service)
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_specialization: Optional[str] = None

    class Config:
        populate_by_name = True
