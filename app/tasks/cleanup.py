import asyncio
import logging
from app.core.database import SessionLocal
from app.repositories.token_blocklist import TokenBlocklistRepository

logger = logging.getLogger(__name__)

async def cleanup_expired_tokens_loop():
    while True:
        try:
            await asyncio.sleep(86400) 
            async with SessionLocal() as db:
                repo = TokenBlocklistRepository(db)
                deleted_count = await repo.cleanup_expired()
                if deleted_count > 0:
                    logger.info(f"Limpeza Automática: {deleted_count} tokens expirados foram removidos da Blocklist.")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Erro inesperado na limpeza de tokens: {e}")