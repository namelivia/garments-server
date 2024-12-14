from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base

from app.garment_types.models import GarmentType


class Rule(Base):
    __tablename__ = "rules"
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"), primary_key=True
    )
    garment_type_id: Mapped[int] = mapped_column(
        ForeignKey("garment_types.id"), primary_key=True
    )
    weather = Column("weather", String, nullable=False, primary_key=True)
    garment_type: Mapped["GarmentType"] = relationship()
    activity: Mapped["Activity"] = relationship()
