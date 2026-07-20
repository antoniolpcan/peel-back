from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.schemas.comments import CommentCreate
from app.models.comments import Comment

class CommentService:

    def __init__(self, db: AsyncSession):
        self.post_repo = PostRepository(db)
        self.comment_repo = CommentRepository(db)

    async def create_comment(self, comment_in: CommentCreate, user_id: int) -> Comment:
        post_exists = await self.post_repo.get_by_id(post_id=comment_in.post_id)
        if not post_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="O post que você está tentando comentar não existe."
            )
        return await self.comment_repo.create(comment_in=comment_in, user_id=user_id)

    async def get_comments_for_post(self, post_id: int) -> list[Comment]:
        post_exists = await self.post_repo.get_by_id(post_id=post_id)
        if not post_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Post não encontrado."
            )
        return await self.comment_repo.get_by_post(post_id=post_id)