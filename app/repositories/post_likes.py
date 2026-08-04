from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post_likes import PostLike

class PostLikeRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_like(self, user_id: int, post_id: int) -> PostLike | None:
        query = select(PostLike).where(PostLike.user_id == user_id, PostLike.post_id == post_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, user_id: int, post_id: int) -> PostLike:
        new_like = PostLike(user_id=user_id, post_id=post_id)
        self.db.add(new_like)
        return new_like

    async def delete(self, like: PostLike) -> None:
        await self.db.delete(like)

    async def is_liked_by_user(self, post_id: int, user_id: int) -> bool:
        stmt = (
            select(PostLike.id)
            .where(
                PostLike.post_id == post_id,
                PostLike.user_id == user_id
            )
            .limit(1)
        )
        result = await self.db.scalar(stmt)
        return result is not None

    async def get_user_liked_post_ids(self, user_id: int, post_ids: list[int]) -> set[int]:
        stmt = select(PostLike.post_id).where(
            PostLike.user_id == user_id,
            PostLike.post_id.in_(post_ids)
        )
        result = await self.db.scalars(stmt)
        return set(result.all())