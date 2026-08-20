from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.notifications import NotificationType
from app.schemas.user import BasicUserResponse

class NotificationBase(BaseModel):
    type: NotificationType
    entity_id: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: str

class NotificationResponse(NotificationBase):
    id: str
    user_id: str
    actor_id: str
    is_read: bool
    created_at: datetime
    actor: BasicUserResponse 
    model_config = ConfigDict(from_attributes=True)