from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.post_repository import PostItRepository
from app.schemas.post import PostItCreate
from app.models.post import PostIt

class PostItService:
    def __init__(self, db: Session):
        self.post_repo = PostItRepository(db)

    def create_post(self, post_in: PostItCreate, user_id: int) -> PostIt:
        return self.post_repo.create(post_in)

    def list_posts(self, skip: int, limit: int) -> list[PostIt]:
        return self.post_repo.get_multi(skip=skip, limit=limit)

    def toggle_like(self, post_id: int, user_id: int) -> PostIt:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post-It não encontrado.")
        if post.has_liked:
            post.likes -= 1
            post.has_liked = False
        else:
            post.likes += 1
            post.has_liked = True
        self.post_repo.save()
        return post