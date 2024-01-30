# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
from . import schemas
from app.garments.models import Garment
import random
from typing import List

logger = logging.getLogger(__name__)


def _filter_garment_for_type(garments, garment_type):
    # garment = garments.filter(Garment.garment_type == garment_type).offset(int(garments.count() * random.random())).first()
    filtered_garments = garments.filter(Garment.garment_type == garment_type)
    if filtered_garments.count() == 0:
        raise Exception(f"No garment of type {garment_type} found")
    return filtered_garments.offset(
        int(filtered_garments.count() * random.random())
    ).first()


def _generate_outfit(db: Session, place: str, activity: str, types: List[str]):
    query = db.query(Garment).filter(
        Garment.washing == False,
        Garment.thrown_away == False,
        Garment.place == place,
        Garment.activity == activity,
    )
    outfit = {}
    for garment_type in types:
        outfit[garment_type] = _filter_garment_for_type(query, garment_type).name
    return outfit


def get_outfit_for_place_and_activity(
    db: Session, place: str, activity, types: List[str]
):
    outfit = _generate_outfit(db, place, activity, types)
    return schemas.Outfit(garments=outfit)
