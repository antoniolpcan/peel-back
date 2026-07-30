from fastapi import APIRouter, Depends
from typing import List

from app.api.deps import get_color_service
from app.schemas.color import ColorResponse
from app.services.colors import ColorService

router = APIRouter()

@router.get("", response_model=List[ColorResponse])
async def read_colors(service: ColorService = Depends(get_color_service)):
    return await service.list_colors()

@router.get("/{color_id}", response_model=ColorResponse)
async def read_color(color_id: int, service: ColorService = Depends(get_color_service)):
    return await service.get_color(color_id)