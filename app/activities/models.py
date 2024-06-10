from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base
from typing import List

from app.garment_types.models import GarmentType


class ActivityGarmentType(Base):
    __tablename__ = "activity_garment_type"
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"), primary_key=True
    )
    garment_type_id: Mapped[int] = mapped_column(
        ForeignKey("garment_types.id"), primary_key=True
    )
    weather = Column("weather", String, nullable=False)
    garment_type: Mapped["GarmentType"] = relationship()


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    garment_types: Mapped[List["ActivityGarmentType"]] = relationship()
