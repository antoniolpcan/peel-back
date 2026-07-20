from fastapi import APIRouter, Depends, status
from typing import List

from app.api.deps import get_color_service
from app.schemas.color import ColorCreate, ColorResponse
from app.services.colors import ColorService

router = APIRouter()

@router.post("", response_model=ColorResponse, status_code=status.HTTP_201_CREATED)
async def create_color(color_in: ColorCreate, service: ColorService = Depends(get_color_service)):
    return await service.create_color(color_in)

@router.post("/by-list", response_model=List[ColorResponse], status_code=status.HTTP_201_CREATED)
async def create_color_by_list(color_in: List[ColorCreate], service: ColorService = Depends(get_color_service)):
    return await service.create_color(color_in)

@router.get("", response_model=List[ColorResponse])
async def read_colors(service: ColorService = Depends(get_color_service)):
    return await service.list_colors()

@router.get("/{color_id}", response_model=ColorResponse)
async def read_color(color_id: int, service: ColorService = Depends(get_color_service)):
    return await service.get_color(color_id)