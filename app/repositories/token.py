from datetime import datetime
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.token import Token

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_token(
        self, 
        token: str, 
        expires_at: datetime, 
        user_id: str | None = None, 
        email: str | None = None
    ) -> Token:
        
        if user_id:
            stmt = (
                update(Token)
                .where(Token.user_id == user_id, Token.used == False)
                .values(used=True)
            )
            await self.db.execute(stmt)
        elif email:
            stmt = (
                update(Token)
                .where(Token.email == email, Token.used == False)
                .values(used=True)
            )
            await self.db.execute(stmt)

        reset_token = Token(
            user_id=user_id,
            email=email,
            token=token,
            expires_at=expires_at
        )
        self.db.add(reset_token)
        await self.db.commit()
        await self.db.refresh(reset_token)
        return reset_token

    async def get_by_token(self, token_str: str) -> Token | None:
        stmt = select(Token).where(Token.token == token_str)
        return await self.db.scalar(stmt)

    async def get_by_email_and_token(self, email: str, token_str: str) -> Token | None:
        stmt = select(Token).where(
            and_(
                Token.email == email,
                Token.token == token_str
            )
        )
        return await self.db.scalar(stmt)

    async def mark_as_used(self, db_token: Token) -> None:
        db_token.used = True
        self.db.add(db_token)
        await self.db.commit()