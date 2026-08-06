from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserSettingBase(BaseModel):
    theme: str = "light"
    sound: bool = False
    is_private: bool = False
    email_notifications: bool = True
    push_notifications: bool = True

class UserSettingUpdate(BaseModel):
    theme: Optional[str] = None
    sound: Optional[bool] = None
    is_private: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None

class UserSettingResponse(UserSettingBase):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)