from sqlalchemy import Column, Integer, String, Table, ForeignKey

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
    garments = relationship(Garment, secondary=outfit_garment)
