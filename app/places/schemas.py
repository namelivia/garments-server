from pydantic import BaseModel, Field


class PlaceBase(BaseModel):
    name: str = Field(title="Name for the garment")


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True
