from pydantic import BaseModel, Field


class GarmentTypeBase(BaseModel):
    name: str = Field(title="Name for the garment type")


class GarmentTypeCreate(GarmentTypeBase):
    pass


class GarmentType(GarmentTypeBase):
    id: int

    class Config:
        from_attributes = True
