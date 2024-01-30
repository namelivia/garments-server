from typing import Optional
from pydantic import BaseModel, Field


class Outfit(BaseModel):
    socks: str = Field(title="Name for the socks")
    underpants: str = Field(title="Name for the underpants")
    pants: str = Field(title="Name for the pants")
    tshirt: str = Field(title="Name for the tshirt")
    shoe: str = Field(title="Name for the shoe")
