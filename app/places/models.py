from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

PlacesBase = declarative_base()


class Place(PlacesBase):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
