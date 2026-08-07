from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth import AuthService
from app.api.deps import get_auth_service

router = APIRouter()

@router.post("", response_model=Token)
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(get_auth_service)):
    return await service.acess_auth(form_data)

@router.post("/forgot-password")
async def forgot_password(
        body: ForgotPasswordRequest,
        background_tasks: BackgroundTasks,
        service: AuthService = Depends(get_auth_service)
    ):
    return await service.request_password_reset(body.email, background_tasks)


@router.post("/reset-password")
async def reset_password(
        body: ResetPasswordRequest,
        service: AuthService = Depends(get_auth_service)
    ):
    return await service.reset_password(body.token, body.new_password)