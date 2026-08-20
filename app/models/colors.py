import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.posts import Post

class Color(Base):
    __tablename__ = "colors"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    hex_code: Mapped[str] = mapped_column(String(7), nullable=False)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="color")
