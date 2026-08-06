from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_settings import UserSetting
from app.schemas.user_settings import UserSettingUpdate

class UserSettingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> UserSetting | None:
        stmt = select(UserSetting).where(UserSetting.user_id == user_id)
        return await self.db.scalar(stmt)

    async def create_default(self, user_id: int) -> UserSetting:
        db_setting = UserSetting(user_id=user_id)
        self.db.add(db_setting)
        await self.db.commit()
        await self.db.refresh(db_setting)
        return db_setting

    async def update(self, db_setting: UserSetting, setting_in: UserSettingUpdate) -> UserSetting:
        update_data = setting_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_setting, field, value)
        
        self.db.add(db_setting)
        await self.db.commit()
        await self.db.refresh(db_setting)
        return db_setting