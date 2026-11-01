"""
Patient Profile Model
MongoDB document structure for patient profiles
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class Allergy(BaseModel):
    allergen: str
    type: str  # "drug" | "food" | "environmental"
    severity: str  # "mild" | "moderate" | "severe"
    reaction: Optional[str] = None
    diagnosed_date: Optional[datetime] = None
    notes: Optional[str] = None

class ChronicCondition(BaseModel):
    condition: str
    icd10_code: Optional[str] = None
    diagnosed_date: Optional[datetime] = None
    status: str  # "active" | "resolved" | "controlled"
    medications: List[str] = []
    notes: Optional[str] = None

class PastSurgery(BaseModel):
    surgery_name: str
    date: Optional[datetime] = None
    hospital: Optional[str] = None
    surgeon: Optional[str] = None
    complications: Optional[str] = None
    notes: Optional[str] = None

class FamilyHistory(BaseModel):
    condition: str
    relationship: str
    age_of_onset: Optional[int] = None
    notes: Optional[str] = None

class EmergencyContact(BaseModel):
    name: str
    relationship: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class InsuranceInfo(BaseModel):
    provider: Optional[str] = None
    policy_number: Optional[str] = None
    group_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    coverage_type: Optional[str] = None

class Preferences(BaseModel):
    preferred_hospital_id: Optional[str] = None
    preferred_pharmacy: Optional[str] = None
    language: str = "en"
    communication_preference: str = "both"  # "email" | "sms" | "both"

class PatientProfile(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str  # Reference to User ID
    
    blood_group: Optional[str] = None  # "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    
    allergies: List[Allergy] = []
    chronic_conditions: List[ChronicCondition] = []
    past_surgeries: List[PastSurgery] = []
    family_history: List[FamilyHistory] = []
    
    emergency_contact: Optional[EmergencyContact] = None
    insurance: Optional[InsuranceInfo] = None
    preferences: Preferences = Field(default_factory=Preferences)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_health_check: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "blood_group": "O+",
                "height_cm": 178.5,
                "weight_kg": 75.0,
                "bmi": 23.5,
                "allergies": [
                    {"allergen": "Penicillin", "type": "drug", "severity": "severe", "reaction": "Hives"}
                ],
                "chronic_conditions": [
                    {"condition": "Hypertension", "status": "controlled"}
                ]
            }
        }
