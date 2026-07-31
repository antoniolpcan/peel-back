from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime

if TYPE_CHECKING:
    from app.models.posts import Post
    from app.models.comments import Comment
    from app.models.post_likes import PostLike
    from app.models.media_files import MediaFile
    from app.models.follows import Follow

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    avatar_id: Mapped[Optional[int]] = mapped_column(ForeignKey("media_files.id"), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(default=func.now(), nullable=False)
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    comments: Mapped[List["Comment"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    likes: Mapped[List["PostLike"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

    avatar: Mapped[Optional["MediaFile"]] = relationship("MediaFile", foreign_keys=[avatar_id])
    media_files: Mapped[List["MediaFile"]] = relationship(back_populates="user", foreign_keys="[MediaFile.user_id]", cascade="all, delete-orphan", passive_deletes=True)
    followers: Mapped[List["Follow"]] = relationship(back_populates="following", foreign_keys="[Follow.following_id]", cascade="all, delete-orphan", passive_deletes=True)
    following: Mapped[List["Follow"]] = relationship(back_populates="follower", foreign_keys="[Follow.follower_id]", cascade="all, delete-orphan", passive_deletes=True)