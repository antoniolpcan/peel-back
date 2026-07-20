from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.posts import Post

class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(default=func.now(), nullable=False)
    
    post: Mapped["Post"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")