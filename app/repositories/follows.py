from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.follows import Follow

class FollowRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_follow(self, follower_id: int, following_id: int) -> Follow | None:
        query = select(Follow).where(
            Follow.follower_id == follower_id, 
            Follow.following_id == following_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_followers(self, user_id: int) -> list[Follow]:
        query = (
            select(Follow)
            .options(
                selectinload(Follow.follower)
            )
            .where(Follow.following_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def get_following(self, user_id: int) -> list[Follow]:
        """Traz todas as pessoas que user_id segue, trazendo os dados de quem é seguido (following)"""
        query = (
            select(Follow)
            .options(
                selectinload(Follow.following)
            )
            .where(Follow.follower_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def create(self, follower_id: int, following_id: int) -> Follow:
        new_follow = Follow(follower_id=follower_id, following_id=following_id)
        self.db.add(new_follow)
        return new_follow

    async def delete(self, follow: Follow) -> None:
        await self.db.delete(follow)