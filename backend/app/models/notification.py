"""
Notification Model
MongoDB document structure for user notifications and alerts
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class RelatedEntity(BaseModel):
    entity_type: str  # "appointment" | "medication" | "document"
    entity_id: str

class Notification(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str  # Reference to User ID
    
    type: str  # "appointment" | "medication" | "lab_result" | "message" | "alert" | "reminder"
    category: str = "info"  # "info" | "warning" | "success" | "error"
    
    title: str
    message: str
    priority: str = "medium"  # "low" | "medium" | "high" | "urgent"
    
    is_read: bool = False
    read_at: Optional[datetime] = None
    
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    
    related_entity: Optional[RelatedEntity] = None
    
    channels: List[str] = ["push"]  # ["push", "email", "sms"]
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "type": "medication",
                "category": "warning",
                "title": "Medication Reminder",
                "message": "It is time to take Paracetamol (500mg)",
                "is_read": False
            }
        }
