from pydantic import BaseModel, ConfigDict
from app.schemas.user import BasicUserResponse

class FollowCreate(BaseModel):
    following_id: str

class FollowerResponse(BaseModel):
    id: str
    follower_id: str
    following_id: str
    follower: BasicUserResponse | None = None
    model_config = ConfigDict(from_attributes=True)

class FollowingResponse(BaseModel):
    id: str
    follower_id: str
    following_id: str
    following: BasicUserResponse | None = None
    model_config = ConfigDict(from_attributes=True)

class FollowStatsResponse(BaseModel):
    followers_count: int
    following_count: int