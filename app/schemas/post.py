from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.enums import PostSortField, SortOrder
from app.schemas.color import ColorResponse
from app.schemas.user import BasicUserResponse

class PostBase(BaseModel):
    title: str
    body: str
    color_id: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    color_id: Optional[str] = None

class PostResponse(PostBase):
    id: str
    user_id: str
    likes: int = 0
    is_liked: bool = False
    created_at: Optional[datetime]
    color: Optional[ColorResponse] = None
    user: BasicUserResponse
    model_config = ConfigDict(from_attributes=True)

class PostQueryParams:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        title: Optional[str] = None,
        body: Optional[str] = None,
        user_id: Optional[str] = None,
        following_for_user_id: Optional[str] = None,
        order_by: PostSortField = PostSortField.created_at,
        sort_order: SortOrder = SortOrder.desc
    ):
        self.skip = skip
        self.limit = limit
        self.title = title
        self.body = body
        self.user_id = user_id
        self.following_for_user_id = following_for_user_id
        self.order_by = order_by
        self.sort_order = sort_order