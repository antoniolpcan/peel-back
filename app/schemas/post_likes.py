from pydantic import BaseModel, ConfigDict

class PostLikeCreate(BaseModel):
    post_id: int

class PostLikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    model_config = ConfigDict(from_attributes=True)