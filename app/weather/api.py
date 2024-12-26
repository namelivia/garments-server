from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session
from . import crud, schemas

router = APIRouter(prefix="/weather", dependencies=[Depends(get_db)])


@router.get("", response_model=schemas.Weather)
def get_weather(
    db: Session = Depends(get_db),
    place: str = None,
):
    return schemas.Weather(weather=crud.get_weather_for_place(db, place))


@router.get("/configuration")
def get_configuration(db: Session = Depends(get_db)):
    return crud.get_weather_configuration(db)
