from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from sqlalchemy.orm import Session
from app.journaling.journaling import Journaling
from app.exceptions.exceptions import NotFoundException
from datetime import date
from typing import List

router = APIRouter(prefix="/outfits", dependencies=[Depends(get_db)])


@router.get("/new", response_model=schemas.Outfit)
def new_outfit(place: str, activity: str, db: Session = Depends(get_db)):
    try:
        return crud.get_outfit_for_place_and_activity(db, place, activity)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


def _get_outfit(db: Session, outfit_id: int):
    db_outfit = crud.get_outfit(db, outfit_id=outfit_id)
    if db_outfit is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Outfit not found")
    return db_outfit


@router.post("/{outfit_id}/wear", response_model=schemas.Outfit)
async def wear_outfit(
    outfit_id: int = Path(title="The ID of the outfit to wear", ge=1),
    db: Session = Depends(get_db),
):
    return crud.wear_outfit(db, _get_outfit(db, outfit_id))


@router.get("/today", response_model=List[schemas.Outfit])
async def get_todays_outfits(
    db: Session = Depends(get_db),
):
    return crud.get_outfits_for_date(db, date.today())


@router.post("/{outfit_id}/reject/{garment_id}", response_model=schemas.Outfit)
async def reject_outfit_garment(
    outfit_id: int = Path(title="The ID of the outfit", ge=1),
    garment_id: int = Path(title="The ID of the garment to reject", ge=1),
    db: Session = Depends(get_db),
):
    return crud.reject_outfit_garment(db, _get_outfit(db, outfit_id), garment_id)
