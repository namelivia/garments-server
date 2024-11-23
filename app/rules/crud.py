from sqlalchemy.orm import Session
from app.activities.models import ActivityGarmentType


def get_activity_garment_types(db: Session):
    return db.query(ActivityGarmentType).all()
