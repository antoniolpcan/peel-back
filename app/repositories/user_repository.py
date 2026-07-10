from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
import asyncio

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.scalar(select(User).where(User.id == user_id))

    async def get_by_email(self, email: str) -> User | None:
        return await self.db.scalar(select(User).where(User.email == email))

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.scalars(select(User).offset(skip).limit(limit))
        return list(result.all())

    async def create(self, user_in: UserCreate) -> User:
        user_data = user_in.model_dump()
        password = user_data.pop("password")
        user_data["hashed_password"] = await asyncio.to_thread(get_password_hash, password)
        
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update(self, db_user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete(self, db_user: User) -> None:
        await self.db.delete(db_user)
        await self.db.commit()