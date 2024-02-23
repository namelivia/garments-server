from sqlalchemy.orm import Session
import logging
from . import models, schemas
from app.garments.crud import count_not_thrown_garments_for_place

logger = logging.getLogger(__name__)


def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()


def get_places(db: Session):
    places = db.query(models.Place).all()
    result = []
    # Filter out places that have no garments
    for place in places:
        place.garments = count_not_thrown_garments_for_place(db, place.name)
        if place.garments > 0:
            result.append(place)
    return result


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
    logger.info("Place deleted")
