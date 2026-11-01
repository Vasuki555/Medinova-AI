"""
Notification Schemas
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.notification import RelatedEntity

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: str
    category: str
    title: str
    message: str
    priority: str
    is_read: bool
    read_at: Optional[datetime] = None
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    related_entity: Optional[RelatedEntity] = None
    created_at: datetime

    class Config:
        populate_by_name = True
