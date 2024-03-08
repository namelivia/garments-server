from typing import List
from pydantic import BaseModel, Field
from app.garments.schemas import Garment


class Outfit(BaseModel):
    id: int
    garments: List[Garment] = Field(title="Garments for the outfit")
