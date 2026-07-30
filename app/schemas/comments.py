from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import BasicUserResponse

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    user: BasicUserResponse
    created_at: datetime

    class Config:
        from_attributes = True