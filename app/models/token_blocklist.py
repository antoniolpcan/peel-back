from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False) 
    expires_at = Column(DateTime, nullable=False)