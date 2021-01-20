from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from typing import Optional, List
from sqlalchemy.orm import Session
from app.journaling.journaling import Journaling

router = APIRouter(prefix="/garments", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Garment])
def garments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    place: Optional[str] = None,
    garment_type: Optional[str] = None,
):
    return crud.get_garments(db, place, garment_type)


def _get_garment(db: Session, garment_id: int):
    db_garment = crud.get_garment(db, garment_id=garment_id)
    if db_garment is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Garment not found"
        )
    return db_garment


@router.get("/{garment_id}", response_model=schemas.Garment)
def get_garment(
    garment_id: int = Path(None, title="The ID of the garment to get", ge=1),
    db: Session = Depends(get_db),
):
    return _get_garment(db, garment_id)


@router.get("/{garment_id}/journal")
def get_journal(
    db: Session = Depends(get_db),
    garment_id: int = Path(
        None, title="The ID of the garment to get the journal from", ge=1
    ),
):
    garment = _get_garment(db, garment_id)
    return Journaling.get(garment.journaling_key)


@router.post(
    "/{garment_id}/journal",
    response_model=schemas.JournalEntry,
    status_code=HTTPStatus.CREATED,
)
def post_journal_entry(
    new_entry: schemas.JournalEntryCreate,
    db: Session = Depends(get_db),
    garment_id: int = Path(None, title="The ID for the garment", ge=1),
):
    garment = _get_garment(db, garment_id)
    return Journaling.create(garment.journaling_key, new_entry.message)


@router.post("", response_model=schemas.Garment, status_code=HTTPStatus.CREATED)
def create_garment(garment: schemas.GarmentCreate, db: Session = Depends(get_db)):
    return crud.create_garment(db, garment)


@router.put("/{garment_id}", response_model=schemas.Garment)
async def update_garment(
    garment_id: int = Path(None, title="The ID of the garment to update", ge=1),
    garment: Optional[schemas.Garment] = None,
):
    result = {"garment": garment}
    if garment:
        result.update({"updated_garment": garment})
    return schemas.Garment(name="test")


@router.delete("/{garment_id}")
async def delete_garment(
    garment_id: int = Path(None, title="The ID of the garment to remove", ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_garment(db, _get_garment(db, garment_id))
    return Response(status_code=HTTPStatus.NO_CONTENT)
