from sqlalchemy import Column, Integer, String, Boolean
from fastapi_utils.guid_type import GUID
from app.database import Base


class Garment(Base):
    __tablename__ = "garments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    garment_type = Column(String, nullable=False)
    color = Column(String, nullable=False)
    status = Column(String, nullable=False)
    place = Column(String, nullable=False)
    journaling_key = Column(GUID, nullable=False)
    worn = Column(Integer, nullable=False)
    total_worn = Column(Integer, nullable=False)
    wear_to_wash = Column(Integer, nullable=False)
    washing = Column(Boolean, nullable=False)
    thrown_away = Column(Boolean, nullable=False)
    image = Column(String)
