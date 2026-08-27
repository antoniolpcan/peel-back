import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, Timestamp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User

class MediaFile(Base):
    __tablename__ = "media_files"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[Timestamp]
    
    user: Mapped["User"] = relationship(back_populates="media_files", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "url": self.url,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }