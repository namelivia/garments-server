from typing import List, Optional
from pydantic import BaseModel, Field
from app.garments.schemas import Garment
import datetime


class Outfit(BaseModel):
    id: int
    worn_on: Optional[datetime.datetime] = Field(title="When was the outfit worn")
    garments: List[Garment] = Field(title="Garments for the outfit")
