# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
import uuid
from . import models, schemas
from app.notifications.notifications import Notifications
from app.journaling.journaling import Journaling

logger = logging.getLogger(__name__)


def get_garment(db: Session, garment_id: int):
    return db.query(models.Garment).filter(models.Garment.id == garment_id).first()


def get_garments_for_place(db: Session, place: str):
    return db.query(models.Garment).filter(models.Garment.place == place).all()


# TODO: skip and limit
def get_garments(db: Session):
    return db.query(models.Garment).all()


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


def delete_garment(db: Session, garment: models.Garment):
    db.delete(garment)
    db.commit()
    logger.info("Garment deleted")
