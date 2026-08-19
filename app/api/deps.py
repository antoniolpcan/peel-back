from typing import AsyncGenerator
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import ALGORITHM, SECRET_KEY
from app.models.users import User
from app.repositories.users import UserRepository
from app.repositories.token_blocklist import TokenBlocklistRepository

from app.services.auth import AuthService
from app.services.chat import ChatService
from app.services.colors import ColorService
from app.services.comments import CommentService
from app.services.follows import FollowService
from app.services.notifications import NotificationService
from app.services.posts import PostService
from app.services.storage import StorageService
from app.services.users import UserService
from app.services.user_settings import UserSettingService

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

reusable_oauth2_optional = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth",
    auto_error=False,
)

async def get_token_hybrid(
    request: Request,
    header_token: str | None = Depends(reusable_oauth2_optional)
) -> str | None:
    if header_token:
        return header_token
    
    token_with_prefix = request.cookies.get("access_token")
    if token_with_prefix:
        if token_with_prefix.startswith("Bearer "):
            return token_with_prefix.split(" ")[1]
        return token_with_prefix
        
    return None

async def get_current_user_optional(
    db: AsyncSession = Depends(get_db),
    token: str | None = Depends(get_token_hybrid),
) -> User | None:
    
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        jti: str | None = payload.get("jti")

        if user_id is None or jti is None:
            return None

        blocklist_repo = TokenBlocklistRepository(db)
        if await blocklist_repo.is_blocked(jti):
            return None
            
    except (jwt.PyJWTError, ValidationError):
        return None

    user_repo = UserRepository(db)
    return await user_repo.get_by_id(user_id=int(user_id))


async def get_current_user(
    current_user: User | None = Depends(get_current_user_optional),
) -> User:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

def get_storage_service(db: AsyncSession = Depends(get_db)) -> StorageService:
    return StorageService(db)

def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(db)

def get_color_service(db: AsyncSession = Depends(get_db)) -> ColorService:
    return ColorService(db)

def get_comment_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    return CommentService(db)

def get_follow_service(db: AsyncSession = Depends(get_db)) -> FollowService:
    return FollowService(db)

def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(db)

def get_user_setting_service(db: AsyncSession = Depends(get_db)) -> UserSettingService:
    return UserSettingService(db)

def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(db)