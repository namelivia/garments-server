from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from sqlalchemy.orm import Session
from app.journaling.journaling import Journaling

router = APIRouter(prefix="/outfits", dependencies=[Depends(get_db)])


@router.get("", response_model=schemas.Outfit)
def outfit(place: str, activity: str, temperature: int, db: Session = Depends(get_db)):
    try:
        return crud.get_outfit_for_place_and_activity(db, place, activity, temperature)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


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
    from pudb.remote import set_trace

    return crud.wear_outfit(db, _get_outfit(db, outfit_id))
