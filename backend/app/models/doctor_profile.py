"""
Doctor Profile Model
MongoDB document structure for doctor profiles
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Qualification(BaseModel):
    degree: str  # e.g., "MBBS", "MD"
    institution: str
    year: int
    country: Optional[str] = None

class TimeSlot(BaseModel):
    start_time: str  # "HH:MM" (e.g., "09:00")
    end_time: str    # "HH:MM" (e.g., "17:00")
    slot_duration: int = 30  # minutes

class AvailabilityDay(BaseModel):
    day: str  # "monday", "tuesday", etc.
    is_available: bool = True
    time_slots: List[TimeSlot] = []

class Award(BaseModel):
    title: str
    organization: str
    year: int
    description: Optional[str] = None

class AffiliatedHospital(BaseModel):
    hospital_id: str
    position: Optional[str] = None  # e.g., "Staff", "Consultant"
    department: Optional[str] = None
    since: Optional[datetime] = None

class DoctorProfile(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str  # Reference to User ID
    
    license_number: str
    license_state: Optional[str] = None
    license_country: Optional[str] = None
    license_expiry: Optional[datetime] = None
    license_document_url: Optional[str] = None
    
    specialization: str
    sub_specializations: List[str] = []
    qualifications: List[Qualification] = []
    
    years_of_experience: int = 0
    total_consultations: int = 0
    consultation_fee: float = 0.0
    consultation_duration: int = 30  # minutes
    accepts_insurance: bool = True
    languages_spoken: List[str] = ["English"]
    
    bio: Optional[str] = None
    primary_hospital_id: Optional[str] = None  # Reference to Hospital ID
    affiliated_hospitals: List[AffiliatedHospital] = []
    
    availability: List[AvailabilityDay] = []
    
    rating: float = 5.0
    review_count: int = 0
    
    is_verified: bool = False
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None  # Reference to Admin User ID
    is_accepting_patients: bool = True
    
    awards: List[Award] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439022",
                "license_number": "DOC-123456",
                "specialization": "Cardiology",
                "consultation_fee": 150.0,
                "is_verified": False,
                "availability": [
                    {
                        "day": "monday",
                        "is_available": True,
                        "time_slots": [{"start_time": "09:00", "end_time": "12:00", "slot_duration": 30}]
                    }
                ]
            }
        }
