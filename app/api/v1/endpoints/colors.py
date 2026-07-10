from fastapi import APIRouter, Depends, status
from typing import List

from app.api.deps import get_color_service
from app.schemas.post_color import PostColorCreate, PostColorResponse
from app.services.post_color_service import ColorService

router = APIRouter()

@router.post("", response_model=PostColorResponse, status_code=status.HTTP_201_CREATED)
async def create_color(color_in: PostColorCreate, service: ColorService = Depends(get_color_service)):
    return await service.create_color(color_in)

@router.post("/by-list", response_model=List[PostColorResponse], status_code=status.HTTP_201_CREATED)
async def create_color_by_list(color_in: List[PostColorCreate], service: ColorService = Depends(get_color_service)):
    return await service.create_color(color_in)

@router.get("", response_model=List[PostColorResponse])
async def read_colors(service: ColorService = Depends(get_color_service)):
    return await service.list_colors()

@router.get("/{color_id}", response_model=PostColorResponse)
async def read_color(color_id: int, service: ColorService = Depends(get_color_service)):
    return await service.get_color(color_id)