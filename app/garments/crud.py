# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
import uuid
from . import models, schemas
from app.notifications.notifications import Notifications
from app.journaling.journaling import Journaling
import random

logger = logging.getLogger(__name__)


def get_garment(db: Session, garment_id: int):
    return db.query(models.Garment).filter(models.Garment.id == garment_id).first()


def get_random_garment(db: Session, place: str = None, garment_type: str = None):
    query = db.query(models.Garment)
    if place is not None:
        query = query.filter(models.Garment.place == place)
    if garment_type is not None:
        query = query.filter(models.Garment.garment_type == garment_type)
    row_count = int(query.count())
    return query.offset(int(row_count * random.random())).first()


def get_garments_for_place(db: Session, place: str):
    return db.query(models.Garment).filter(models.Garment.place == place).all()


# TODO: skip and limit
def get_garments(db: Session, place: str = None, garment_type: str = None):
    query = db.query(models.Garment)
    if place is not None:
        query = query.filter(models.Garment.place == place)
    if garment_type is not None:
        query = query.filter(models.Garment.garment_type == garment_type)
    return query.all()


def create_garment(db: Session, garment: schemas.GarmentCreate):
    db_garment = models.Garment(
        **garment.dict(),
        journaling_key=uuid.uuid4(),
    )
    db.add(db_garment)
    db.commit()
    db.refresh(db_garment)
    logger.info("New garment created")
    try:
        Notifications.send(f"A new garment called {db_garment.name} has been created")
    except Exception as err:
        logger.error(f"Notification could not be sent: {str(err)}")
    try:
        Journaling.create(
            db_garment.journaling_key,
            f"A new garment called {db_garment.name} has been created",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return db_garment


def update_garment(
    db: Session, garment_id: int, new_garment_data: schemas.GarmentUpdate
):
    garments = db.query(models.Garment).filter(models.Garment.id == garment_id)
    garments.update(new_garment_data, synchronize_session=False)
    db.commit()
    garment = garments.first()
    logger.info("Garment updated")
    try:
        Notifications.send(f"The garment {garment.name} has been updated")
    except Exception as err:
        logger.error(f"Notification could not be sent: {str(err)}")
    try:
        Journaling.create(
            garment.journaling_key,
            f"The garment {garment.name} has been updated",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return garment


def delete_garment(db: Session, garment: models.Garment):
    db.delete(garment)
    db.commit()
    logger.info("Garment deleted")
