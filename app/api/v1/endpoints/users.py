from fastapi import APIRouter, Depends, status
from typing import List

from app.api.deps import get_user_service
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate, 
        service: UserService = Depends(get_user_service)
    ):
    return await service.create_user(user_in)

@router.get("", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
    return await service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    return await service.get_user(user_id)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate, service: UserService = Depends(get_user_service)):
    return await service.update_user(user_id, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    await service.delete_user(user_id)
    return None