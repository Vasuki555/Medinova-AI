"""
Patient Profile Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.models.patient_profile import Allergy, ChronicCondition, PastSurgery, FamilyHistory, EmergencyContact, InsuranceInfo, Preferences

class PatientProfileCreate(BaseModel):
    blood_group: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: List[Allergy] = []
    chronic_conditions: List[ChronicCondition] = []
    past_surgeries: List[PastSurgery] = []
    family_history: List[FamilyHistory] = []
    emergency_contact: Optional[EmergencyContact] = None
    insurance: Optional[InsuranceInfo] = None
    preferences: Optional[Preferences] = None

class PatientProfileUpdate(BaseModel):
    blood_group: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: Optional[List[Allergy]] = None
    chronic_conditions: Optional[List[ChronicCondition]] = None
    past_surgeries: Optional[List[PastSurgery]] = None
    family_history: Optional[List[FamilyHistory]] = None
    emergency_contact: Optional[EmergencyContact] = None
    insurance: Optional[InsuranceInfo] = None
    preferences: Optional[Preferences] = None

class PatientProfileResponse(BaseModel):
    id: Optional[str] = None
    user_id: str
    blood_group: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    allergies: List[Allergy] = []
    chronic_conditions: List[ChronicCondition] = []
    past_surgeries: List[PastSurgery] = []
    family_history: List[FamilyHistory] = []
    emergency_contact: Optional[EmergencyContact] = None
    insurance: Optional[InsuranceInfo] = None
    preferences: Preferences
    created_at: datetime
    updated_at: datetime
    last_health_check: Optional[datetime] = None

    class Config:
        populate_by_name = True
