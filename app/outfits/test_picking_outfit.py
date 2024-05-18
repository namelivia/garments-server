from app.outfits.crud import get_outfit_for_place_and_activity
from tests.test_base import database_test_session
import uuid
from app.garments.models import Garment
from app.activities.models import Activity
from app.garment_types.models import GarmentType


class TestPickingOutfit:
    def _insert_test_activity(self, session, activity: dict = {}):
        data = {
            "name": "Test activity",
        }
        data.update(activity)
        db_activity = Activity(**data)
        garment_types = activity["garment_types"] if "garment_types" in activity else []
        for garment_type in garment_types:
            db_activity.garment_types.append(garment_type)
        session.add(db_activity)
        session.commit()
        return db_activity

    def _insert_test_garment(self, session, garment: dict = {}):
        key = uuid.uuid4()
        data = {
            "name": "Test garment",
            "garment_type": "Shoe",
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "journaling_key": key,
            "wear_to_wash": 1,
            "worn": 0,
            "total_worn": 0,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": False,
        }
        data.update(garment)
        db_garment = Garment(**data)
        activities = garment["activities"] if "activities" in garment else []
        for activity in activities:
            db_garment.activities.append(activity)
        session.add(db_garment)
        session.commit()
        return db_garment

    def _insert_test_garment_type(self, session, garment_type: dict = {}):
        data = {
            "name": "Test garment type",
        }
        data.update(garment_type)
        db_garment_type = GarmentType(**data)
        session.add(db_garment_type)
        session.commit()
        return db_garment_type

    def test_getting_an_outfit(self, database_test_session):
        key = uuid.uuid4()

        # Define a running activity, it requires a tshirt
        running_activity = self._insert_test_activity(
            database_test_session,
            {
                "name": "Running",
                "garment_types": [
                    self._insert_test_garment_type(
                        database_test_session, {"name": "Tshirt"}
                    ),
                ],
            },
        )

        # Insert a running tshirt
        self._insert_test_garment(
            database_test_session,
            {
                "journaling_key": key,
                "name": "Running tshirt",
                "place": "New York",
                "activities": [running_activity],
                "garment_type": "Tshirt",
            },
        )

        # Get an outfit for running in New York
        outfit = get_outfit_for_place_and_activity(
            database_test_session, "New York", "Running"
        )

        # Assert that the outfit is the running tshirt
        assert len(outfit.garments) == 1
        assert outfit.garments[0].name == "Running tshirt"
