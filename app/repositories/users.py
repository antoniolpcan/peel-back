from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.users import User
from app.schemas.user import UserCreate, UserBase
from app.core.security import get_password_hash
import asyncio

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).options(selectinload(User.avatar)).where(User.id == user_id)
        return await self.db.scalar(stmt)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).options(selectinload(User.avatar)).where(User.email == email)
        return await self.db.scalar(stmt)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).options(selectinload(User.avatar)).where(User.username == username)
        return await self.db.scalar(stmt)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).options(selectinload(User.avatar)).offset(skip).limit(limit)
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def create(self, user_in: UserCreate) -> User:
        user_data = user_in.model_dump()
        password = user_data.pop("password")
        user_data["hashed_password"] = await asyncio.to_thread(get_password_hash, password)
        
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return await self.get_by_id(db_user.id)

    async def update(self, db_user: User, user_in: UserBase) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return await self.get_by_id(db_user.id)

    async def delete(self, db_user: User) -> None:
        await self.db.delete(db_user)
        await self.db.commit()