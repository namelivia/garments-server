from sqlalchemy import Column, Integer, String
from app.database import Base


class GarmentType(Base):
    __tablename__ = "garment_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
