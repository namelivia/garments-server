from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/garment_types", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.GarmentType])
def garment_types(db: Session = Depends(get_db)):
    garment_types = crud.get_garment_types(db)
    return garment_types


def _get_garment_type(db: Session, garment_type_id: int):
    db_garment_type = crud.get_garment_type(db, garment_type_id=garment_type_id)
    if db_garment_type is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Garment type not found"
        )
    return db_garment_type


@router.post("", response_model=schemas.GarmentType, status_code=HTTPStatus.CREATED)
def create_garment_type(
    garment_type: schemas.GarmentTypeCreate, db: Session = Depends(get_db)
):
    return crud.create_garment_type(db, garment_type)


@router.delete("/{garment_type_id}")
async def delete_garment_type(
    garment_type_id: int = Path(title="The ID of the garment_type to remove", ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_garment_type(db, _get_garment_type(db, garment_type_id))
    return Response(status_code=HTTPStatus.NO_CONTENT)
