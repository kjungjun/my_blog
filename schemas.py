from pydantic import BaseModel

class ImageBase(BaseModel):
    filename: str
    filepath: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True
