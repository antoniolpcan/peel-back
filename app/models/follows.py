from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User

class Follow(Base):
    __tablename__ = "follows"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    
    follower: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[follower_id])
    following: Mapped["User"] = relationship(back_populates="following", foreign_keys=[following_id])