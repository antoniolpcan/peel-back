from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.media_files import MediaFile

class MediaRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def save(self, filename: str, user_id: int, url: str) -> MediaFile:
        new_file = MediaFile(filename=filename, user_id=user_id,url=url)
        self.db.add(new_file)
        await self.db.commit()
        await self.db.refresh(new_file)
        return new_file

    async def find_all(self):
        result = await self.db.execute(select(MediaFile))
        return result.scalars().all()