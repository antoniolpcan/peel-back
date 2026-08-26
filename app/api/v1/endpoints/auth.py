from fastapi import APIRouter, Depends, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, ForgotPasswordRequest, ResetPasswordRequest, VerifyCodeRequest
from app.services.auth import AuthService
from app.api.deps import get_auth_service, get_token_hybrid

router = APIRouter()

@router.post("", response_model=Token)
async def login_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(get_auth_service)
    ):
    auth_data = await service.acess_auth(form_data)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {auth_data['access_token']}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800
    )
    return auth_data

@router.post("/send-mail-verification")
async def send_mail_verify(
        body: ForgotPasswordRequest,
        background_tasks: BackgroundTasks,
        service: AuthService = Depends(get_auth_service)
    ):
    return await service.request_email_verify(body.email, background_tasks)

@router.post("/verify-code")
async def verify_code(
        body: VerifyCodeRequest,
        service: AuthService = Depends(get_auth_service)
    ):
    return await service.verify_email_code(body.email, body.code)

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

@router.post("/logout")
async def logout(
        response: Response,
        token: str | None = Depends(get_token_hybrid),
        service: AuthService = Depends(get_auth_service),
    ):
    await service.logout(token)
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Logout realizado com sucesso"}