from sqlalchemy.orm import Session
import logging
from . import models, schemas

logger = logging.getLogger(__name__)


def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()


def get_activities(db: Session):
    return db.query(models.Activity).all()


def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(
        **activity.dict(),
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    logger.info("New activity created")
    return db_activity


def delete_activity(db: Session, activity: models.Activity):
    db.delete(activity)
    db.commit()
    logger.info("Activity deleted")
