from pydantic import BaseModel

class ColorBase(BaseModel):
    name: str
    hex_code: str

class ColorCreate(ColorBase):
    pass

class ColorResponse(ColorBase):
    id: int

    class Config:
        from_attributes = True