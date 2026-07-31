from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)