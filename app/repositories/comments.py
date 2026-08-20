from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.comments import Comment
from app.models.users import User
from app.schemas.comments import CommentCreate

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comment_id: str) -> Comment | None:
        stmt = (
            select(Comment)
            .options(selectinload(Comment.user).selectinload(User.avatar))
            .where(Comment.id == comment_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, comment_in: CommentCreate, user_id: str) -> Comment:
        db_comment = Comment(
            content=comment_in.content,
            post_id=comment_in.post_id,
            user_id=user_id
        )
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return await self.get_by_id(db_comment.id)

    async def get_by_post(self, post_id: str) -> list[Comment]:
        stmt = (
            select(Comment)
            .options(
                selectinload(Comment.user).selectinload(User.avatar)
            )
            .where(Comment.post_id == post_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())