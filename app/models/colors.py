from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.posts import Post

class Color(Base):
    __tablename__ = "colors"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="color")
