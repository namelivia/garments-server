from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.activities.schemas import Activity
import datetime


class GarmentBase(BaseModel):
    name: str = Field(title="Name for the garment")
    garment_type: str = Field(title="Type of the garment")
    color: str = Field(title="Color of the garment")
    status: str = Field(title="Status of the garment")
    place: str = Field(title="Place of the garment")
    activity: str = Field(title="Activity for the garment")
    wear_to_wash: int = Field(title="Times to wear before washing")
    image: Optional[str] = Field(None, title="Image url for the garment")


class GarmentCreate(GarmentBase):
    pass


class GarmentUpdate(GarmentBase):
    pass


class Garment(GarmentBase):
    id: int
    worn: int = Field(title="Times worn")
    total_worn: int = Field(title="Total times worn")
    times_rejected: int = Field(title="Total times rejected")
    washing: bool = Field(title="If the garment is pending to be washed")
    thrown_away: bool = Field(title="If the garment has been thrown away")
    journaling_key: UUID = Field(title="Parent key for the journal entry")
    activities: List[Activity] = Field(title="Activities for the outfit")

    class Config:
        from_attributes = True


class JournalEntryBase(BaseModel):
    message: str = Field(title="Message contents")


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntry(JournalEntryBase):
    id: int
    key: UUID = Field(title="Parent key for the journal entry")
    timestamp: datetime.datetime = Field(title="Entry timestamp")
