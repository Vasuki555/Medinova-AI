"""
Authentication Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


class UserRegisterRequest(BaseModel):
    """
    User registration request schema
    Validates all required fields for new user creation
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=100, description="User's password (min 8 characters)")
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    role: str = Field(..., description="User role: patient, doctor, or admin")
    phone: Optional[str] = Field(None, description="Phone number in E.164 format (+1234567890)")
    date_of_birth: Optional[datetime] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender: male, female, other, prefer_not_to_say")
    
    @validator("password")
    def validate_password(cls, v):
        """
        Validate password strength
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        
        return v
    
    @validator("role")
    def validate_role(cls, v):
        """Validate user role"""
        allowed_roles = ["patient", "doctor", "admin"]
        if v.lower() not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return v.lower()
    
    @validator("phone")
    def validate_phone(cls, v):
        """Validate phone number format (E.164)"""
        if v is None:
            return v
        
        # E.164 format: +[country code][number] (e.g., +14155552671)
        pattern = r"^\+?[1-9]\d{1,14}$"
        if not re.match(pattern, v):
            raise ValueError("Phone number must be in E.164 format (e.g., +14155552671)")
        
        return v
    
    @validator("gender")
    def validate_gender(cls, v):
        """Validate gender value"""
        if v is None:
            return v
        
        allowed_genders = ["male", "female", "other", "prefer_not_to_say"]
        if v.lower() not in allowed_genders:
            raise ValueError(f"Gender must be one of: {', '.join(allowed_genders)}")
        
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Doe",
                "role": "patient",
                "phone": "+14155552671",
                "gender": "male"
            }
        }


class UserLoginRequest(BaseModel):
    """
    User login request schema
    Simple email and password authentication
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!"
            }
        }


class TokenResponse(BaseModel):
    """
    Token response schema
    Returned after successful login or registration
    """
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: dict = Field(..., description="User information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "_id": "507f1f77bcf86cd799439011",
                    "email": "john.doe@example.com",
                    "role": "patient",
                    "first_name": "John",
                    "last_name": "Doe"
                }
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response schema
    Standard error format for all authentication errors
    """
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid credentials",
                "error_code": "INVALID_CREDENTIALS"
            }
        }
