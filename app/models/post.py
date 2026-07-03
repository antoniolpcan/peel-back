from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.post_color import PostColor

class PostIt(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    body: Mapped[str] = mapped_column(String(400), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    color_id: Mapped[int] = mapped_column(ForeignKey("post_colors.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    likes: Mapped[int] = mapped_column(default=0)
    has_liked: Mapped[bool] = mapped_column(default=False)
    
    user: Mapped["User"] = relationship(back_populates="post_its")
    color: Mapped["PostColor"] = relationship(back_populates="post_its")