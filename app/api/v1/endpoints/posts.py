from fastapi import APIRouter, Depends, status
from typing import List
from app.api.deps import get_post_service, get_comment_service, get_current_user 
from app.schemas.post import PostBase, PostResponse, PostUpdate
from app.schemas.comments import CommentCreate, CommentResponse
from app.services.posts import PostService
from app.services.comments import CommentService
from app.models.users import User 

router = APIRouter()

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostBase, 
                      service: PostService = Depends(get_post_service),
                      current_user: User = Depends(get_current_user)):
    return await service.create_post(payload, user_id=current_user.id)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, service: PostService = Depends(get_post_service)):
    return await service.get_post_by_id(post_id)

@router.get("", response_model=List[PostResponse])
async def list_posts(skip: int = 0, limit: int = 100, service: PostService = Depends(get_post_service)):
    return await service.search_posts(skip=skip, limit=limit)

@router.post("/{post_id}", response_model=PostResponse)
async def update_post(
        payload: PostUpdate, 
        post_id: int, 
        service: PostService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.update_post(post_id, post_in=payload, user_id=current_user.id)
    
@router.delete("/{post_id}")
async def delete_post(
        post_id: int, 
        service: PostService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.delete_post(post_id, user_id=current_user.id)

@router.post("/{post_id}/like", response_model=PostResponse)
async def like_post(post_id: int, service: PostService = Depends(get_post_service),
        current_user: User = Depends(get_current_user)
    ):
    return await service.toggle_post_like(current_user.id, post_id)

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, content: str, service: CommentService = Depends(get_comment_service), current_user: User = Depends(get_current_user)):
    payload = CommentCreate(content=content, post_id=post_id)
    return await service.create_comment(comment_in=payload, user_id=current_user.id)

@router.get("/{post_id}/comments", response_model=list[CommentResponse])
async def get_comments(post_id: int, service: CommentService = Depends(get_comment_service)):
    return await service.get_comments_for_post(post_id=post_id)