from typing import Optional
from pydantic import BaseModel, Field


class Outfit(BaseModel):
    garments: dict = Field(
        ...,
        description="A dictionary with the garment type as key and the name of the garment as value",
    )
