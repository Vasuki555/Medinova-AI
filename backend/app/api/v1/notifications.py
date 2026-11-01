"""
Notifications Router
FastAPI endpoints for alerts, notifications inbox, and read counts
"""

from typing import List
from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.core.dependencies import get_current_user
from app.schemas.notification import NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationResponse])
async def get_my_notifications(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Retrieve full notification log for logged-in user"""
    service = NotificationService(db)
    notifications = await service.get_user_notifications(current_user["_id"])
    return notifications

@router.get("/unread-count")
async def get_unread_count(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get the total count of unread notifications in the inbox"""
    service = NotificationService(db)
    count = await service.get_unread_count(current_user["_id"])
    return {"unread_count": count}

@router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark a single notification alert as read"""
    service = NotificationService(db)
    success = await service.mark_as_read(current_user["_id"], notification_id)
    return {"success": success}

@router.patch("/read-all")
async def mark_all_as_read(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark all active notifications in the inbox as read"""
    service = NotificationService(db)
    success = await service.mark_all_as_read(current_user["_id"])
    return {"success": success}
