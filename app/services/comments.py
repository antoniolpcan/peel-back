from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.schemas.comments import CommentCreate
from app.models.comments import Comment
from app.services.notifications import NotificationService
from app.schemas.notifications import NotificationCreate
from app.models.notifications import NotificationType

class CommentService:

    def __init__(self, db: AsyncSession):
        self.post_repo = PostRepository(db)
        self.comment_repo = CommentRepository(db)
        self.notification_service = NotificationService(db)

    async def create_comment(self, comment_in: CommentCreate, user_id: str) -> Comment:
        post = await self.post_repo.get_by_id(post_id=comment_in.post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="O post que você está tentando comentar não existe."
            )
        comment = await self.comment_repo.create(comment_in=comment_in, user_id=user_id)
        if user_id != post.user_id:
            notif_data = NotificationCreate(
                user_id=post.user_id,
                type=NotificationType.COMMENT,
                entity_id=post.id
            )
            await self.notification_service.create_notification(notif_data, actor_id=user_id)
        return comment

    async def get_comments_for_post(self, post_id: str) -> list[Comment]:
        post_exists = await self.post_repo.get_by_id(post_id=post_id)
        if not post_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Post não encontrado."
            )
        return await self.comment_repo.get_by_post(post_id=post_id)