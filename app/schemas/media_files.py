from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MediaFileBase(BaseModel):
    url: str
    filename: str

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileResponse(MediaFileBase):
    id: str
    user_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)