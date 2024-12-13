from pydantic import BaseModel


class ActivityGarmentTypeBase(BaseModel):
    activity_id: int
    garment_type_id: int
    weather: str


class ActivityGarmentTypeCreate(ActivityGarmentTypeBase):
    pass
