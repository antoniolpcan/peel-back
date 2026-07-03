from pydantic import BaseModel, ConfigDict

class PostColorCreate(BaseModel):
    color_name: str

class PostColorResponse(BaseModel):
    id: int
    color_name: str
    model_config = ConfigDict(from_attributes=True)