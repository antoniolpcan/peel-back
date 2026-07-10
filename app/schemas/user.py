from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: Optional[str] = None
    avatar_id: Optional[int] = None
    bio: Optional[str] = ""

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_id: Optional[int] = None
    bio: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True