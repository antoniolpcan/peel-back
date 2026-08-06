from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.notifications import NotificationType
from app.schemas.user import BasicUserResponse

class NotificationBase(BaseModel):
    type: NotificationType
    entity_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    actor_id: int
    is_read: bool
    created_at: datetime
    actor: BasicUserResponse 
    model_config = ConfigDict(from_attributes=True)