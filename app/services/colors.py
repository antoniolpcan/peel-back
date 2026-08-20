from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.colors import ColorRepository
from app.schemas.color import ColorCreate
from app.models.colors import Color

class ColorService:
    def __init__(self, db: AsyncSession):
        self.color_repo = ColorRepository(db)

    async def create_color(self, color_in: ColorCreate) -> Color:
        color = await self.color_repo.get_by_name(color_in.name)
        if color:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cor já registrada."
            )
        return await self.color_repo.create(color_in)

    async def get_color(self, color_id: str) -> Color | None:
        color = await self.color_repo.get_by_id(color_id)
        if not color:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cor não registrada."
            )
        return color
    
    async def list_colors(self) -> list[Color]:
        return await self.color_repo.get_all()