# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
from . import models, schemas
from app.garments.models import Garment
from app.garments.crud import wear, reject
from app.activities.models import Activity, ActivityGarmentType
from app.places.models import Place
from app.exceptions.exceptions import NotFoundException
from app.weather.weather import get_weather
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


def _generate_outfit(
    db: Session, place: str, weather: str, activity: str, types: List[str]
):
    query = db.query(Garment).filter(
        Garment.washing == False,
        Garment.thrown_away == False,
        Garment.place == place,
        Garment.activities.any(Activity.name == activity),
    )
    garments = []
    for garment_type in types:
        garments.append(_filter_garment_for_type(query, garment_type))

    db_outfit = models.Outfit(garments=garments, activity=activity, weather=weather)
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
        weather=outfit.weather,
        garments=outfit.garments,
        worn_on=outfit.worn_on,
    )


def get_outfits_for_date(db: Session, date: date):
    outfits = db.query(models.Outfit).filter(models.Outfit.worn_on == date)
    return [
        schemas.Outfit(
            id=outfit.id,
            activity=outfit.activity,
            weather=outfit.weather,
            garments=outfit.garments,
            worn_on=outfit.worn_on,
        )
        for outfit in outfits
    ]


def _get_garment_types_for_activity_and_weather(
    db: Session, activity: str, weather: str
):
    db_activity = db.query(Activity).filter(Activity.name == activity).first()
    if not db_activity:
        raise NotFoundException(f"Activity {activity} not found")

    activity_garment_types = db.query(ActivityGarmentType).filter(
        ActivityGarmentType.activity_id == db_activity.id,
        ActivityGarmentType.weather == weather,
    )

    return [
        activity_garment_type.garment_type.name
        for activity_garment_type in activity_garment_types
    ]


def get_outfit_for_place_and_activity(db: Session, place: str, activity: str):
    db_place = db.query(Place).filter(Place.name == place).first()
    if not db_place:
        raise NotFoundException(f"Place {place} not found")
    weather = get_weather(db_place)
    types = _get_garment_types_for_activity_and_weather(db, activity, weather)
    outfit = _generate_outfit(db, place, weather, activity, types)
    if not outfit:
        raise NotFoundException(f"No outfit available for {place} and {activity}")
    return schemas.Outfit(
        id=outfit.id,
        activity=outfit.activity,
        weather=outfit.weather,
        garments=outfit.garments,
        worn_on=outfit.worn_on,
    )


def get_outfit(db: Session, outfit_id: int):
    return db.query(models.Outfit).filter(models.Outfit.id == outfit_id).first()


def reject_outfit_garment(db: Session, outfit: models.Outfit, garment_id: int):
    garment = db.query(Garment).filter(Garment.id == garment_id).first()
    if not garment:
        raise NotFoundException(f"Garment {garment_id} not found")
    reject(db, garment)
    outfit.garments.remove(garment)

    new_garment_query = db.query(Garment).filter(
        Garment.washing == False,
        Garment.thrown_away == False,
        Garment.place == garment.place,
        Garment.activities.any(Activity.name == outfit.activity),
        Garment.id != garment_id,
    )
    new_garment = _filter_garment_for_type(new_garment_query, garment.garment_type)
    outfit.garments.append(new_garment)
    db.commit()
    db.refresh(outfit)
    return schemas.Outfit(
        id=outfit.id,
        activity=outfit.activity,
        weather=outfit.weather,
        garments=outfit.garments,
        worn_on=outfit.worn_on,
    )
