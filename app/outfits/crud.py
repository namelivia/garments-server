# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
from . import schemas
from app.garments.models import Garment
import random

logger = logging.getLogger(__name__)


def _filter_garment_for_type(garments, garment_type):
    # garment = garments.filter(Garment.garment_type == garment_type).offset(int(garments.count() * random.random())).first()
    filtered_garments = garments.filter(Garment.garment_type == garment_type)
    if filtered_garments.count() == 0:
        raise Exception(f"No garment of type {garment_type} found")
    return filtered_garments.offset(
        int(filtered_garments.count() * random.random())
    ).first()


def get_outfit_for_place_and_activity(db: Session, place: str, activity):
    query = db.query(Garment).filter(
        Garment.washing == False,
        Garment.thrown_away == False,
        Garment.place == place,
        Garment.activity == activity,
    )
    socks = _filter_garment_for_type(query, "socks").name
    underpants = _filter_garment_for_type(query, "underpants").name
    pants = _filter_garment_for_type(query, "pants").name
    tshirt = _filter_garment_for_type(query, "tshirt").name
    shoe = _filter_garment_for_type(query, "shoe").name
    return schemas.Outfit(
        socks=socks, underpants=underpants, pants=pants, tshirt=tshirt, shoe=shoe
    )
