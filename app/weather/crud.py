from sqlalchemy.orm import Session
from app.places.models import Place
from app.exceptions.exceptions import NotFoundException
from .weather import get_complete_weather
from . import models


def get_weather_for_place(db: Session, place: str):
    db_place = db.query(Place).filter(Place.name == place).first()
    if not db_place:
        raise NotFoundException(f"Place {place} not found")
    return get_complete_weather(db_place)


def get_weather_configuration(db: Session):
    return db.query(models.WeatherRange).all()
