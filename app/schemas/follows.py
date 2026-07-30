from pydantic import BaseModel
from datetime import datetime

class UserSimpleResponse(BaseModel):
    id: int
    name: str
    username: str | None = None
    avatar_id: int | None = None
    class Config:
        from_attributes = True

class FollowCreate(BaseModel):
    following_id: int

class FollowerResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    follower: UserSimpleResponse | None = None
    class Config:
        from_attributes = True

class FollowingResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    following: UserSimpleResponse | None = None

    class Config:
        from_attributes = True