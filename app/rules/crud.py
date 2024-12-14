from sqlalchemy.orm import Session, joinedload
from app.activities.models import Rule, Activity
from app.garment_types.models import GarmentType


def get_rules(db: Session):
    return (
        db.query(Rule)
        .options(
            joinedload(Rule.garment_type),
            joinedload(Rule.activity),
        )
        .all()
    )


def create_rule(db: Session, rule):
    activity = db.query(Activity).filter(Activity.name == rule.activity).first()
    if not activity:
        raise ValueError(f"Activity {rule.activity} not found")
    garment_type = (
        db.query(GarmentType).filter(GarmentType.name == rule.garment_type).first()
    )
    if not garment_type:
        raise ValueError(f"Garment type {rule.garment_type} not found")
    db_rule = Rule(
        activity_id=activity.id,
        garment_type_id=garment_type.id,
        weather=rule.weather,
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule
