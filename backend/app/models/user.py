"""
User Model
MongoDB document structure for users collection
Following approved database schema from MediNova_MongoDB_Database_Design.md
"""

from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class UserRole:
    """User role constants"""
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class UserInDB(BaseModel):
    """
    User document structure in MongoDB
    Maps to 'users' collection in database
    """
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    password_hash: str
    role: str  # "patient" | "doctor" | "admin"
    first_name: str
    last_name: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None  # "male" | "female" | "other" | "prefer_not_to_say"
    profile_picture_url: Optional[str] = None
    
    # Account Status
    is_active: bool = True
    is_email_verified: bool = False
    is_phone_verified: bool = False
    email_verification_token: Optional[str] = None
    email_verification_expires: Optional[datetime] = None
    
    # Security
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    failed_login_attempts: int = 0
    account_locked_until: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password_hash": "$2b$12$...",
                "role": "patient",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+14155552671",
                "is_active": True,
                "is_email_verified": False,
                "created_at": "2026-07-03T10:00:00"
            }
        }


class UserResponse(BaseModel):
    """
    User response model (excludes sensitive data)
    Returned to client after authentication
    """
    id: str = Field(..., alias="_id")
    email: EmailStr
    role: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "john.doe@example.com",
                "role": "patient",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+14155552671",
                "is_active": True,
                "is_email_verified": False,
                "created_at": "2026-07-03T10:00:00"
            }
        }


def user_helper(user: dict) -> dict:
    """
    Convert MongoDB user document to response format
    Removes sensitive fields like password_hash
    """
    return {
        "_id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "phone": user.get("phone"),
        "profile_picture_url": user.get("profile_picture_url"),
        "is_active": user["is_active"],
        "is_email_verified": user["is_email_verified"],
        "created_at": user["created_at"],
        "last_login_at": user.get("last_login_at")
    }
