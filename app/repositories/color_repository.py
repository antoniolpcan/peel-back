from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post_color import PostColor
from app.schemas.post_color import PostColorCreate

class ColorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> PostColor | None:
        return await self.db.scalar(select(PostColor).where(PostColor.id == post_id))
    
    async def get_by_name(self, color_name: str) -> PostColor | None:
        return await self.db.scalar(select(PostColor).where(PostColor.color_name == color_name))
    
    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[PostColor]:
        result = await self.db.scalars(select(PostColor).offset(skip).limit(limit))
        return list(result.all())

    async def get_all(self) -> list[PostColor]:
        result = await self.db.scalars(select(PostColor))
        return list(result.all())

    async def create(self, obj_in: PostColorCreate) -> PostColor:
        db_obj = PostColor(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: PostColor) -> None:
        await self.db.delete(db_obj)
        await self.db.commit()

    async def save(self) -> None:
        await self.db.commit()