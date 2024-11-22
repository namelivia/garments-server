from pydantic import BaseModel, Field


class Weather(BaseModel):
    weather: dict = Field(title="Weather")
