from fastapi import APIRouter, Depends, status
from typing import List

from app.api.deps import get_user_service, get_current_user 
from app.schemas.user import UserCreate, UserResponse, UserUpdate, BasicUserResponse
from app.services.users import UserService
from app.models.users import User

router = APIRouter()

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(payload)

@router.get("", response_model=List[BasicUserResponse])
async def read_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
    return await service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=BasicUserResponse)
async def get_user_profile(user_id: str, service: UserService = Depends(get_user_service)):
    return await service.get_user(user_id)

@router.patch("/me", response_model=UserResponse)
async def update_current_user(payload: UserUpdate, service: UserService = Depends(get_user_service),
                        current_user: User = Depends(get_current_user)):
    return await service.update_user(user_id=current_user.id, user_in=payload)
