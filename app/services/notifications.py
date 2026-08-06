from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status
from app.models.notifications import Notification
from app.schemas.notifications import NotificationCreate
from app.repositories.notifications import NotificationRepository

class NotificationService:
    def __init__(self, session: AsyncSession):
        self.repository = NotificationRepository(session)

    async def create_notification(self, data: NotificationCreate, actor_id: int) -> Notification:
        return await self.repository.create(data, actor_id)

    async def get_user_notifications(self, user_id: int, skip: int, limit: int) -> Sequence[Notification]:
        return await self.repository.get_by_user_id(user_id, skip, limit)

    async def read_notification(self, notification_id: int, user_id: int) -> Notification:
        notification = await self.repository.mark_as_read(notification_id, user_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificação não encontrada ou você não tem permissão para acessá-la."
            )
        return notification