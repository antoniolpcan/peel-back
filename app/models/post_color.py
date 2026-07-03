from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import PostIt

class PostColor(Base):
    __tablename__ = "post_colors"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    color_name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    
    post_its: Mapped[list["PostIt"]] = relationship(back_populates="color")
