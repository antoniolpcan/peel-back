from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.models.follows import Follow
from app.models.users import User

class FollowRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_follow(self, follower_id: str, following_id: str) -> Follow | None:
        query = select(Follow).where(
            Follow.follower_id == follower_id, 
            Follow.following_id == following_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_followers(self, user_id: str) -> list[Follow]:
        query = (
            select(Follow)
            .options(
                selectinload(Follow.follower).selectinload(User.avatar)
            )
            .where(Follow.following_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def get_following(self, user_id: str) -> list[Follow]:
        query = (
            select(Follow)
            .options(
                selectinload(Follow.following).selectinload(User.avatar)
            )
            .where(Follow.follower_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def create(self, follower_id: str, following_id: str) -> Follow:
        new_follow = Follow(follower_id=follower_id, following_id=following_id)
        self.db.add(new_follow)
        return new_follow

    async def delete(self, follow: Follow) -> None:
        await self.db.delete(follow)

    async def get_follow_stats(self, user_id: str) -> dict:
        followers_query = select(func.count()).select_from(Follow).where(Follow.following_id == user_id)
        following_query = select(func.count()).select_from(Follow).where(Follow.follower_id == user_id)
        followers_result = await self.db.execute(followers_query)
        following_result = await self.db.execute(following_query)
        
        return {
            "followers_count": followers_result.scalar() or 0,
            "following_count": following_result.scalar() or 0
        }