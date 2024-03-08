# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
from . import models, schemas
from app.garments.models import Garment
from app.garments.crud import wear
import random
from typing import List

logger = logging.getLogger(__name__)


def _filter_garment_for_type(garments, garment_type):
    filtered_garments = garments.filter(Garment.garment_type == garment_type)
    if filtered_garments.count() == 0:
        raise Exception(f"No garment of type {garment_type} found")
    return filtered_garments.offset(
        int(filtered_garments.count() * random.random())
    ).first()


def _generate_outfit(db: Session, place: str, activity: str, temperature: int):
    query = db.query(Garment).filter(
        Garment.washing == False,
        Garment.thrown_away == False,
        Garment.place == place,
        Garment.activity == activity,
    )
    types = ["socks", "underpants", "pants", "tshirt", "shoe"]
    garments = []
    for garment_type in types:
        garments.append(_filter_garment_for_type(query, garment_type))

    db_outfit = models.Outfit(garments=garments)
    db.add(db_outfit)
    db.commit()
    db.refresh(db_outfit)
    return db_outfit


def wear_outfit(db: Session, outfit: models.Outfit):
    [wear(db, garment) for garment in outfit.garments]
    db.refresh(outfit)
    return schemas.Outfit(id=outfit.id, garments=outfit.garments)


def get_outfit_for_place_and_activity(
    db: Session, place: str, activity, types: List[str]
):
    outfit = _generate_outfit(db, place, activity, types)
    return schemas.Outfit(id=outfit.id, garments=outfit.garments)


def get_outfit(db: Session, outfit_id: int):
    return db.query(models.Outfit).filter(models.Outfit.id == outfit_id).first()
