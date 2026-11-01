"""
Notification Service
Business logic for system notifications and user inbox feeds
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class NotificationService:
    """Service for managing user notifications"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.notifications_collection = db.notifications

    async def get_user_notifications(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch list of notifications for a user"""
        notifications = await self.notifications_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).to_list(limit)
        
        for n in notifications:
            n["id"] = str(n["_id"])
        return notifications

    async def get_unread_count(self, user_id: str) -> int:
        """Count unread messages"""
        return await self.notifications_collection.count_documents(
            {"user_id": user_id, "is_read": False}
        )

    async def create_notification(
        self,
        user_id: str,
        type: str,
        category: str = "info",
        title: str = "",
        message: str = "",
        action_url: Optional[str] = None,
        action_text: Optional[str] = None,
        related_entity: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Save a new notification to the database"""
        notification_dict = {
            "user_id": user_id,
            "type": type,
            "category": category,
            "title": title,
            "message": message,
            "priority": "high" if category in ["error", "warning"] else "medium",
            "is_read": False,
            "read_at": None,
            "action_url": action_url,
            "action_text": action_text,
            "related_entity": related_entity,
            "channels": ["push"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await self.notifications_collection.insert_one(notification_dict)
        created = await self.notifications_collection.find_one({"_id": result.inserted_id})
        created["id"] = str(created["_id"])
        return created

    async def mark_as_read(self, user_id: str, notification_id: str) -> bool:
        """Mark single item as read"""
        result = await self.notifications_collection.update_one(
            {"_id": ObjectId(notification_id), "user_id": user_id},
            {"$set": {"is_read": True, "read_at": datetime.utcnow(), "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def mark_all_as_read(self, user_id: str) -> bool:
        """Mark all notifications as read for a user"""
        result = await self.notifications_collection.update_many(
            {"user_id": user_id, "is_read": False},
            {"$set": {"is_read": True, "read_at": datetime.utcnow(), "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
