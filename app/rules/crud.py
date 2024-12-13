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


def create_activity_garment_type(db: Session, rule):
    db_rule = ActivityGarmentType(
        activity_id=rule.activity_id,
        garment_type_id=rule.garment_type_id,
        weather=rule.weather,
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule
