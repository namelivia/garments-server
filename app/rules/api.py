from fastapi import APIRouter, Depends
from http import HTTPStatus
from app.dependencies import get_db
from sqlalchemy.orm import Session
from . import crud, schemas

router = APIRouter(prefix="/rules", dependencies=[Depends(get_db)])


# @router.get("", response_model=List[schemas.Rule])
@router.get("")
def get_rules(db: Session = Depends(get_db)):
    return crud.get_rules(db)


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
)
def create_rule(rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db, rule)
