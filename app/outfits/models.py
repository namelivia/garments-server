from sqlalchemy import Column, Integer, String
from app.database import Base
from app.garments.models import Garment


class Outfit(Base):
    __tablename__ = "outfits"
    id = Column(Integer, primary_key=True, index=True)
