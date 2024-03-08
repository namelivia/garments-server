from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from sqlalchemy.orm import Session
from app.journaling.journaling import Journaling

router = APIRouter(prefix="/outfit", dependencies=[Depends(get_db)])


@router.get("", response_model=schemas.Outfit)
def outfit(place: str, activity: str, temperature: int, db: Session = Depends(get_db)):
    try:
        return crud.get_outfit_for_place_and_activity(db, place, activity, temperature)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
