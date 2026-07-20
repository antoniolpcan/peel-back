from pydantic import BaseModel

class PostLikeCreate(BaseModel):
    post_id: int

class PostLikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True