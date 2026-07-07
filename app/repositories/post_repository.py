from sqlalchemy.orm import Session
from app.models.post import PostIt
from app.schemas.post import PostItCreate, PostItUpdate

class PostItRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> PostIt | None:
        return self.db.query(PostIt).filter(PostIt.id == post_id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> list[PostIt]:
        return self.db.query(PostIt).offset(skip).limit(limit).all()

    def create(self, obj_in: PostItCreate) -> PostIt:
        db_obj = PostIt(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: PostIt, obj_in: PostItUpdate) -> PostIt:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
        
    def delete(self, db_obj: PostIt) -> bool:
        try:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
        
    def save(self) -> None:
        self.db.commit()