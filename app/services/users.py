from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.follows import FollowRepository
from app.repositories.users import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.users import User

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.follow_repo = FollowRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
        existing_user = await self.user_repo.get_by_email(email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O email já está cadastrado no sistema."
            )
        return await self.user_repo.create(user_in=user_in)

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
        return await self.user_repo.update(db_user=user, user_in=user_in)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.user_repo.delete(db_user=user)
    
    async def toggle_user_follow(self, follower_id: int, following_id: int) -> bool:
        if follower_id == following_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode seguir a si mesmo."
            )
        target_user = await self.user_repo.get_by_id(user_id=following_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O usuário que você está tentando seguir não existe."
            )
        existing_follow = await self.follow_repo.get_follow(follower_id=follower_id, following_id=following_id)
        if existing_follow:
            await self.follow_repo.delete(existing_follow)
            return False
        else:
            await self.follow_repo.create(follower_id=follower_id, following_id=following_id)
            return True