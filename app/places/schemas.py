from pydantic import BaseModel, Field


class PlaceBase(BaseModel):
    name: str = Field(title="Name for the place")
    latitude: str = Field(title="Latitude for the place")
    longitude: str = Field(title="Longitude for the place")


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        from_attributes = True
