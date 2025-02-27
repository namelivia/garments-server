# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
import uuid
from . import models, schemas
from app.journaling.journaling import Journaling
from app.activities.models import Activity
from app.notifications.notifications import Notifications
from app.exceptions.exceptions import NotFoundException
import random

logger = logging.getLogger(__name__)


def get_garment(db: Session, garment_id: int):
    return db.query(models.Garment).filter(models.Garment.id == garment_id).first()


def get_random_garment(
    db: Session, place: str = None, garment_type: str = None, activity: str = None
):
    query = db.query(models.Garment).filter(
        models.Garment.washing == False,
        models.Garment.thrown_away == False,
    )
    if place is not None:
        query = query.filter(models.Garment.place == place)
    if garment_type is not None:
        query = query.filter(models.Garment.garment_type == garment_type)
    if activity is not None:
        query = query.filter(models.Garment.activities.any(Activity.name == activity))
    row_count = int(query.count())
    return query.offset(int(row_count * random.random())).first()


def get_garments_for_place(db: Session, place: str):
    return db.query(models.Garment).filter(models.Garment.place == place).all()


def count_not_thrown_garments_for_place(db: Session, place: str):
    return (
        db.query(models.Garment)
        .filter(models.Garment.place == place, models.Garment.thrown_away == False)
        .count()
    )


# TODO: skip and limit
def get_garments(
    db: Session, place: str = None, garment_type: str = None, activity: str = None
):
    query = db.query(models.Garment).filter(models.Garment.thrown_away == False)
    if place is not None:
        query = query.filter(models.Garment.place == place)
    if activity is not None:
        query = query.filter(models.Garment.activities.any(Activity.name == activity))
    if garment_type is not None:
        query = query.filter(models.Garment.garment_type == garment_type)
    return query.all()


def get_washing_garments(db: Session):
    query = db.query(models.Garment).filter(
        models.Garment.washing == True, models.Garment.thrown_away == False
    )
    return query.all()


def get_thrown_away_garments(db: Session):
    query = db.query(models.Garment).filter(models.Garment.thrown_away == True)
    return query.all()


def create_garment(db: Session, garment: schemas.GarmentCreate):
    db_garment = models.Garment(
        **garment.dict(exclude={"activity"}),
        journaling_key=uuid.uuid4(),
        worn=0,
        total_worn=0,
        times_rejected=0,
        washing=False,
        thrown_away=False,
    )
    activity = db.query(Activity).filter(Activity.name == garment.activity).first()
    if not activity:
        raise NotFoundException(f"Activity {garment.activity} not found")
    db_garment.activities.append(activity)
    db.add(db_garment)
    db.commit()
    db.refresh(db_garment)
    logger.info("New garment created")
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
    garments.update(new_garment_data.dict(), synchronize_session=False)
    db.commit()
    garment = garments.first()
    logger.info("Garment updated")
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


def send_to_wash(db: Session, garment: models.Garment):
    garment.washing = True
    db.commit()
    db.refresh(garment)
    logger.info("Sending garment {garment.name} to wash")
    try:
        Journaling.create(
            garment.journaling_key,
            f"Garment {garment.name} sent to wash",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return garment


def wear(db: Session, garment: models.Garment):
    garment.worn += 1
    garment.total_worn += 1
    garment.washing = garment.worn >= garment.wear_to_wash
    db.commit()
    db.refresh(garment)
    logger.info(f"Wearing garment {garment.name}")
    try:
        if garment.washing and garment.wear_to_wash > 1:
            Notifications.send(
                f"Garment {garment.name} has been worn {garment.worn} times and needs to be washed"
            )
    except Exception as err:
        logger.error(f"Could not send notification: {str(err)}")
    try:
        Journaling.create(
            garment.journaling_key,
            f"Wearing {garment.name}",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return garment


def reject(db: Session, garment: models.Garment):
    garment.times_rejected += 1
    db.commit()
    db.refresh(garment)
    logger.info(f"Rejecting garment {garment.name}")
    try:
        Journaling.create(
            garment.journaling_key,
            f"Rejecting {garment.name}",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return garment


def wash(db: Session, garment: models.Garment):
    garment.worn = 0
    garment.washing = False
    db.commit()
    db.refresh(garment)
    logger.info(f"Washing garment {garment.name}")
    try:
        Journaling.create(
            garment.journaling_key,
            f"Garment {garment.name} has been washed",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return garment


def throw_away(db: Session, garment: models.Garment):
    garment.washing = False
    garment.thrown_away = True
    db.commit()
    db.refresh(garment)
    logger.info(f"Throwing away garment {garment.name}")
    try:
        Journaling.create(
            garment.journaling_key,
            f"Garment {garment.name} has been thrown_away",
        )
    except Exception as err:
        logger.error(f"Could not add journal entry: {str(err)}")
    return garment
