"""
FastAPI Dependencies
Reusable dependency functions for authentication and authorization
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.utils.security import verify_token
from app.services.auth_service import AuthService
from app.models.user import UserRole

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get current authenticated user from JWT token
    
    Usage in routes:
        @router.get("/protected")
        async def protected_route(current_user = Depends(get_current_user)):
            return {"user": current_user}
    
    Args:
        credentials: HTTP Bearer token from request header
        db: Database connection
        
    Returns:
        Current user document
        
    Raises:
        HTTPException 401: If token is invalid or expired
        HTTPException 404: If user not found
    """
    token = credentials.credentials
    
    # Verify token and extract user ID
    user_id = verify_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer", "error_code": "INVALID_TOKEN"}
        )
    
    # Get user from database
    auth_service = AuthService(db)
    user = await auth_service.get_current_user(user_id)
    
    return user


def require_role(allowed_roles: List[str]):
    """
    Role-based authorization dependency factory
    
    Usage in routes:
        @router.get("/admin-only", dependencies=[Depends(require_role(["admin"]))])
        async def admin_route():
            return {"message": "Admin access granted"}
        
        @router.get("/patient-or-doctor", dependencies=[Depends(require_role(["patient", "doctor"]))])
        async def mixed_route():
            return {"message": "Patient or Doctor access granted"}
    
    Args:
        allowed_roles: List of roles that can access the endpoint
        
    Returns:
        Dependency function that checks user role
        
    Raises:
        HTTPException 403: If user role is not in allowed_roles
    """
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}",
                headers={"error_code": "INSUFFICIENT_PERMISSIONS"}
            )
        
        return current_user
    
    return role_checker


# Pre-defined role dependencies for convenience
async def require_admin(current_user: dict = Depends(get_current_user)):
    """
    Require admin role
    
    Usage:
        @router.get("/admin")
        async def admin_route(user = Depends(require_admin)):
            return {"message": "Admin access"}
    """
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
            headers={"error_code": "ADMIN_REQUIRED"}
        )
    return current_user


async def require_doctor(current_user: dict = Depends(get_current_user)):
    """
    Require doctor role
    
    Usage:
        @router.get("/doctor")
        async def doctor_route(user = Depends(require_doctor)):
            return {"message": "Doctor access"}
    """
    if current_user.get("role") != UserRole.DOCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor access required",
            headers={"error_code": "DOCTOR_REQUIRED"}
        )
    return current_user


async def require_patient(current_user: dict = Depends(get_current_user)):
    """
    Require patient role
    
    Usage:
        @router.get("/patient")
        async def patient_route(user = Depends(require_patient)):
            return {"message": "Patient access"}
    """
    if current_user.get("role") != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient access required",
            headers={"error_code": "PATIENT_REQUIRED"}
        )
    return current_user


async def require_patient_or_doctor(current_user: dict = Depends(get_current_user)):
    """
    Require patient or doctor role
    
    Usage:
        @router.get("/healthcare")
        async def healthcare_route(user = Depends(require_patient_or_doctor)):
            return {"message": "Patient or Doctor access"}
    """
    if current_user.get("role") not in [UserRole.PATIENT, UserRole.DOCTOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient or Doctor access required",
            headers={"error_code": "HEALTHCARE_USER_REQUIRED"}
        )
    return current_user
