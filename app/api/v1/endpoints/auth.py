from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.services.auth import AuthService
from app.api.deps import get_auth_service

router = APIRouter()

@router.post("", response_model=Token)
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(get_auth_service)):
    return await service.acess_auth(form_data)