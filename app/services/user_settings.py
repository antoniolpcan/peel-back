from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_settings import UserSettingRepository
from app.schemas.user_settings import UserSettingUpdate
from app.models.user_settings import UserSetting

class UserSettingService:
    def __init__(self, db: AsyncSession):
        self.setting_repo = UserSettingRepository(db)

    async def get_user_settings(self, user_id: str) -> UserSetting:
        setting = await self.setting_repo.get_by_user_id(user_id)
        if not setting:
            setting = await self.setting_repo.create_default(user_id)
        return setting

    async def update_user_settings(self, user_id: str, setting_in: UserSettingUpdate) -> UserSetting:
        setting = await self.get_user_settings(user_id)
        return await self.setting_repo.update(db_setting=setting, setting_in=setting_in)