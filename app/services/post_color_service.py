from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.color_repository import ColorRepository
from app.schemas.post_color import PostColorCreate
from app.models.post_color import PostColor

class ColorService:
    def __init__(self, db: AsyncSession):
        self.color_repo = ColorRepository(db)

    async def create_color(self, color_in: PostColorCreate) -> PostColor:
        color = await self.color_repo.get_by_name(color_in.color_name)
        if color:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cor já registrada."
            )
        return await self.color_repo.create(color_in)

    async def get_color(self, color_id: int) -> PostColor | None:
        return await self.color_repo.get_by_id(color_id)
    
    async def list_colors(self) -> list[PostColor]:
        return await self.color_repo.get_all()