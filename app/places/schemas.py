from pydantic import BaseModel, Field


class PlaceBase(BaseModel):
    name: str = Field(title="Name for the place")


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True
