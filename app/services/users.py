from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user_settings import UserSettingRepository
from app.repositories.users import UserRepository
from app.repositories.token import TokenRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.users import User

from datetime import datetime, timezone

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.setting_repo = UserSettingRepository(db)
        self.token_repo = TokenRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
        db_code = await self.token_repo.get_by_email_and_token(
            email=user_in.email, 
            token_str=user_in.verification_token
        )
        if not db_code or db_code.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de verificação inválido ou já utilizado."
            )
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if db_code.expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O código de verificação expirou. Solicite um novo."
            )
        existing_user = await self.user_repo.get_by_email(email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O email já está cadastrado no sistema."
            )
        existing_username = await self.user_repo.get_by_username(username=user_in.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este nome de usuário já está em uso."
            )
        await self.token_repo.mark_as_used(db_code)
        new_user = await self.user_repo.create(user_in=user_in)
        await self.setting_repo.create_default(user_id=new_user.id)
        return new_user

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def get_user(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuário não encontrado."
            )
        return user

    async def update_user(self, user_id: str, user_in: UserUpdate) -> User:
        user = await self.get_user(user_id)
        if user_in.email and user_in.email != user.email:
            email_exists = await self.user_repo.get_by_email(email=user_in.email) 
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este e-mail já está sendo usado por outra conta."
                )
        if user_in.username and user_in.username != user.username:
            username_exists = await self.user_repo.get_by_username(username=user_in.username)
            if username_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este nome de usuário já está em uso."
                )
        return await self.user_repo.update(db_user=user, user_in=user_in)

    async def delete_user(self, user_id: str) -> None:
        user = await self.get_user(user_id)
        await self.user_repo.delete(db_user=user)
    