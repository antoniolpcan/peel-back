from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.users import UserRepository
from app.core.security import verify_password, create_access_token
import asyncio

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def acess_auth(self, form_data):
        user = await self.user_repo.get_by_email(email=form_data.username)
        if user:
            is_password_valid = await asyncio.to_thread(
                verify_password, form_data.password, user.hashed_password
            )
        else:
            is_password_valid = False
        if not user or not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "access_token": create_access_token(subject=user.id),
            "token_type": "bearer",
        }