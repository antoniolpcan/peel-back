from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user 
from app.schemas.post import PostItCreate, PostItResponse, PostItUpdate
from app.services.post_service import PostItService
from app.models.user import User 

router = APIRouter()

@router.post("/", response_model=PostItResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostItCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    service = PostItService(db)
    return service.create_post(payload, user_id=current_user.id)

@router.get("/", response_model=List[PostItResponse])
def get_posts(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    service = PostItService(db)
    return service.list_posts(skip=skip, limit=limit)

@router.post("/{post_id}/like", response_model=PostItResponse)
def like_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    service = PostItService(db)
    return service.toggle_like(post_id, user_id=current_user.id)

@router.put("/{post_id}", response_model=PostItResponse)
def like_post(
    payload: PostItUpdate, 
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    service = PostItService(db)
    return service.update_post(post_id, post_in=payload)
    
@router.delete("/{post_id}")
def like_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    service = PostItService(db)
    return service.delete_post(post_id, user_id=current_user.id)