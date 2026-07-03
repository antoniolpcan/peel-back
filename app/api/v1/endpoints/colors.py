from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.post_color import PostColorCreate, PostColorResponse
from app.services.post_color_service import ColorService

router = APIRouter()

@router.post("/", response_model=PostColorResponse, status_code=status.HTTP_201_CREATED)
def create_color(color_in: PostColorCreate, db: Session = Depends(get_db)):
    service = ColorService(db)
    return service.create_color(color_in)

@router.post("/by-list", response_model=List[PostColorResponse], status_code=status.HTTP_201_CREATED)
def create_color_by_list(color_in: List[PostColorCreate], db: Session = Depends(get_db)):
    service = ColorService(db)
    return service.create_color(color_in)

@router.get("/", response_model=List[PostColorResponse])
def read_colors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ColorService(db)
    return service.list_colors(skip=skip, limit=limit)

@router.get("/{color_id}", response_model=PostColorResponse)
def read_color(color_id: int, db: Session = Depends(get_db)):
    service = ColorService(db)
    return service.get_color(color_id)