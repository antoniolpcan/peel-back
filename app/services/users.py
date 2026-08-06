from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user_settings import UserSettingRepository
from app.repositories.users import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.users import User

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.setting_repo = UserSettingRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
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
                detail="Este nome de usuário (username) já está em uso."
            )
        new_user = await self.user_repo.create(user_in=user_in)
        await self.setting_repo.create_default(user_id=new_user.id)
        return new_user

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuário não encontrado."
            )
        return user

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User:
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

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.user_repo.delete(db_user=user)
    