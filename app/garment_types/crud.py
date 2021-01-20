from sqlalchemy.orm import Session
import logging
from . import models, schemas

logger = logging.getLogger(__name__)


def get_garment_type(db: Session, garment_type_id: int):
    return (
        db.query(models.GarmentType)
        .filter(models.GarmentType.id == garment_type_id)
        .first()
    )


def get_garment_types(db: Session):
    return db.query(models.GarmentType).all()


def create_garment_type(db: Session, garment_type: schemas.GarmentTypeCreate):
    db_garment_type = models.GarmentType(
        **garment_type.dict(),
    )
    db.add(db_garment_type)
    db.commit()
    db.refresh(db_garment_type)
    logger.info("New garment type created")
    return db_garment_type


def delete_garment_type(db: Session, garment: models.GarmentType):
    db.delete(garment)
    db.commit()
    logger.info("Garment type deleted")
