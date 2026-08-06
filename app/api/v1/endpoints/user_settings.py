from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_user_setting_service
from app.schemas.user_settings import UserSettingResponse, UserSettingUpdate
from app.services.user_settings import UserSettingService
from app.models.users import User

router = APIRouter()

@router.get("/", response_model=UserSettingResponse)
async def get_my_settings(
        current_user: User = Depends(get_current_user),
        service: UserSettingService = Depends(get_user_setting_service)
    ):
    return await service.get_user_settings(user_id=current_user.id)

@router.patch("/", response_model=UserSettingResponse)
async def update_my_settings(
        setting_in: UserSettingUpdate,
        current_user: User = Depends(get_current_user),
        service: UserSettingService = Depends(get_user_setting_service)
    ):
    return await service.update_user_settings(user_id=current_user.id, setting_in=setting_in)