from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

from app.garment_types.models import GarmentType

activity_garment_type = Table(
    "activity_garment_type",
    Base.metadata,
    Column("activity_id", ForeignKey("activities.id")),
    Column("garment_type_id", ForeignKey("garment_types.id")),
)


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    garment_types = relationship(GarmentType, secondary=activity_garment_type)
