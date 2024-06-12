from pydantic import BaseModel, Field


class Weather(BaseModel):
    weather: str = Field(title="Weather")
