from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class Token(BaseModel):
    access_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., description="Nova senha forte para adequação à LGPD")

    @field_validator('new_password')
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