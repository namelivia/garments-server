from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
import datetime


class GarmentBase(BaseModel):
    name: str = Field(title="Name for the garment")
    garment_type: str = Field(title="Type of the garment")
    color: str = Field(title="Color of the garment")
    status: str = Field(title="Status of the garment")
    image: Optional[str] = Field(title="Image url for the garment")


class GarmentCreate(GarmentBase):
    pass


class Garment(GarmentBase):
    id: int
    journaling_key: UUID = Field(title="Parent key for the journal entry")

    class Config:
        orm_mode = True


class JournalEntryBase(BaseModel):
    message: str = Field(title="Message contents")


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntry(JournalEntryBase):
    id: int
    key: UUID = Field(title="Parent key for the journal entry")
    timestamp: datetime.datetime = Field(title="Entry timestamp")
