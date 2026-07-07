from typing import Generator
from app.core.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from pydantic import ValidationError

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
        )
    user = UserRepository(db)
    user.get_by_id(user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user