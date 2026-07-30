from pydantic import BaseModel
from app.schemas.user import BasicUserResponse

class FollowCreate(BaseModel):
    following_id: int

class FollowerResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    follower: BasicUserResponse | None = None
    class Config:
        from_attributes = True

class FollowingResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    following: BasicUserResponse | None = None

    class Config:
        from_attributes = True

class FollowStatsResponse(BaseModel):
    followers_count: int
    following_count: int