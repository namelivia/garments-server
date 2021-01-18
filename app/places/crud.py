from sqlalchemy.orm import Session
import logging
from . import models, schemas

logger = logging.getLogger(__name__)


def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()


def get_places(db: Session):
    return db.query(models.Place).all()


def create_place(db: Session, place: schemas.PlaceCreate):
    db_place = models.Place(
        **place.dict(),
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    logger.info("New place created")
    return db_place


def delete_place(db: Session, garment: models.Place):
    db.delete(garment)
    db.commit()
    logger.info("Garment deleted")
