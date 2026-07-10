from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import PostIt
from app.schemas.post import PostItCreate, PostItUpdate
from sqlalchemy import select

class PostItRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> PostIt | None:
        return await self.db.scalar(select(PostIt).where(PostIt.id == post_id))

    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[PostIt]:
        result = await self.db.scalars(select(PostIt).offset(skip).limit(limit))
        return list(result.all())

    async def create(self, obj_in: PostItCreate) -> PostIt:
        db_obj = PostIt(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: PostIt, obj_in: PostItUpdate) -> PostIt:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
        
    async def delete(self, db_obj: PostIt) -> bool:
        try:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False
        
    async def save(self) -> None:
        await self.db.commit()