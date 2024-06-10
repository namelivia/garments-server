from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime

from sqlalchemy.orm import relationship
from app.database import Base
from app.garments.models import Garment

outfit_garment = Table(
    "outfit_garment",
    Base.metadata,
    Column("outfit_id", ForeignKey("outfits.id")),
    Column("garment_id", ForeignKey("garments.id")),
)


class Outfit(Base):
    __tablename__ = "outfits"
    id = Column(Integer, primary_key=True, index=True)
    activity = Column(String, nullable=False)
    garments = relationship(Garment, secondary=outfit_garment)
    worn_on = Column(DateTime)
    weather = Column(String, nullable=False)
