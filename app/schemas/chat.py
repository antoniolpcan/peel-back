from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.schemas.user import BasicUserResponse

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatMemberResponse(BaseModel):
    user_id: int
    joined_at: datetime
    user: Optional[BasicUserResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ChatResponse(BaseModel):
    id: int
    created_at: datetime
    members: List[ChatMemberResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class UnreadSenderResponse(BaseModel):
    user: BasicUserResponse
    unread_count: int

    model_config = ConfigDict(from_attributes=True)

class UnreadSummaryResponse(BaseModel):
    total_unread: int
    senders: List[UnreadSenderResponse]