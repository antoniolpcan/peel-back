from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.follows import Follow

class FollowRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_follow(self, follower_id: int, following_id: int) -> Follow | None:
        query = select(Follow).where(
            Follow.follower_id == follower_id, 
            Follow.following_id == following_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, follower_id: int, following_id: int) -> Follow:
        new_follow = Follow(follower_id=follower_id, following_id=following_id)
        self.db.add(new_follow)
        return new_follow

    async def delete(self, follow: Follow) -> None:
        await self.db.delete(follow)