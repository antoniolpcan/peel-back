from pydantic import BaseModel, ConfigDict

class ColorBase(BaseModel):
    name: str
    hex_code: str

class ColorCreate(ColorBase):
    pass

class ColorResponse(ColorBase):
    id: str
    model_config = ConfigDict(from_attributes=True)