from sqlalchemy import Column, Integer, String

from app.database import Base


class WeatherRange(Base):
    __tablename__ = "weather_ranges"
    id = Column(Integer, primary_key=True, index=True)
    max = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
