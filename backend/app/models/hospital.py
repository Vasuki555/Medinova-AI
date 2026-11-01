"""
Hospital Model
MongoDB document structure for hospitals and clinics
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class GeoLocation(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class HospitalAddress(BaseModel):
    street: Optional[str] = None
    city: str
    state: str
    country: str
    postal_code: Optional[str] = None
    location: GeoLocation

class HospitalFacilities(BaseModel):
    emergency_services: bool = True
    icu_beds: int = 0
    general_beds: int = 0
    operation_theaters: int = 0
    pharmacy: bool = True
    laboratory: bool = True
    ambulance_service: bool = True
    parking_available: bool = True

class OperatingHour(BaseModel):
    day: str  # "monday", "tuesday", etc.
    open_time: str = "00:00"
    close_time: str = "23:59"
    is_24_7: bool = True

class Hospital(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    hospital_id: str  # Unique slug or identifier
    name: str
    type: str = "hospital"  # "hospital" | "clinic" | "diagnostic_center"
    
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    address: HospitalAddress
    services: List[str] = []
    specialties: List[str] = []
    facilities: HospitalFacilities = Field(default_factory=HospitalFacilities)
    
    operating_hours: List[OperatingHour] = []
    insurance_accepted: List[str] = []
    
    rating: float = 4.0
    review_count: int = 0
    
    is_verified: bool = False
    is_active: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "hospital_id": "govt-civil-hospital",
                "name": "District Civil Hospital",
                "type": "hospital",
                "address": {
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "country": "India",
                    "location": {
                        "type": "Point",
                        "coordinates": [72.8777, 19.0760]
                    }
                },
                "services": ["Emergency", "General Ward", "OPD"],
                "facilities": {
                    "emergency_services": True,
                    "icu_beds": 10,
                    "general_beds": 100,
                    "pharmacy": True
                }
            }
        }
