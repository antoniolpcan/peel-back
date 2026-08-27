import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, Timestamp

if TYPE_CHECKING:
    from app.models.posts import Post
    from app.models.comments import Comment
    from app.models.post_likes import PostLike
    from app.models.media_files import MediaFile
    from app.models.follows import Follow
    from app.models.notifications import Notification
    from app.models.user_settings import UserSetting
    from app.models.chat import ChatMember

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    avatar_id: Mapped[Optional[str]] = mapped_column(ForeignKey("media_files.id"), nullable=True)
    created_at: Mapped[Timestamp]
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    comments: Mapped[List["Comment"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    likes: Mapped[List["PostLike"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

    avatar: Mapped[Optional["MediaFile"]] = relationship("MediaFile", foreign_keys=[avatar_id], lazy="selectin")
    media_files: Mapped[List["MediaFile"]] = relationship(back_populates="user", foreign_keys="[MediaFile.user_id]", cascade="all, delete-orphan", passive_deletes=True)
    followers: Mapped[List["Follow"]] = relationship(back_populates="following", foreign_keys="[Follow.following_id]", cascade="all, delete-orphan", passive_deletes=True)
    following: Mapped[List["Follow"]] = relationship(back_populates="follower", foreign_keys="[Follow.follower_id]", cascade="all, delete-orphan", passive_deletes=True)
    settings: Mapped[Optional["UserSetting"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user", foreign_keys="[Notification.user_id]", cascade="all, delete-orphan")
    chats: Mapped[List["ChatMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")