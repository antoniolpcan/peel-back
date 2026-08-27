import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, Timestamp

if TYPE_CHECKING:
    from app.models.users import User

class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[Timestamp]
    
    members: Mapped[List["ChatMember"]] = relationship(
        back_populates="chats", 
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    messages: Mapped[List["Message"]] = relationship(back_populates="chats", cascade="all, delete-orphan")


class ChatMember(Base):
    __tablename__ = "chat_members"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    joined_at: Mapped[Timestamp]
    
    chats: Mapped["Chat"] = relationship(back_populates="members")
    
    user: Mapped["User"] = relationship(
        back_populates="chats",
        lazy="selectin"
    )


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[Timestamp]
    
    chats: Mapped["Chat"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship("User", lazy="selectin")