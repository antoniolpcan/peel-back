from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BasicUserResponse(BaseModel):
    name: str
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar_id: Optional[int] = None
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
    avatar_id: Optional[int] = None
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_id: Optional[int] = None