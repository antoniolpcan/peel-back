from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.password_reset import PasswordResetToken

class PasswordResetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_token(self, user_id: int, token: str, expires_at: datetime) -> PasswordResetToken:
        stmt = (
            update(PasswordResetToken)
            .where(PasswordResetToken.user_id == user_id, PasswordResetToken.used == False)
            .values(used=True)
        )
        await self.db.execute(stmt)

        reset_token = PasswordResetToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        self.db.add(reset_token)
        await self.db.commit()
        await self.db.refresh(reset_token)
        return reset_token

    async def get_by_token(self, token_str: str) -> PasswordResetToken | None:
        stmt = select(PasswordResetToken).where(PasswordResetToken.token == token_str)
        return await self.db.scalar(stmt)

    async def mark_as_used(self, db_token: PasswordResetToken) -> None:
        db_token.used = True
        self.db.add(db_token)
        await self.db.commit()