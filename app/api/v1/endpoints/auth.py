from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.api.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("", response_model=Token)
def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
    ):
    auth = AuthService(db)
    return auth.acess_auth(form_data)