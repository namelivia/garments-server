# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
from . import models, schemas
from app.garments.models import Garment
from app.garments.crud import wear
from app.activities.models import Activity
from app.exceptions.exceptions import NotFoundException
import random
from datetime import date
from typing import List

logger = logging.getLogger(__name__)


def _filter_garment_for_type(garments, garment_type):
    filtered_garments = garments.filter(Garment.garment_type == garment_type)
    if filtered_garments.count() == 0:
        raise NotFoundException(f"No garment of type {garment_type} found")
    return filtered_garments.offset(
        int(filtered_garments.count() * random.random())
    ).first()


def _generate_outfit(db: Session, place: str, activity: str, types: List[str]):
    query = db.query(Garment).filter(
        Garment.washing == False,
        Garment.thrown_away == False,
        Garment.place == place,
        Garment.activities.any(Activity.name == activity),
    )
    garments = []
    for garment_type in types:
        garments.append(_filter_garment_for_type(query, garment_type))

    db_outfit = models.Outfit(garments=garments, activity=activity)
    db.add(db_outfit)
    db.commit()
    db.refresh(db_outfit)
    return db_outfit


def wear_outfit(db: Session, outfit: models.Outfit):
    today = date.today()
    outfit.worn_on = today
    [wear(db, garment) for garment in outfit.garments]
    db.refresh(outfit)
    return schemas.Outfit(
        id=outfit.id,
        activity=outfit.activity,
        garments=outfit.garments,
        worn_on=outfit.worn_on,
    )


def get_outfits_for_date(db: Session, date: date):
    outfits = db.query(models.Outfit).filter(models.Outfit.worn_on == date)
    return [
        schemas.Outfit(
            id=outfit.id,
            activity=outfit.activity,
            garments=outfit.garments,
            worn_on=outfit.worn_on,
        )
        for outfit in outfits
    ]


def get_outfit_for_place_and_activity(db: Session, place: str, activity: str):
    db_activity = db.query(Activity).filter(Activity.name == activity).first()
    if not db_activity:
        raise NotFoundException(f"Activity {activity} not found")
    types = [garment_type.name for garment_type in db_activity.garment_types]
    outfit = _generate_outfit(db, place, activity, types)
    if not outfit:
        raise NotFoundException(f"No outfit available for {place} and {activity}")
    return schemas.Outfit(
        id=outfit.id,
        activity=outfit.activity,
        garments=outfit.garments,
        worn_on=outfit.worn_on,
    )


def get_outfit(db: Session, outfit_id: int):
    return db.query(models.Outfit).filter(models.Outfit.id == outfit_id).first()
