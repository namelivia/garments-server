from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

GarmentTypesBase = declarative_base()


class GarmentType(GarmentTypesBase):
    __tablename__ = "garment_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
