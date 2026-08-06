from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.follows import FollowRepository
from app.schemas.follows import FollowCreate
from app.models.follows import Follow
from app.services.notifications import NotificationService
from app.schemas.notifications import NotificationCreate
from app.models.notifications import NotificationType

class FollowService:

    def __init__(self, db: AsyncSession):
        self.follower_repo = FollowRepository(db)
        self.notification_service = NotificationService(db)

    async def follow_user(self, follower_id: int, follow_data: FollowCreate) -> Follow:
        if follower_id == follow_data.following_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode seguir a si mesmo."
            )

        existing_follow = await self.follower_repo.get_follow(follower_id, follow_data.following_id)
        if existing_follow:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Você já segue este usuário."
            )

        new_follow = await self.follower_repo.create(follower_id, follow_data.following_id)
        await self.follower_repo.db.commit()
        await self.follower_repo.db.refresh(new_follow)
        notif_data = NotificationCreate(
            user_id=follow_data.following_id,
            type=NotificationType.FOLLOW,
            entity_id=follower_id
        )
        await self.notification_service.create_notification(notif_data, actor_id=follower_id)
        return new_follow

    async def unfollow_user(self, follower_id: int, following_id: int) -> None:
        follow = await self.follower_repo.get_follow(follower_id, following_id)
        if not follow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Relação de busca não encontrada."
            )

        await self.follower_repo.delete(follow)
        await self.follower_repo.db.commit()

    async def get_followers(self, user_id: int) -> list[Follow]:
        return await self.follower_repo.get_followers(user_id)

    async def get_following(self, user_id: int) -> list[Follow]:
        return await self.follower_repo.get_following(user_id)

    async def get_follow_stats(self, user_id: int) -> list[Follow]:
        return await self.follower_repo.get_follow_stats(user_id)