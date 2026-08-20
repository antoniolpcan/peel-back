from fastapi import APIRouter, Depends, status
from typing import List
from app.api.deps import get_follow_service, get_current_user 
from app.services.follows import FollowService
from app.schemas.follows import FollowCreate, FollowingResponse, FollowerResponse, FollowStatsResponse
from app.models.users import User 

router = APIRouter()

@router.post("/", response_model=FollowerResponse, status_code=status.HTTP_201_CREATED)
async def follow_user(
        follow_data: FollowCreate,
        current_user: User = Depends(get_current_user),
        service: FollowService = Depends(get_follow_service)
    ):
    return await service.follow_user(current_user.id, follow_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
        user_id: str,
        current_user: User = Depends(get_current_user),
        service: FollowService = Depends(get_follow_service)
    ):
    await service.unfollow_user(current_user.id, user_id)

@router.get("/followers/{user_id}", response_model=List[FollowerResponse])
async def get_followers(
        user_id: str,
        service: FollowService = Depends(get_follow_service)
    ):
    return await service.get_followers(user_id)

@router.get("/following/{user_id}", response_model=List[FollowingResponse])
async def get_following(
        user_id: str,
        service: FollowService = Depends(get_follow_service)
    ):
    return await service.get_following(user_id)

@router.get("/{user_id}/stats", response_model=FollowStatsResponse)
async def get_user_follow_stats(
        user_id: str,
        service: FollowService = Depends(get_follow_service)
    ):
    return await service.get_follow_stats(user_id)