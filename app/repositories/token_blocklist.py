from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.token_blocklist import TokenBlocklist

class TokenBlocklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, jti: str, expires_at: datetime) -> TokenBlocklist:
        db_token = TokenBlocklist(jti=jti, expires_at=expires_at)
        self.db.add(db_token)
        await self.db.commit()
        return db_token

    async def is_blocked(self, jti: str) -> bool:
        result = await self.db.execute(
            select(TokenBlocklist).where(TokenBlocklist.jti == jti)
        )
        return result.scalar_one_or_none() is not None

    async def cleanup_expired(self) -> int:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        result = await self.db.execute(
            delete(TokenBlocklist).where(TokenBlocklist.expires_at < now)
        )
        await self.db.commit()
        return result.rowcount