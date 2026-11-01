"""
Health Record Model
MongoDB document structure for vitals, laboratory tests, diagnoses, and general notes
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class VitalSigns(BaseModel):
    blood_pressure_systolic: Optional[float] = None
    blood_pressure_diastolic: Optional[float] = None
    heart_rate: Optional[float] = None  # BPM
    respiratory_rate: Optional[float] = None  # breaths per minute
    oxygen_saturation: Optional[float] = None  # SpO2 percentage
    temperature: Optional[float] = None  # Celsius
    temperature_location: Optional[str] = None  # "oral", "armpit", "ear"
    weight: Optional[float] = None  # kg
    height: Optional[float] = None  # cm
    bmi: Optional[float] = None
    blood_glucose: Optional[float] = None  # mg/dL

class LabResultItem(BaseModel):
    parameter: str
    value: float
    unit: str
    reference_range: Optional[str] = None
    is_abnormal: bool = False

class LabTestDetails(BaseModel):
    test_name: str
    lab_name: Optional[str] = None
    ordered_by: Optional[str] = None  # Doctor User ID
    results: List[LabResultItem] = []
    report_document_id: Optional[str] = None

class DiagnosisDetails(BaseModel):
    condition: str
    icd10_code: Optional[str] = None
    diagnosed_by: Optional[str] = None  # Doctor User ID
    severity: str = "moderate"  # "mild" | "moderate" | "severe"
    notes: Optional[str] = None

class GeneralNoteDetails(BaseModel):
    title: str
    content: str
    category: str = "general"  # "symptom" | "medication" | "lifestyle" | "general"

class HealthRecord(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str  # Reference to User ID of patient
    
    record_type: str  # "vitals" | "lab_test" | "diagnosis" | "note"
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    
    vitals: Optional[VitalSigns] = None
    lab_test: Optional[LabTestDetails] = None
    diagnosis: Optional[DiagnosisDetails] = None
    note: Optional[GeneralNoteDetails] = None
    
    recorded_by: str  # User ID of recorder
    source: str = "manual"  # "manual" | "device" | "doctor" | "lab"
    device_name: Optional[str] = None
    
    appointment_id: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "patient_id": "507f1f77bcf86cd799439011",
                "record_type": "vitals",
                "recorded_at": "2026-07-09T08:00:00",
                "vitals": {
                    "blood_pressure_systolic": 120.0,
                    "blood_pressure_diastolic": 80.0,
                    "heart_rate": 72.0,
                    "temperature": 36.6,
                    "oxygen_saturation": 98.0
                },
                "recorded_by": "507f1f77bcf86cd799439011",
                "source": "manual"
            }
        }
