from sqlalchemy import Column, Integer, String
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
    image = Column(String)
