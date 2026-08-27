import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, Timestamp
import enum

if TYPE_CHECKING:
    from app.models.users import User

class NotificationType(str, enum.Enum):
    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType), nullable=False)
    entity_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[Timestamp]

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    
    actor: Mapped["User"] = relationship("User", foreign_keys=[actor_id], lazy="selectin")