"""
Authentication Service
Business logic for user authentication and management
"""

from datetime import datetime
from typing import Optional, Dict
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.user import UserInDB, user_helper, UserRole
from app.schemas.auth import UserRegisterRequest, UserLoginRequest
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.config import settings


class AuthService:
    """Authentication service for user operations"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.users_collection = db.users
        self.patient_collection = db.patient_profiles
        self.doctor_collection = db.doctor_profiles

    # ── Registration ──────────────────────────────────────────────────────────

    async def register_user(self, user_data: UserRegisterRequest) -> Dict:
        """
        Register a new user.

        - Checks email uniqueness
        - Hashes the password with bcrypt
        - Inserts user document
        - Auto-creates blank patient or doctor profile
        - Generates email verification token and sends verification email
        - Returns JWT access + refresh tokens and user info
        """
        # Check if email already exists
        existing_user = await self.users_collection.find_one({"email": user_data.email.lower()})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
                headers={"error_code": "EMAIL_EXISTS"}
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Build user document
        user_dict = {
            "email": user_data.email.lower(),
            "password_hash": hashed_password,
            "role": user_data.role,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "phone": user_data.phone,
            "date_of_birth": user_data.date_of_birth,
            "gender": user_data.gender,
            "profile_picture_url": None,

            # Account status
            "is_active": True,
            "is_email_verified": False,
            "is_phone_verified": False,
            "email_verification_token": None,
            "email_verification_expires": None,

            # Security
            "password_reset_token": None,
            "password_reset_expires": None,
            "mfa_enabled": False,
            "mfa_secret": None,
            "failed_login_attempts": 0,
            "account_locked_until": None,

            # Timestamps
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login_at": None,
            "deleted_at": None,
        }

        # Insert user
        result = await self.users_collection.insert_one(user_dict)
        user_id = str(result.inserted_id)

        # Auto-create role-specific profile
        if user_data.role == UserRole.PATIENT:
            await self._create_patient_profile(user_id)
        elif user_data.role == UserRole.DOCTOR:
            await self._create_doctor_profile(user_id)

        # Generate and send email verification
        email_sent = False
        email_error_message = None
        try:
            token = await self.generate_verification_token(user_id)
            from app.services.email_service import email_service
            user_name = f"{user_data.first_name} {user_data.last_name}"
            await email_service.send_verification_email(user_data.email, token, user_name)
            email_sent = True
        except Exception as e:
            # Log error but don't fail registration
            import logging
            logging.getLogger(__name__).error(f"Failed to send verification email: {e}")
            email_error_message = "Email verification could not be sent. You can request a new verification email later."

        # Fetch created user
        created_user = await self.users_collection.find_one({"_id": result.inserted_id})

        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(created_user["_id"]), "role": created_user["role"]}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(created_user["_id"])}
        )

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user_helper(created_user),
            "email_verification_sent": email_sent
        }
        
        # Include warning message if email failed
        if email_error_message:
            response["warning"] = email_error_message
        
        return response

    async def _create_patient_profile(self, user_id: str) -> None:
        """Auto-create a blank patient profile on registration."""
        # Guard against duplicate profile (idempotent)
        existing = await self.patient_collection.find_one({"user_id": user_id})
        if existing:
            return

        default_profile = {
            "user_id": user_id,
            "blood_group": None,
            "height_cm": None,
            "weight_kg": None,
            "bmi": None,
            "allergies": [],
            "chronic_conditions": [],
            "past_surgeries": [],
            "family_history": [],
            "emergency_contact": None,
            "insurance": None,
            "preferences": {
                "preferred_hospital_id": None,
                "preferred_pharmacy": None,
                "language": "en",
                "communication_preference": "both",
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_health_check": None,
        }
        await self.patient_collection.insert_one(default_profile)

    async def _create_doctor_profile(self, user_id: str) -> None:
        """Auto-create a blank doctor profile on registration (pending verification)."""
        existing = await self.doctor_collection.find_one({"user_id": user_id})
        if existing:
            return

        # Generate unique pending license number using UUID
        import uuid
        pending_license = f"PENDING-{str(uuid.uuid4())[:8].upper()}"
        
        default_profile = {
            "user_id": user_id,
            "license_number": pending_license,  # Unique pending value - replaced after verification
            "license_state": "",
            "license_country": "",
            "license_expiry": None,
            "license_document_url": "",
            "specialization": "General Practitioner",
            "sub_specializations": [],
            "qualifications": [],
            "years_of_experience": 0,
            "consultation_fee": 0.0,
            "consultation_duration": 30,
            "accepts_insurance": True,
            "languages_spoken": ["English"],
            "bio": "",
            "primary_hospital_id": "",
            "affiliated_hospitals": [],
            "availability": [],
            "rating": 0.0,
            "review_count": 0,
            "total_consultations": 0,
            "is_verified": False,
            "is_accepting_patients": False,
            "awards": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        await self.doctor_collection.insert_one(default_profile)

    # ── Login ─────────────────────────────────────────────────────────────────

    async def login_user(self, login_data: UserLoginRequest) -> Dict:
        """
        Authenticate user and generate tokens.

        - Verifies credentials
        - Checks account status and lock state
        - Resets failed-attempt counter on success
        - Returns JWT access + refresh tokens and user info
        """
        # Find user by email
        user = await self.users_collection.find_one({"email": login_data.email.lower()})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"error_code": "INVALID_CREDENTIALS"},
            )

        # Check if account is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is suspended",
                headers={"error_code": "ACCOUNT_SUSPENDED"},
            )

        # Check if account is locked
        if user.get("account_locked_until"):
            if user["account_locked_until"] > datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is temporarily locked. Please try again later.",
                    headers={"error_code": "ACCOUNT_LOCKED"},
                )
            else:
                # Lock expired — reset it
                await self.users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"account_locked_until": None, "failed_login_attempts": 0}},
                )

        # Verify password
        if not verify_password(login_data.password, user["password_hash"]):
            failed_attempts = user.get("failed_login_attempts", 0) + 1
            update_data = {
                "failed_login_attempts": failed_attempts,
                "updated_at": datetime.utcnow(),
            }

            # Lock account after 5 consecutive failures (15-minute window)
            if failed_attempts >= 5:
                from datetime import timedelta
                update_data["account_locked_until"] = datetime.utcnow() + timedelta(minutes=15)

            await self.users_collection.update_one({"_id": user["_id"]}, {"$set": update_data})

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"error_code": "INVALID_CREDENTIALS"},
            )

        # Reset failed attempts and record last login
        await self.users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "failed_login_attempts": 0,
                    "last_login_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        # Re-fetch updated user
        user = await self.users_collection.find_one({"_id": user["_id"]})

        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(user["_id"]), "role": user["role"]}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user["_id"])}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user_helper(user),
        }

    # ── User Retrieval ────────────────────────────────────────────────────────

    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """
        Get user by MongoDB ObjectId string.

        Returns:
            Sanitized user dict (no password_hash) or None if not found.
        """
        try:
            user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return user_helper(user)
            return None
        except Exception:
            return None

    async def get_current_user(self, user_id: str) -> Dict:
        """
        Get currently authenticated user.

        Raises:
            HTTPException 404: if user does not exist.
        """
        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"error_code": "USER_NOT_FOUND"},
            )

        return user

    async def generate_verification_token(self, user_id: str) -> str:
        """
        Generate email verification token and update user record
        
        Returns the verification token (not saved in database for security)
        """
        import secrets
        from datetime import timedelta
        
        # Generate cryptographically secure random token
        token = secrets.token_urlsafe(32)
        
        # Hash the token before storing (don't store plaintext tokens)
        from app.utils.security import hash_password
        token_hash = hash_password(token)
        
        # Set expiration (24 hours)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Update user with token hash and expiration
        await self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "email_verification_token": token_hash,
                    "email_verification_expires": expires_at,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return token  # Return unhashed token for email
    
    async def verify_email(self, token: str) -> Dict:
        """
        Verify email with token
        
        Returns user data if successful
        Raises HTTPException if token is invalid/expired
        """
        from app.utils.security import verify_password
        
        # Find users with non-null verification tokens
        users_cursor = self.users_collection.find({
            "email_verification_token": {"$ne": None},
            "is_email_verified": False
        })
        
        users = await users_cursor.to_list(length=100)
        
        # Check token against each user (constant-time comparison via bcrypt)
        matching_user = None
        for user in users:
            if verify_password(token, user.get("email_verification_token", "")):
                matching_user = user
                break
        
        if not matching_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        # Check if token expired
        expires_at = matching_user.get("email_verification_expires")
        if not expires_at or expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token has expired"
            )
        
        # Mark email as verified and clear token (one-time use)
        await self.users_collection.update_one(
            {"_id": matching_user["_id"]},
            {
                "$set": {
                    "is_email_verified": True,
                    "email_verification_token": None,
                    "email_verification_expires": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Fetch updated user
        updated_user = await self.users_collection.find_one({"_id": matching_user["_id"]})
        
        return {
            "success": True,
            "message": "Email verified successfully",
            "user": user_helper(updated_user)
        }
    
    async def resend_verification_email(self, email: str) -> Dict:
        """
        Resend verification email
        
        Returns success message (does not reveal if email exists)
        """
        # Find user by email
        user = await self.users_collection.find_one({"email": email.lower()})
        
        # Always return success to prevent email enumeration
        response = {
            "success": True,
            "message": "If the email exists and is not verified, a verification email has been sent",
            "email_sent": False
        }
        
        if not user:
            return response  # Don't reveal email doesn't exist
        
        if user.get("is_email_verified"):
            return response  # Don't reveal email is already verified
        
        # Generate new verification token
        token = await self.generate_verification_token(str(user["_id"]))
        
        # Try to send verification email
        try:
            from app.services.email_service import email_service
            user_name = f"{user['first_name']} {user['last_name']}"
            await email_service.send_verification_email(email, token, user_name)
            response["email_sent"] = True
        except Exception as e:
            # Log the error but maintain generic response for security
            import logging
            logging.getLogger(__name__).error(f"Failed to send verification email to {email}: {e}")
            response["warning"] = "Email service is currently unavailable. Please try again later."
        
        return response

    async def request_password_reset(self, email: str) -> Dict:
        """
        Request password reset - generates token and sends email
        
        Returns generic success message (no email enumeration)
        """
        # Find user by email
        user = await self.users_collection.find_one({"email": email.lower()})
        
        # Always return success to prevent email enumeration
        response = {
            "success": True,
            "message": "If the email exists, a password reset link has been sent",
            "email_sent": False
        }
        
        if not user:
            return response  # Don't reveal email doesn't exist
        
        # Generate password reset token
        import secrets
        from datetime import timedelta
        
        token = secrets.token_urlsafe(32)
        
        # Hash the token before storing
        from app.utils.security import hash_password
        token_hash = hash_password(token)
        
        # Set expiration (1 hour)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        # Update user with reset token
        await self.users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "password_reset_token": token_hash,
                    "password_reset_expires": expires_at,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Try to send password reset email
        try:
            from app.services.email_service import email_service
            user_name = f"{user['first_name']} {user['last_name']}"
            await email_service.send_password_reset_email(email, token, user_name)
            response["email_sent"] = True
        except Exception as e:
            # Log the error but maintain generic response for security
            import logging
            logging.getLogger(__name__).error(f"Failed to send password reset email to {email}: {e}")
            response["warning"] = "Email service is currently unavailable. Please try again later."
        
        return response
    
    async def reset_password(self, token: str, new_password: str) -> Dict:
        """
        Reset password with token
        
        Returns success if token is valid
        Raises HTTPException if token is invalid/expired
        """
        from app.utils.security import verify_password
        
        # Find users with non-null reset tokens
        users_cursor = self.users_collection.find({
            "password_reset_token": {"$ne": None}
        })
        
        users = await users_cursor.to_list(length=100)
        
        # Check token against each user (constant-time comparison)
        matching_user = None
        for user in users:
            if verify_password(token, user.get("password_reset_token", "")):
                matching_user = user
                break
        
        if not matching_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Check if token expired
        expires_at = matching_user.get("password_reset_expires")
        if not expires_at or expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )
        
        # Hash new password
        new_password_hash = hash_password(new_password)
        
        # Update password and clear reset token (one-time use)
        await self.users_collection.update_one(
            {"_id": matching_user["_id"]},
            {
                "$set": {
                    "password_hash": new_password_hash,
                    "password_reset_token": None,
                    "password_reset_expires": None,
                    "updated_at": datetime.utcnow(),
                    "failed_login_attempts": 0,
                    "account_locked_until": None
                }
            }
        )
        
        return {
            "success": True,
            "message": "Password reset successfully"
        }
