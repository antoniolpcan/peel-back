from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notifications import Notification
from app.schemas.notifications import NotificationCreate

class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: NotificationCreate, actor_id: int) -> Notification:
        db_notification = Notification(**data.model_dump(), actor_id=actor_id)
        self.session.add(db_notification)
        await self.session.commit()
        await self.session.refresh(db_notification)
        return db_notification

    async def get_by_user_id(self, user_id: int, skip: int, limit: int) -> Sequence[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, notification_id: int, user_id: int) -> Notification | None:
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
            .values(is_read=True)
            .returning(Notification)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()