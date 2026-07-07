from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def acess_auth(self, form_data):
        user = self.user_repo.get_by_email(email=form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "access_token": create_access_token(subject=user.id),
            "token_type": "bearer",
        }