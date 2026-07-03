from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.post_color import PostColor
from app.schemas.post_color import PostColorCreate

class ColorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> PostColor | None:
        return self.db.query(PostColor).filter(PostColor.id == post_id).first()
    
    def get_by_name(self, color_name: str) -> PostColor | None:
        return self.db.query(PostColor).filter(PostColor.color_name == color_name).first()
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> list[PostColor]:
        return self.db.query(PostColor).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PostColor]:
        return list(self.db.scalars(select(PostColor).offset(skip).limit(limit)).all())

    def create(self, obj_in: PostColorCreate) -> PostColor:
        db_obj = PostColor(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: PostColor) -> None:
        self.db.delete(db_obj)
        self.db.commit()

    def save(self) -> None:
        self.db.commit()