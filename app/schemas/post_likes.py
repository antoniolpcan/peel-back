from pydantic import BaseModel, ConfigDict

class PostLikeCreate(BaseModel):
    post_id: str

class PostLikeResponse(BaseModel):
    id: str
    user_id: str
    post_id: str
    model_config = ConfigDict(from_attributes=True)