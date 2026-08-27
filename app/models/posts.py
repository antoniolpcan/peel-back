import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, Timestamp

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.comments import Comment
    from app.models.post_likes import PostLike
    from app.models.colors import Color

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    color_id: Mapped[Optional[str]] = mapped_column(ForeignKey("colors.id"), nullable=True)
    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[Timestamp]

    user: Mapped["User"] = relationship(back_populates="posts")
    color: Mapped[Optional["Color"]] = relationship(back_populates="posts")
    
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan", passive_deletes=True)
    post_likes: Mapped[List["PostLike"]] = relationship(back_populates="post", cascade="all, delete-orphan", passive_deletes=True)