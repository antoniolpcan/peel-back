from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.comments import Comment
from app.schemas.comments import CommentCreate

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, comment_in: CommentCreate, user_id: int) -> Comment:
        db_comment = Comment(
            content=comment_in.content,
            post_id=comment_in.post_id,
            user_id=user_id
        )
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return db_comment

    async def get_by_post(self, post_id: int) -> list[Comment]:
        result = await self.db.execute(select(Comment).where(Comment.post_id == post_id))
        return list(result.scalars().all())