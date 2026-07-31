from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)