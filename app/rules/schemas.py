from pydantic import BaseModel, Field


class ActivityGarmentTypeBase(BaseModel):
    garment_type: str = Field(title="Type of the garment")
    activity: str = Field(title="Activity for the garment")
    weather: str = Field(title="Weather for the garment")


class ActivityGarmentTypeCreate(ActivityGarmentTypeBase):
    pass
