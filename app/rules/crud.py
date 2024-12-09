from sqlalchemy.orm import Session, joinedload
from app.activities.models import ActivityGarmentType


def get_activity_garment_types(db: Session):
    return (
        db.query(ActivityGarmentType)
        .options(
            joinedload(ActivityGarmentType.garment_type),
            joinedload(ActivityGarmentType.activity),
        )
        .all()
    )
