from pydantic import BaseModel, HttpUrl
from datetime import datetime

class MediaFileBase(BaseModel):
    filename: str
    url: str

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileResponse(MediaFileBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True