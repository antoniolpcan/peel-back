from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import BasicUserResponse

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: str

class CommentResponse(CommentBase):
    id: str
    post_id: str
    user_id: str
    user: BasicUserResponse
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)