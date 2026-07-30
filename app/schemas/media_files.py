from pydantic import BaseModel
from datetime import datetime

class MediaFileBase(BaseModel):
    url: str
    filename: str

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileResponse(MediaFileBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True