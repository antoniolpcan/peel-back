from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PostItBase(BaseModel):
    title: str
    body: str
    color_id: Optional[int] = None

class PostItCreate(PostItBase):
    user_id: int

class PostItResponse(PostItBase):
    id: int
    user_id: int
    created_at: datetime
    likes: int
    has_liked: bool

    model_config = ConfigDict(from_attributes=True)