from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.colors import Color
from app.schemas.color import ColorCreate

class ColorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, color_id: str) -> Color | None:
        return await self.db.scalar(select(Color).where(Color.id == color_id))
    
    async def get_by_name(self, color_name: str) -> Color | None:
        return await self.db.scalar(select(Color).where(Color.name == color_name))
    
    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[Color]:
        result = await self.db.scalars(select(Color).offset(skip).limit(limit))
        return list(result.all())

    async def get_all(self) -> list[Color]:
        result = await self.db.scalars(select(Color))
        return list(result.all())

    async def create(self, obj_in: ColorCreate) -> Color:
        db_obj = Color(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: Color) -> None:
        await self.db.delete(db_obj)
        await self.db.commit()

    async def save(self) -> None:
        await self.db.commit()