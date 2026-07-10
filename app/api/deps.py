from app.core.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.storage_service import StorageService
from app.services.post_service import PostItService
from app.services.post_color_service import ColorService

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
        )
    user = UserRepository(db)
    autenticated_user = await user.get_by_id(user_id=int(user_id))
    if not autenticated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return autenticated_user

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

def get_storage_service(db: AsyncSession = Depends(get_db)) -> StorageService:
    return StorageService(db)

def get_post_service(db: AsyncSession = Depends(get_db)) -> PostItService:
    return PostItService(db)

def get_color_service(db: AsyncSession = Depends(get_db)) -> ColorService:
    return ColorService(db)