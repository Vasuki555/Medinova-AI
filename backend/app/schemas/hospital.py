"""
Hospital Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class LocationSchema(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class HospitalResponse(BaseModel):
    id: str
    name: str
    address: str
    location: Optional[LocationSchema] = None
    phone: Optional[str] = None
    emergency_available: bool = False
    services: List[str] = []
    type: str  # "Government" or "Private"
    city: Optional[str] = None
    state: Optional[str] = None
    distance_km: Optional[float] = None
    rating: Optional[float] = None
    verified: Optional[bool] = None
    created_at: Optional[datetime] = None
    source: Optional[str] = None  # "database" or "google_places"
    place_id: Optional[str] = None  # Google Places ID
    user_ratings_total: Optional[int] = None  # Number of Google reviews
    is_open: Optional[bool] = None  # Currently open/closed (from Google)

    class Config:
        populate_by_name = True
        from_attributes = True

class HospitalCreate(BaseModel):
    name: str
    address: str
    location: LocationSchema
    phone: Optional[str] = None
    emergency_available: bool = False
    services: List[str] = []
    type: str = "government"
    city: Optional[str] = None
    state: Optional[str] = None
    rating: Optional[float] = 4.0

