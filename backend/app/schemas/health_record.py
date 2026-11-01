"""
Health Record Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.health_record import VitalSigns, LabTestDetails, DiagnosisDetails, GeneralNoteDetails

class HealthRecordCreate(BaseModel):
    record_type: str  # "vitals" | "lab_test" | "diagnosis" | "note"
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    vitals: Optional[VitalSigns] = None
    lab_test: Optional[LabTestDetails] = None
    diagnosis: Optional[DiagnosisDetails] = None
    note: Optional[GeneralNoteDetails] = None
    source: str = "manual"
    device_name: Optional[str] = None
    appointment_id: Optional[str] = None

class HealthRecordResponse(BaseModel):
    id: str
    patient_id: str
    record_type: str
    recorded_at: datetime
    vitals: Optional[VitalSigns] = None
    lab_test: Optional[LabTestDetails] = None
    diagnosis: Optional[DiagnosisDetails | str] = None  # Accept both object and legacy string format
    note: Optional[GeneralNoteDetails] = None
    recorded_by: Optional[str] = None  # Made optional for legacy records from document upload
    source: str
    device_name: Optional[str] = None
    appointment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
