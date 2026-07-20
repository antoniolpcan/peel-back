from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    body: str
    color_id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    color_id: Optional[int] = None

class PostResponse(PostBase):
    id: int
    user_id: int
    likes: int = 0
    created_at: Optional[datetime]

    class Config:
        from_attributes = True