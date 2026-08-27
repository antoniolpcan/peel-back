from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import DateTime, func
from app.core.config import settings
from datetime import datetime, timezone
from typing import Annotated

engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0
    }
)

SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

Timestamp = Annotated[
    datetime, 
    mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
]