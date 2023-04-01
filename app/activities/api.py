from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/activities", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Activity])
def activities(db: Session = Depends(get_db)):
    activities = crud.get_activities(db)
    return activities


def _get_activity(db: Session, activity_id: int):
    db_activity = crud.get_activity(db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Activity not found"
        )
    return db_activity


@router.post("", response_model=schemas.Activity, status_code=HTTPStatus.CREATED)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(db, activity)


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int = Path(title="The ID of the activity to remove", ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_activity(db, _get_activity(db, activity_id))
    return Response(status_code=HTTPStatus.NO_CONTENT)
