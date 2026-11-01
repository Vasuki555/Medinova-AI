"""
OAuth Authentication Router
Google OAuth 2.0 integration for social login
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, EmailStr
from bson import ObjectId
import httpx

from app.database import get_database
from app.config import settings
from app.utils.security import create_access_token, create_refresh_token, hash_password
from app.core.dependencies import get_current_user
from app.core.rate_limit import limiter

router = APIRouter(prefix="/oauth", tags=["OAuth"])


class GoogleTokenRequest(BaseModel):
    """Google OAuth token exchange request"""
    code: str
    redirect_uri: str


class GoogleUserInfo(BaseModel):
    """Google user information"""
    id: str
    email: EmailStr
    given_name: str
    family_name: Optional[str] = None
    picture: Optional[str] = None
    verified_email: bool


@router.get("/google/url")
async def get_google_oauth_url():
    """
    Generate Google OAuth authorization URL.
    
    **Frontend Flow:**
    1. User clicks "Sign in with Google"
    2. Frontend calls this endpoint
    3. Frontend redirects user to returned URL
    4. User authorizes on Google
    5. Google redirects back to frontend with code
    6. Frontend calls /oauth/google/callback with code
    """
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth not configured. Set GOOGLE_CLIENT_ID in environment."
        )
    
    # Generate state token for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Build OAuth URL
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account"
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    
    return {
        "auth_url": auth_url,
        "state": state
    }


@router.post("/google/callback")
@limiter.limit("10/minute")
async def google_oauth_callback(
    request: Request,
    response: Response,
    token_request: GoogleTokenRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Handle Google OAuth callback.
    
    **Process:**
    1. Exchange authorization code for access token
    2. Fetch user info from Google
    3. Create or update user in database
    4. Return JWT tokens for MediNova session
    """
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth not configured"
        )
    
    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        try:
            # Token exchange
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": token_request.code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": token_request.redirect_uri,
                    "grant_type": "authorization_code"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange authorization code"
                )
            
            token_data = token_response.json()
            google_access_token = token_data.get("access_token")
            
            # Fetch user info from Google
            user_info_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {google_access_token}"}
            )
            
            if user_info_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to fetch user information from Google"
                )
            
            google_user = user_info_response.json()
            
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to communicate with Google: {str(e)}"
            )
    
    # Check if user already exists
    email = google_user.get("email")
    existing_user = await db.users.find_one({"email": email})
    
    if existing_user:
        # User exists - update profile picture and last login
        await db.users.update_one(
            {"_id": existing_user["_id"]},
            {
                "$set": {
                    "profile_picture_url": google_user.get("picture"),
                    "last_login_at": datetime.utcnow(),
                    "is_email_verified": True,  # Google verified
                    "oauth_provider": "google",
                    "oauth_google_id": google_user.get("sub")
                }
            }
        )
        user_id = str(existing_user["_id"])
        role = existing_user.get("role", "patient")
    
    else:
        # New user - create account
        new_user = {
            "email": email,
            "password_hash": hash_password(secrets.token_urlsafe(32)),  # Random password
            "first_name": google_user.get("given_name", ""),
            "last_name": google_user.get("family_name", ""),
            "role": "patient",  # Default role for OAuth users
            "phone": None,
            "profile_picture_url": google_user.get("picture"),
            "is_active": True,
            "is_email_verified": True,  # Google verified
            "created_at": datetime.utcnow(),
            "last_login_at": datetime.utcnow(),
            "failed_login_attempts": 0,
            "account_locked_until": None,
            "oauth_provider": "google",
            "oauth_google_id": google_user.get("sub")
        }
        
        result = await db.users.insert_one(new_user)
        user_id = str(result.inserted_id)
        role = "patient"
        
        # Create patient profile
        patient_profile = {
            "user_id": user_id,
            "date_of_birth": None,
            "gender": None,
            "blood_type": None,
            "height_cm": None,
            "weight_kg": None,
            "allergies": [],
            "chronic_conditions": [],
            "emergency_contact_name": None,
            "emergency_contact_phone": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await db.patient_profiles.insert_one(patient_profile)
    
    # Generate JWT tokens for MediNova session
    access_token = create_access_token({"sub": user_id, "role": role})
    refresh_token = create_refresh_token({"sub": user_id})
    
    # Fetch complete user object
    user_doc = await db.users.find_one(
        {"_id": ObjectId(user_id)},
        {"password_hash": 0}
    )
    user_doc["id"] = str(user_doc.pop("_id"))
    
    # Convert datetime fields
    for field in ["created_at", "updated_at", "last_login_at", "account_locked_until"]:
        if user_doc.get(field):
            user_doc[field] = user_doc[field].isoformat()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user_doc,
        "is_new_user": not existing_user
    }


@router.post("/google/link")
async def link_google_account(
    token_request: GoogleTokenRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Link Google account to existing MediNova account.
    
    **Use Case:**
    - User already has MediNova account with email/password
    - User wants to also enable Google login
    """
    # Similar to callback but for existing logged-in users
    # Exchange code, verify email matches, update user record
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Account linking not yet implemented"
    )
