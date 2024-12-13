from sqlalchemy.orm import Session, joinedload
from app.activities.models import ActivityGarmentType, Activity
from app.garment_types.models import GarmentType


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
    activity = db.query(Activity).filter(Activity.name == rule.activity).first()
    if not activity:
        raise ValueError(f"Activity {rule.activity} not found")
    garment_type = (
        db.query(GarmentType).filter(GarmentType.name == rule.garment_type).first()
    )
    if not garment_type:
        raise ValueError(f"Garment type {rule.garment_type} not found")
    db_rule = ActivityGarmentType(
        activity_id=activity.id,
        garment_type_id=garment_type.id,
        weather=rule.weather,
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule
