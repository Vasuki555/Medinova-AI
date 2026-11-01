"""
Doctor Profile Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.doctor_profile import Qualification, AvailabilityDay, Award, AffiliatedHospital

class DoctorProfileCreate(BaseModel):
    license_number: str
    license_state: Optional[str] = None
    license_country: Optional[str] = None
    license_expiry: Optional[datetime] = None
    license_document_url: Optional[str] = None
    specialization: str
    sub_specializations: List[str] = []
    qualifications: List[Qualification] = []
    years_of_experience: int = 0
    consultation_fee: float = 0.0
    consultation_duration: int = 30
    accepts_insurance: bool = True
    languages_spoken: List[str] = ["English"]
    bio: Optional[str] = None
    primary_hospital_id: Optional[str] = None
    availability: List[AvailabilityDay] = []

class DoctorProfileUpdate(BaseModel):
    specialization: Optional[str] = None
    sub_specializations: Optional[List[str]] = None
    qualifications: Optional[List[Qualification]] = None
    years_of_experience: Optional[int] = None
    consultation_fee: Optional[float] = None
    consultation_duration: Optional[int] = None
    accepts_insurance: Optional[bool] = None
    languages_spoken: Optional[List[str]] = None
    bio: Optional[str] = None
    primary_hospital_id: Optional[str] = None
    availability: Optional[List[AvailabilityDay]] = None
    is_accepting_patients: Optional[bool] = None
    awards: Optional[List[Award]] = None

class DoctorProfileResponse(BaseModel):
    id: Optional[str] = None
    user_id: str
    
    # User details (hydrated from users collection)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    
    # Doctor profile fields
    license_number: Optional[str] = None
    specialization: str
    sub_specializations: List[str] = []
    qualifications: List[str] = []  # Changed from List[Qualification] to List[str] to support simple string format
    years_of_experience: int
    consultation_fee: float
    consultation_duration: int
    accepts_insurance: bool
    languages_spoken: List[str]
    bio: Optional[str] = None
    primary_hospital_id: Optional[str] = None
    affiliated_hospitals: List[AffiliatedHospital] = []
    availability: List[AvailabilityDay] = []
    rating: float
    review_count: int
    is_verified: bool
    is_accepting_patients: bool
    awards: List[Award] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
