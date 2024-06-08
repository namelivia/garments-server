from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    name: str = Field(title="Name for the activity")


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int

    class Config:
        from_attributes = True
