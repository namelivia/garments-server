from fastapi import APIRouter, Depends
from http import HTTPStatus
from app.dependencies import get_db
from sqlalchemy.orm import Session
from . import crud, schemas

router = APIRouter(prefix="/rules", dependencies=[Depends(get_db)])


# @router.get("", response_model=List[schemas.ActivityGarmentType])
@router.get("")
def get_rules(db: Session = Depends(get_db)):
    return crud.get_activity_garment_types(db)


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
)
def create_rule(rule: schemas.ActivityGarmentTypeCreate, db: Session = Depends(get_db)):
    return crud.create_activity_garment_type(db, rule)
