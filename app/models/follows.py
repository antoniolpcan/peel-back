import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, Timestamp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User

class Follow(Base):
    __tablename__ = "follows"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    follower_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    following_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[Timestamp]
    
    follower: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[follower_id])
    following: Mapped["User"] = relationship(back_populates="following", foreign_keys=[following_id])