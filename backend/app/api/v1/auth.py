"""
Authentication Routes
API endpoints for user authentication
"""

from fastapi import APIRouter, Depends, status, HTTPException, Request, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field, validator
from bson import ObjectId
import re

from app.database import get_database
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, ErrorResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.core.rate_limit import limit_login, limit_register, limit_password, limit_email_verification, limit_password_reset
from app.models.user import user_helper
from app.config import settings

router = APIRouter()


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
    
    @validator("new_password")
    def validate_new_password(cls, v):
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


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="""
    Register a new user account.
    
    **Rate Limit:** 5 registrations per hour per IP
    
    **Roles:**
    - `patient` - Patient user
    - `doctor` - Doctor user  
    - `admin` - Administrator user
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character (!@#$%^&*(),.?":{}|<>)
    
    **Phone Format:**
    - E.164 format (e.g., +14155552671)
    
    **Returns:**
    - JWT access token (expires in 30 minutes)
    - JWT refresh token (expires in 7 days)
    - User information (excluding sensitive data)
    """,
    responses={
        201: {
            "description": "User successfully registered",
            "model": TokenResponse
        },
        400: {
            "description": "Email already exists or validation error",
            "model": ErrorResponse
        },
        422: {
            "description": "Validation error (invalid email, weak password, etc.)",
            "model": ErrorResponse
        },
        429: {
            "description": "Too many registration attempts. Rate limit exceeded."
        }
    }
)
@limit_register()
async def register(
    request: Request,
    response: Response,
    user_data: UserRegisterRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Register a new user
    
    - Creates new user account with hashed password
    - Generates JWT access and refresh tokens
    - Returns user info and tokens
    - Rate limited to 5 registrations per hour per IP
    """
    auth_service = AuthService(db)
    result = await auth_service.register_user(user_data)
    return result


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="""
    Authenticate user and generate tokens.
    
    **Rate Limit:** 5 login attempts per 15 minutes per IP
    
    **Security Features:**
    - Password verification using bcrypt
    - Failed login attempt tracking
    - Account locking after 5 failed attempts (15 minutes)
    - Updates last login timestamp
    
    **Returns:**
    - JWT access token (expires in 30 minutes)
    - JWT refresh token (expires in 7 days)
    - User information (excluding sensitive data)
    """,
    responses={
        200: {
            "description": "Login successful",
            "model": TokenResponse
        },
        401: {
            "description": "Invalid credentials",
            "model": ErrorResponse
        },
        403: {
            "description": "Account suspended or locked",
            "model": ErrorResponse
        },
        429: {
            "description": "Too many login attempts. Rate limit exceeded."
        }
    }
)
@limit_login()
async def login(
    request: Request,
    response: Response,
    login_data: UserLoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Login user
    
    - Validates credentials
    - Checks account status
    - Generates JWT tokens
    - Updates last login timestamp
    """
    auth_service = AuthService(db)
    result = await auth_service.login_user(login_data)
    return result


@router.get(
    "/me",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get Current User",
    description="""
    Get currently authenticated user information.
    
    **Authentication Required:**
    - Must provide valid JWT token in Authorization header
    - Format: `Authorization: Bearer <token>`
    
    **Returns:**
    - User information (excluding sensitive data like password)
    - User ID, email, role, name, etc.
    """,
    responses={
        200: {
            "description": "Current user information",
            "content": {
                "application/json": {
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
            }
        },
        401: {
            "description": "Invalid or expired token",
            "model": ErrorResponse
        },
        404: {
            "description": "User not found",
            "model": ErrorResponse
        }
    }
)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user
    
    - Requires valid JWT token
    - Returns user profile information
    - Excludes sensitive data (password, tokens, etc.)
    """
    return current_user


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change Password",
    description="""
    Change the authenticated user's password.
    
    **Rate Limit:** 5 password changes per 15 minutes per IP
    
    **Security Features:**
    - Verifies current password before changing
    - New password must be at least 8 characters
    - Hashes new password with bcrypt before storing
    
    **Requires:** Valid JWT authentication token
    """,
    responses={
        200: {
            "description": "Password changed successfully"
        },
        401: {
            "description": "Current password is incorrect or unauthorized"
        },
        404: {
            "description": "User not found"
        },
        429: {
            "description": "Too many password change attempts. Rate limit exceeded."
        }
    }
)
@limit_password()
async def change_password(
    request: Request,
    response: Response,
    data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Change the authenticated user's password.
    
    - Verifies current password before changing
    - New password must be at least 8 characters
    - Hashes new password with bcrypt before storing
    - Rate limited to 5 attempts per 15 minutes per IP
    """
    import bcrypt

    # Fetch user with password hash
    user_doc = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify current password
    stored_hash = user_doc.get("password_hash", "")
    if not stored_hash or not bcrypt.checkpw(
        data.current_password.encode("utf-8"),
        stored_hash.encode("utf-8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )

    # Hash new password
    new_hash = bcrypt.hashpw(data.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Update in DB
    await db.users.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": {"password_hash": new_hash}}
    )

    return {"success": True, "message": "Password changed successfully"}



@router.post(
    "/verify-email",
    status_code=status.HTTP_200_OK,
    summary="Verify Email Address",
    description="""
    Verify user email address with token sent via email.
    
    **Security Features:**
    - Token is hashed in database (not stored in plaintext)
    - Token expires after 24 hours
    - One-time use only (token deleted after verification)
    - Constant-time comparison to prevent timing attacks
    
    **Returns:**
    - Success message
    - Updated user information
    """,
    responses={
        200: {
            "description": "Email verified successfully"
        },
        400: {
            "description": "Invalid or expired token",
            "model": ErrorResponse
        }
    }
)
async def verify_email(
    token: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Verify email with token
    
    - Validates verification token
    - Marks email as verified
    - Invalidates token (one-time use)
    """
    auth_service = AuthService(db)
    result = await auth_service.verify_email(token)
    return result


class ResendVerificationRequest(BaseModel):
    email: str = Field(..., description="Email address to resend verification")


@router.post(
    "/resend-verification",
    status_code=status.HTTP_200_OK,
    summary="Resend Verification Email",
    description="""
    Resend email verification link.
    
    **Rate Limit:** 3 requests per hour per IP
    
    **Security Features:**
    - Does not reveal if email exists (prevents enumeration)
    - Does not reveal if email is already verified
    - Rate limited to prevent abuse
    - Generates new token each time
    
    **Returns:**
    - Generic success message (always, regardless of email existence)
    """,
    responses={
        200: {
            "description": "Success message (does not reveal email status)"
        },
        429: {
            "description": "Too many resend requests. Rate limit exceeded."
        }
    }
)
@limit_email_verification()
async def resend_verification(
    request: Request,
    response: Response,
    data: ResendVerificationRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Resend verification email
    
    - Generates new verification token
    - Sends verification email
    - Returns generic success message (no email enumeration)
    - Rate limited to 3 per hour per IP
    """
    auth_service = AuthService(db)
    result = await auth_service.resend_verification_email(data.email)
    return result



class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., description="Email address for password reset")


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Request Password Reset",
    description="""
    Request password reset link via email.
    
    **Rate Limit:** 3 requests per hour per IP
    
    **Security Features:**
    - Does not reveal if email exists (prevents enumeration)
    - Token is hashed in database
    - Token expires in 1 hour
    - One-time use only
    - Rate limited to prevent abuse
    
    **Returns:**
    - Generic success message (always, regardless of email existence)
    """,
    responses={
        200: {
            "description": "Success message (does not reveal email status)"
        },
        429: {
            "description": "Too many password reset requests. Rate limit exceeded."
        }
    }
)
@limit_password_reset()
async def forgot_password(
    request: Request,
    response: Response,
    data: ForgotPasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Request password reset
    
    - Generates secure reset token
    - Sends reset link via email
    - Returns generic success message (no email enumeration)
    - Rate limited to 3 per hour per IP
    """
    auth_service = AuthService(db)
    result = await auth_service.request_password_reset(data.email)
    return result


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password reset token from email")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
    
    @validator("new_password")
    def validate_new_password(cls, v):
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


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Reset Password",
    description="""
    Reset password with token received via email.
    
    **Security Features:**
    - Validates reset token
    - Token must not be expired (1 hour expiration)
    - One-time use (token invalidated after use)
    - New password is hashed with bcrypt
    - Clears failed login attempts
    - Unlocks account if locked
    
    **Returns:**
    - Success message
    """,
    responses={
        200: {
            "description": "Password reset successfully"
        },
        400: {
            "description": "Invalid or expired token",
            "model": ErrorResponse
        }
    }
)
async def reset_password(
    data: ResetPasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Reset password with token
    
    - Validates reset token
    - Updates password
    - Invalidates token (one-time use)
    - Clears failed login attempts
    """
    auth_service = AuthService(db)
    result = await auth_service.reset_password(data.token, data.new_password)
    return result



@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout User",
    description="""
    Logout user by revoking their refresh token.
    
    **Security Features:**
    - Revokes refresh token (prevents reuse)
    - Marks session as inactive
    - Access token remains valid until expiration (stateless JWT)
    
    **Note:** Access tokens are stateless and will remain valid until they expire.
    For critical operations, always check if the user's session is still active.
    
    **Requires:** Valid JWT authentication token
    """,
    responses={
        200: {
            "description": "Logout successful"
        },
        401: {
            "description": "Unauthorized - invalid or missing token",
            "model": ErrorResponse
        }
    }
)
async def logout(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Logout user
    
    - Revokes all active refresh tokens for the user
    - Marks all user sessions as inactive
    - Note: Access tokens remain valid until expiration
    """
    from app.services.session_service import SessionService
    
    session_service = SessionService(db)
    revoked_count = await session_service.revoke_all_user_sessions(current_user["_id"])
    
    return {
        "success": True,
        "message": "Logged out successfully",
        "sessions_revoked": revoked_count
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="""
    Get a new access token using a refresh token.
    
    **Security Features:**
    - Validates refresh token
    - Checks if token is revoked
    - Issues new access token
    - Updates session last_used timestamp
    
    **Returns:**
    - New access token
    - Same refresh token (or new one if rotation enabled)
    """,
    responses={
        200: {
            "description": "Token refreshed successfully",
            "model": TokenResponse
        },
        401: {
            "description": "Invalid or revoked refresh token",
            "model": ErrorResponse
        }
    }
)
async def refresh_token(
    refresh_token: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Refresh access token
    
    - Validates refresh token
    - Checks if token is revoked
    - Issues new access token
    """
    from jose import JWTError, jwt
    from app.services.session_service import SessionService
    
    try:
        # Decode refresh token
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY or settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        token_jti: str = payload.get("jti")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if token is revoked
        session_service = SessionService(db)
        if token_jti and await session_service.is_token_revoked(token_jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked"
            )
        
        # Get user from database
        auth_service = AuthService(db)
        user = await auth_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Generate new access token
        from app.utils.security import create_access_token
        access_token = create_access_token(
            data={"sub": user_id, "role": user["role"]}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,  # Return same refresh token
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user_helper(user)
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
