from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/places", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Place])
def places(db: Session = Depends(get_db)):
    places = crud.get_places(db)
    return places


def _get_place(db: Session, place_id: int):
    db_place = crud.get_place(db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Place not found")
    return db_place


@router.post("", response_model=schemas.Place, status_code=HTTPStatus.CREATED)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    return crud.create_place(db, place)


@router.delete("/{place_id}")
async def delete_place(
    place_id: int = Path(None, title="The ID of the place to remove", ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_place(db, _get_place(db, place_id))
    return Response(status_code=HTTPStatus.NO_CONTENT)
