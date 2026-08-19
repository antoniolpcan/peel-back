import jwt
import secrets
import asyncio
from datetime import datetime, timedelta, timezone
from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.email import EmailService
from app.repositories.users import UserRepository
from app.repositories.password_reset import PasswordResetRepository
from app.repositories.token_blocklist import TokenBlocklistRepository
from app.core.security import verify_password, create_access_token, get_password_hash

DUMMY_PASSWORD_HASH = "$2b$12$L7R2QhZ.nO.E3A.B9C8D7.E6F5G4H3I2J1K0L9M8N7O6P5Q4R3S"

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.reset_repo = PasswordResetRepository(db)
        self.blocklist_repo = TokenBlocklistRepository(db)

    async def acess_auth(self, form_data):
        user = await self.user_repo.get_by_email(email=form_data.username)
        if user:
            is_password_valid = await asyncio.to_thread(
                verify_password, form_data.password, user.hashed_password
            )
        else:
            is_password_valid = await asyncio.to_thread(
                verify_password, form_data.password, DUMMY_PASSWORD_HASH
            )
            is_password_valid = False
        if not user or not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "access_token": create_access_token(subject=user.id),
            "token_type": "bearer",
        }

    async def request_password_reset(self, email: str, background_tasks: BackgroundTasks) -> dict:
        user = await self.user_repo.get_by_email(email)

        generic_message = {"message": "Se o e-mail estiver cadastrado, você receberá as instruções em breve."}
        if not user:
            return generic_message
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=15)

        await self.reset_repo.create_token(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )

        background_tasks.add_task(EmailService.send_reset_password, user.email, token)
        return generic_message

    async def reset_password(self, token_str: str, new_password: str) -> dict:
        db_token = await self.reset_repo.get_by_token(token_str)

        if not db_token or db_token.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de redefinição inválido ou já utilizado."
            )

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        token_expiry = db_token.expires_at.replace(tzinfo=None) if db_token.expires_at.tzinfo else db_token.expires_at

        if token_expiry < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O token de redefinição expirou. Solicite um novo."
            )

        user = await self.user_repo.get_by_id(db_token.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )

        new_hashed_password = await asyncio.to_thread(get_password_hash, new_password)
        
        await self.user_repo.update_password(user, new_hashed_password)
        await self.reset_repo.mark_as_used(db_token)

        return {"message": "Senha redefinida com sucesso!"}

    async def logout(self, token: str | None) -> None:
        if not token:
            return

        try:
            secret = settings.SECRET_KEY.get_secret_value() if hasattr(settings.SECRET_KEY, "get_secret_value") else settings.SECRET_KEY
            payload = jwt.decode(token, secret, algorithms=[settings.ALGORITHM])
            jti = payload.get("jti")
            exp = payload.get("exp")

            if jti and exp:
                expires_at = datetime.fromtimestamp(exp, tz=timezone.utc).replace(tzinfo=None)
                await self.blocklist_repo.add(jti=jti, expires_at=expires_at)
                
        except jwt.PyJWTError:
            pass