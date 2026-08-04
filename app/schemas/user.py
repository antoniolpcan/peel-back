from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.media_files import MediaFileBase

class BasicUserResponse(BaseModel):
    id: int
    name: str
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[MediaFileBase] = None
    created_at: Optional[datetime]

class UserBase(BaseModel):
    name: str
    username: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    avatar: Optional[MediaFileBase] = None
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_id: Optional[int] = None