from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.color_repository import ColorRepository
from app.schemas.post_color import PostColorCreate
from app.models.post_color import PostColor

class ColorService:
    def __init__(self, db: Session):
        self.color_repo = ColorRepository(db)

    def create_color(self, color_in: PostColorCreate) -> PostColor:
        if self.color_repo.get_by_name(color_in.color_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cor já registrada."
            )
        return self.color_repo.create(color_in)

    def get_color(self, color_id: int) -> list[PostColor]:
        return self.color_repo.get_by_id(color_id)
    
    def list_colors(self, skip: int, limit: int) -> list[PostColor]:
        return self.color_repo.get_all(skip=skip, limit=limit)