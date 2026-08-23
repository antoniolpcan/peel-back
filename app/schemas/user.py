import re
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field
from typing import Optional
from datetime import datetime
from app.schemas.media_files import MediaFileBase

class BasicUserResponse(BaseModel):
    id: str
    name: str
    username: str
    bio: Optional[str] = None
    avatar: Optional[MediaFileBase] = None
    created_at: Optional[datetime]

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., description="Senha forte para adequação à LGPD")
    verification_token: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('A senha deve conter no mínimo 8 caracteres.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('A senha deve conter no mínimo uma letra maiúscula.')
        if not re.search(r'[a-z]', v):
            raise ValueError('A senha deve conter no mínimo uma letra minúscula.')
        if not re.search(r'\d', v):
            raise ValueError('A senha deve conter no mínimo um número.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('A senha deve conter no mínimo um caractere especial.')
        return v

class UserResponse(UserBase):
    id: str
    avatar: Optional[MediaFileBase] = None
    created_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_id: Optional[str] = None