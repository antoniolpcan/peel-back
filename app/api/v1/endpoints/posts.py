from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_post_service, get_current_user 
from app.schemas.post import PostItBase, PostItResponse, PostItUpdate
from app.services.post_service import PostItService
from app.models.user import User 

router = APIRouter()

@router.post("", response_model=PostItResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
        payload: PostItBase, 
        service: PostItService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.create_post(payload, user_id=current_user.id)

@router.get("", response_model=List[PostItResponse])
async def get_posts(
        skip: int = 0, 
        limit: int = 100, 
        service: PostItService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.list_posts(skip=skip, limit=limit)

@router.post("/{post_id}/like", response_model=PostItResponse)
async def like_post(
        post_id: int, 
        service: PostItService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.toggle_like(post_id, user_id=current_user.id)

@router.put("/{post_id}", response_model=PostItResponse)
async def update_post(
        payload: PostItUpdate, 
        post_id: int, 
        service: PostItService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.update_post(post_id, post_in=payload)
    
@router.delete("/{post_id}")
async def delete_post(
        post_id: int, 
        service: PostItService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.delete_post(post_id, user_id=current_user.id)