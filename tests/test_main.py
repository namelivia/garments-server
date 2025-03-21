import pytest

from mock import patch, Mock
import uuid
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.garments.models import Garment
from app.outfits.models import Outfit
from app.places.models import Place
from app.activities.models import Activity
from app.weather.models import WeatherRange
from app.rules.models import Rule
from app.garment_types.models import GarmentType
from datetime import date
from freezegun import freeze_time

weather_api_response = {
    "latitude": 0.0,
    "longitude": 0.0,
    "generationtime_ms": 0.01704692840576172,
    "utc_offset_seconds": 7200,
    "timezone": "Europe/Berlin",
    "timezone_abbreviation": "CEST",
    "elevation": 0.0,
    "daily_units": {
        "time": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C",
    },
    "daily": {
        "time": ["2024-06-08"],
        "temperature_2m_max": [25.2],
        "temperature_2m_min": [24.7],
    },
}


@freeze_time("2013-04-09")
class TestApp:
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

    def _insert_test_outfit(self, session, outfit: dict = {}):
        key = uuid.uuid4()
        data = {
            "activity": "everyday",
            "weather": "hot",
        }
        data.update(outfit)
        db_outfit = Outfit(**data)
        session.add(db_outfit)
        session.commit()
        return db_outfit

    def _insert_test_weather_range(self, session, weather_range: dict = {}):
        data = {
            "name": "hot",
            "max": 30,
        }
        data.update(weather_range)
        db_range = WeatherRange(**data)
        session.add(db_range)
        session.commit()
        return db_range

    def _insert_test_place(self, session, place: dict = {}):
        data = {
            "name": "Test place",
            "latitude": "0.00001",
            "longitude": "0.0001",
        }
        data.update(place)
        db_place = Place(**data)
        session.add(db_place)
        session.commit()
        return db_place

    def _insert_test_activity(self, session, activity: dict = {}):
        data = {
            "name": "Test activity",
        }
        data.update(activity)
        db_activity = Activity(**data)
        session.add(db_activity)
        session.commit()
        return db_activity

    def _insert_test_rule(self, session, rule: dict = {}):
        data = {
            "activity_id": 1,
            "garment_type_id": 1,
            "weather": "hot",
        }
        data.update(rule)
        db_rule = Rule(**data)
        session.add(db_rule)
        session.commit()
        return db_rule

    def _insert_test_garment_type(self, session, garment_type: dict = {}):
        data = {
            "name": "Test garment type",
        }
        data.update(garment_type)
        db_garment_type = GarmentType(**data)
        session.add(db_garment_type)
        session.commit()
        return db_garment_type

    @patch("uuid.uuid4")
    def test_create_garment(self, m_uuid, client, database_test_session):
        key = "271c973a-638f-4e01-9a79-308c880e3d11"
        m_uuid.return_value = key
        activity = self._insert_test_activity(
            database_test_session, {"name": "everyday"}
        )
        response = client.post(
            "/garments",
            json={
                "name": "Some test garment",
                "garment_type": "shirt",
                "color": "white",
                "place": "home",
                "activity": "everyday",
                "status": "ok",
                "wear_to_wash": 2,
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Some test garment",
            "garment_type": "shirt",
            "image": None,
            "color": "white",
            "place": "home",
            "activity": "None",
            "status": "ok",
            "journaling_key": key,
            "wear_to_wash": 2,
            "worn": 0,
            "total_worn": 0,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": False,
            "activities": [
                {
                    "id": 1,
                    "name": "everyday",
                }
            ],
        }

    def test_get_non_existing_garment(self, client):
        response = client.get("/garments/99")
        assert response.status_code == 404

    @patch("app.users.api.UserInfo.get_current")
    def test_get_current_user(self, m_get_user_info, client):
        m_get_user_info.return_value = {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
        }
        response = client.get(
            "/users/me", headers={"X-Pomerium-Jwt-Assertion": "jwt_assertion"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
            "place": None,
        }
        m_get_user_info.assert_called_with("jwt_assertion")

    def test_get_existing_garment(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        response = client.get("/garments/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test garment",
            "garment_type": "Shoe",
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "image": None,
            "journaling_key": str(key),
            "wear_to_wash": 1,
            "worn": 0,
            "total_worn": 0,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": False,
            "activities": [],
        }

    def test_create_garment_invalid(self, client):
        response = client.post("/garments", json={"payload": "Invalid"})
        assert response.status_code == 422

    def test_get_all_garments(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        # This won't be included in the response
        self._insert_test_garment(
            database_test_session, {"journaling_key": key, "thrown_away": True}
        )
        response = client.get("/garments")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "home",
                "activity": "everyday",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
                "wear_to_wash": 1,
                "worn": 0,
                "total_worn": 0,
                "times_rejected": 0,
                "washing": False,
                "thrown_away": False,
                "activities": [],
            },
            {
                "id": 2,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "home",
                "activity": "everyday",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
                "wear_to_wash": 1,
                "worn": 0,
                "total_worn": 0,
                "times_rejected": 0,
                "washing": False,
                "thrown_away": False,
                "activities": [],
            },
        ]

    def test_get_washing_garments(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        self._insert_test_garment(
            database_test_session, {"journaling_key": key, "washing": True}
        )
        response = client.get("/garments/washing")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 2,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "home",
                "activity": "everyday",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
                "wear_to_wash": 1,
                "worn": 0,
                "total_worn": 0,
                "times_rejected": 0,
                "washing": True,
                "thrown_away": False,
                "activities": [],
            },
        ]

    def test_get_thrown_away_garments(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        self._insert_test_garment(
            database_test_session, {"journaling_key": key, "thrown_away": True}
        )
        response = client.get("/garments/thrown_away")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 2,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "home",
                "activity": "everyday",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
                "wear_to_wash": 1,
                "worn": 0,
                "total_worn": 0,
                "times_rejected": 0,
                "washing": False,
                "thrown_away": True,
                "activities": [],
            },
        ]

    def test_delete_non_existing_garment(self, client):
        response = client.get("/garments/99")
        assert response.status_code == 404

    def test_delete_garment(self, client, database_test_session):
        self._insert_test_garment(database_test_session)
        response = client.get("/garments/1")
        assert response.status_code == 200

    def test_post_image(self, client):
        response = client.post("/image")
        assert response.status_code == 422

    @patch("requests.get")
    def test_get_image(self, m_get, client):
        m_get.return_value = Mock()
        m_get.return_value.content = "image_binary_data"
        response = client.get("/image/image_path/extra")
        # TODO: Change this assertion once the image service is done
        # m_get.assert_called_with("http://images-service:80/image/image_path")
        assert response.status_code == 200
        assert response.content == b"image_binary_data"

    def test_create_place(self, client):
        response = client.post(
            "/places",
            json={
                "name": "Some test place",
                "latitude": "1.0",
                "longitude": "1.0",
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Some test place",
            "latitude": "1.0",
            "longitude": "1.0",
        }

    def test_get_all_places(self, client, database_test_session):
        self._insert_test_place(database_test_session, {"name": "test place 1"})
        # These two will be filtered out
        self._insert_test_place(database_test_session, {"name": "test place 2"})
        self._insert_test_place(database_test_session, {"name": "test place 3"})
        self._insert_test_garment(database_test_session, {"place": "test place 1"})
        self._insert_test_garment(
            database_test_session, {"place": "test place 2", "thrown_away": True}
        )
        response = client.get("/places")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "test place 1",
                "latitude": "0.00001",
                "longitude": "0.0001",
            }
        ]

    def test_get_all_activities(self, client, database_test_session):
        self._insert_test_activity(database_test_session, {"name": "test activity 1"})
        self._insert_test_activity(database_test_session, {"name": "test activity 2"})
        response = client.get("/activities")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "test activity 1",
            },
            {
                "id": 2,
                "name": "test activity 2",
            },
        ]

    def test_get_all_garment_types(self, client, database_test_session):
        self._insert_test_garment_type(
            database_test_session, {"name": "test garment type 1"}
        )
        self._insert_test_garment_type(
            database_test_session, {"name": "test garment type 2"}
        )
        response = client.get("/garment_types")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "test garment type 1",
            },
            {
                "id": 2,
                "name": "test garment type 2",
            },
        ]

    def test_delete_place(self, client, database_test_session):
        self._insert_test_place(database_test_session)
        response = client.delete("/places/1")
        assert response.status_code == 204

    def test_delete_activity(self, client, database_test_session):
        self._insert_test_activity(database_test_session)
        response = client.delete("/activities/1")
        assert response.status_code == 204

    def test_get_garments_by_place(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session, {"place": "place1", "journaling_key": key}
        )
        self._insert_test_garment(
            database_test_session, {"place": "place2", "journaling_key": key}
        )
        response = client.get("/garments?place=place1")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "place1",
                "activity": "everyday",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
                "wear_to_wash": 1,
                "worn": 0,
                "total_worn": 0,
                "times_rejected": 0,
                "washing": False,
                "thrown_away": False,
                "activities": [],
            }
        ]

    def test_get_garments_by_place_type_and_activity(
        self, client, database_test_session
    ):
        key = uuid.uuid4()
        running_activity = self._insert_test_activity(
            database_test_session, {"name": "running"}
        )
        everyday_activity = self._insert_test_activity(
            database_test_session, {"name": "everyday"}
        )
        socks = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "socks",
            },
        )
        underpants = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "underpants",
            },
        )
        pants = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "pants",
            },
        )
        tshirt = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "tshirt",
            },
        )
        shoe = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "shoe",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": socks.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": underpants.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": pants.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": tshirt.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": shoe.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": running_activity.id,
                "garment_type_id": socks.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": running_activity.id,
                "garment_type_id": shoe.id,
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "activity": "everyday",
                "garment_type": "garment_type_1",
                "journaling_key": key,
                "activities": [everyday_activity],
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "cold",
                "max": 5,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "mild",
                "max": 16,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "hot",
                "max": 100,
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "activity": "running",
                "garment_type": "garment_type_1",
                "journaling_key": key,
                "activities": [running_activity],
            },
        )
        response = client.get(
            "/garments?place=place1&garment_type=garment_type_1&activity=running"
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 2,
                "name": "Test garment",
                "garment_type": "garment_type_1",
                "color": "red",
                "place": "place1",
                "activity": "running",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
                "wear_to_wash": 1,
                "worn": 0,
                "total_worn": 0,
                "times_rejected": 0,
                "washing": False,
                "thrown_away": False,
                "activities": [{"id": 1, "name": "running"}],
            }
        ]

    def test_updating_garment(self, client, database_test_session):
        key = uuid.uuid4()
        original_garment = self._insert_test_garment(
            database_test_session, {"name": "Some name", "journaling_key": key}
        )
        response = client.put(
            "/garments/1",
            json={
                "name": "Updated name",
                "garment_type": original_garment.garment_type,
                "color": original_garment.color,
                "place": original_garment.place,
                "activity": original_garment.activity,
                "status": "ok",
                "journaling_key": str(key),
                "wear_to_wash": 4,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Updated name",
            "garment_type": "Shoe",
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "image": None,
            "journaling_key": str(key),
            "wear_to_wash": 4,
            "worn": 0,
            "total_worn": 0,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": False,
            "activities": [],
        }

    def test_get_random_garment(self, client, database_test_session):
        key = uuid.uuid4()
        running_activity = self._insert_test_activity(
            database_test_session, {"name": "running"}
        )
        everyday_activity = self._insert_test_activity(
            database_test_session, {"name": "everyday"}
        )
        test_garment = self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "garment_type": "garment_type_1",
                "activity": "running",
                "journaling_key": key,
                "activities": [running_activity],
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "activity": "running",
                "garment_type": "garment_type_1",
                "journaling_key": key,
                "activities": [running_activity],
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "activity": "everyday",
                "garment_type": "garment_type_1",
                "journaling_key": key,
                "activities": [everyday_activity],
            },
        )
        # Washing garments will be excluded
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "garment_type": "garment_type_1",
                "journaling_key": key,
                "washing": True,
                "thrown_away": False,
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "garment_type": "garment_type_2",
                "journaling_key": key,
            },
        )
        self._insert_test_garment(
            database_test_session, {"place": "place2", "journaling_key": key}
        )
        response = client.get(
            "/garments/random?place=place1&garment_type=garment_type_1&activity=running"
        )
        assert response.status_code == 200
        assert response.json()["id"] in (1, 2)

    def test_wear_garment(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session, {"journaling_key": key, "wear_to_wash": 3}
        )
        response = client.post("/garments/1/wear")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test garment",
            "garment_type": "Shoe",
            "image": None,
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "journaling_key": str(key),
            "wear_to_wash": 3,
            "worn": 1,
            "total_worn": 1,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": False,
        }

    @patch("app.notifications.notifications.Notifications.send")
    def test_wear_garment_sets_washing(
        self, m_send_notification, client, database_test_session
    ):
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session,
            {"total_worn": 2, "worn": 2, "journaling_key": key, "wear_to_wash": 3},
        )
        response = client.post("/garments/1/wear")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test garment",
            "garment_type": "Shoe",
            "image": None,
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "journaling_key": str(key),
            "wear_to_wash": 3,
            "worn": 3,
            "total_worn": 3,
            "times_rejected": 0,
            "washing": True,
            "thrown_away": False,
        }
        m_send_notification.assert_any_call(
            "Garment Test garment has been worn 3 times and needs to be washed",
        )

    def test_sending_garment_to_wash_garment(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session,
            {
                "worn": 2,
                "total_worn": 2,
                "journaling_key": key,
                "worn": 0,
                "wear_to_wash": 9,
                "washing": False,
                "thrown_away": False,
            },
        )
        response = client.post("/garments/1/send_to_wash")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test garment",
            "garment_type": "Shoe",
            "image": None,
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "journaling_key": str(key),
            "wear_to_wash": 9,
            "times_rejected": 0,
            "worn": 0,
            "total_worn": 2,
            "washing": True,
            "thrown_away": False,
        }

    def test_wash_garment(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session,
            {
                "worn": 2,
                "total_worn": 2,
                "journaling_key": key,
                "washing": True,
                "thrown_away": False,
            },
        )
        response = client.post("/garments/1/wash")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test garment",
            "garment_type": "Shoe",
            "image": None,
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "journaling_key": str(key),
            "wear_to_wash": 1,
            "worn": 0,
            "total_worn": 2,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": False,
        }

    def test_throw_away_garment(self, client, database_test_session):
        key = uuid.uuid4()
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session,
            {
                "journaling_key": key,
                "washing": True,
                "thrown_away": False,
            },
        )
        response = client.post("/garments/1/throw_away")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test garment",
            "garment_type": "Shoe",
            "image": None,
            "color": "red",
            "place": "home",
            "activity": "everyday",
            "status": "ok",
            "journaling_key": str(key),
            "wear_to_wash": 1,
            "worn": 0,
            "total_worn": 0,
            "times_rejected": 0,
            "washing": False,
            "thrown_away": True,
        }

    @patch("requests.get")
    def test_get_outfit_by_place_type_and_activity(
        self, m_get, client, database_test_session
    ):
        key = uuid.uuid4()
        m_get.return_value = Mock()
        m_get.return_value.json.return_value = weather_api_response
        home = self._insert_test_place(
            database_test_session,
            {"name": "home", "latitude": "0.00001", "longitude": "0.0001"},
        )
        everyday_activity = self._insert_test_activity(
            database_test_session,
            {"name": "everyday"},
        )
        running_activity = self._insert_test_activity(
            database_test_session,
            {
                "name": "running",
            },
        )
        socks = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "socks",
            },
        )
        underpants = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "underpants",
            },
        )
        pants = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "pants",
            },
        )
        tshirt = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "tshirt",
            },
        )
        shoe = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "shoe",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": socks.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": underpants.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": pants.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": tshirt.id,
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": shoe.id,
            },
        )
        # This will be excluded because it is for cold weather
        # and the fixture temperature is "hot"
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": running_activity.id,
                "garment_type_id": socks.id,
                "weather": "cold",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": running_activity.id,
                "garment_type_id": shoe.id,
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "garment_type": "socks",
                "journaling_key": key,
                "activities": [everyday_activity, running_activity],
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "garment_type": "underpants",
                "journaling_key": key,
                "activities": [everyday_activity],
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "garment_type": "pants",
                "journaling_key": key,
                "activities": [everyday_activity],
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "garment_type": "tshirt",
                "journaling_key": key,
                "activities": [everyday_activity],
            },
        )
        self._insert_test_garment(
            database_test_session,
            {
                "garment_type": "shoe",
                "journaling_key": key,
                "activities": [everyday_activity, running_activity],
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "cold",
                "max": 5,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "mild",
                "max": 16,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "hot",
                "max": 100,
            },
        )
        response = client.get("/outfits/new?place=home&activity=running")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "worn_on": None,
            "activity": "running",
            "weather": "hot",
            "garments": [
                {
                    "id": 5,
                    "name": "Test garment",
                    "garment_type": "shoe",
                    "image": None,
                    "color": "red",
                    "place": "home",
                    "activity": "everyday",
                    "status": "ok",
                    "journaling_key": str(key),
                    "wear_to_wash": 1,
                    "worn": 0,
                    "total_worn": 0,
                    "times_rejected": 0,
                    "washing": False,
                    "thrown_away": False,
                    "activities": [
                        {"id": 1, "name": "everyday"},
                        {"id": 2, "name": "running"},
                    ],
                },
            ],
        }

    @patch("requests.get")
    def test_when_there_are_no_available_garments_for_outfit_404_is_returned(
        self, m_get, client, database_test_session
    ):
        key = uuid.uuid4()
        m_get.return_value = Mock()
        m_get.return_value.json.return_value = weather_api_response
        home = self._insert_test_place(
            database_test_session,
            {"name": "home", "latitude": "0.00001", "longitude": "0.0001"},
        )
        self._insert_test_garment(
            database_test_session,
            {
                "garment_type": "shoe",
                "journaling_key": key,
            },
        )
        everyday = self._insert_test_activity(
            database_test_session,
            {
                "name": "everyday",
            },
        )
        socks = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "socks",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday.id,
                "garment_type_id": socks.id,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "cold",
                "max": 5,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "mild",
                "max": 16,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "hot",
                "max": 100,
            },
        )

        response = client.get("/outfits/new?place=home&activity=everyday")
        assert response.status_code == 404
        assert response.json() == {"detail": "No garment of type socks found"}

    def test_wear_outfit(self, client, database_test_session):
        key = uuid.uuid4()
        garments = [self._insert_test_garment(database_test_session)]
        outfit = self._insert_test_outfit(database_test_session, {"garments": garments})
        response = client.post("/outfits/1/wear")
        assert response.status_code == 200
        assert response.json()["garments"][0]["worn"] == 1
        assert response.json()["worn_on"] == "2013-04-09T00:00:00"

    def test_getting_todays_outfits(self, client, database_test_session):
        key = uuid.uuid4()
        garments = [self._insert_test_garment(database_test_session)]
        today = date.today()
        outfit = self._insert_test_outfit(
            database_test_session, {"garments": [], "worn_on": today}
        )
        another_outfit = self._insert_test_outfit(
            database_test_session, {"garments": [], "worn_on": today}
        )
        response = client.get("/outfits/today")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "worn_on": "2013-04-09T00:00:00",
                "garments": [],
                "activity": "everyday",
                "weather": "hot",
            },
            {
                "id": 2,
                "worn_on": "2013-04-09T00:00:00",
                "garments": [],
                "activity": "everyday",
                "weather": "hot",
            },
        ]

    def test_rejecting_garment_from_outfit(self, client, database_test_session):
        key = uuid.uuid4()
        everyday_activity = self._insert_test_activity(
            database_test_session,
            {
                "name": "everyday",
            },
        )
        shoe = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "Shoe",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": shoe.id,
            },
        )

        garments = [
            self._insert_test_garment(
                database_test_session,
                {
                    "journaling_key": key,
                    "activities": [everyday_activity],
                },
            ),
            self._insert_test_garment(
                database_test_session,
                {
                    "journaling_key": key,
                    "name": "Another garment",
                    "activities": [everyday_activity],
                },
            ),
        ]
        outfit = self._insert_test_outfit(
            database_test_session, {"garments": garments, "activity": "everyday"}
        )
        response = client.post("/outfits/1/reject/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "worn_on": None,
            "garments": [
                {
                    "id": 2,
                    "name": "Another garment",
                    "garment_type": "Shoe",
                    "color": "red",
                    "place": "home",
                    "activity": "everyday",
                    "status": "ok",
                    "image": None,
                    "journaling_key": str(key),
                    "wear_to_wash": 1,
                    "worn": 0,
                    "total_worn": 0,
                    "times_rejected": 0,
                    "washing": False,
                    "thrown_away": False,
                    "activities": [
                        {"id": 1, "name": "everyday"},
                    ],
                }
            ],
            "activity": "everyday",
            "weather": "hot",
        }

    @patch("requests.get")
    def test_get_weather(self, m_get, client, database_test_session):
        self._insert_test_place(database_test_session, {"name": "home"})
        m_get.return_value = Mock()
        m_get.return_value.json.return_value = weather_api_response
        response = client.get("/weather?place=home")
        assert response.json() == {
            "weather": {
                "min": 24.7,
                "avg": 24.95,
                "max": 25.2,
            }
        }

    def test_get_rules(self, client, database_test_session):
        everyday_activity = self._insert_test_activity(
            database_test_session, {"name": "everyday"}
        )
        socks = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "socks",
            },
        )
        pants = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "pants",
            },
        )
        tshirt = self._insert_test_garment_type(
            database_test_session,
            {
                "name": "tshirt",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": socks.id,
                "weather": "hot",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": pants.id,
                "weather": "hot",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": tshirt.id,
                "weather": "cold",
            },
        )
        self._insert_test_rule(
            database_test_session,
            {
                "activity_id": everyday_activity.id,
                "garment_type_id": pants.id,
                "weather": "cold",
            },
        )
        response = client.get("/rules")
        assert response.status_code == 200
        assert response.json() == [
            {
                "activity_id": 1,
                "activity": {
                    "id": 1,
                    "name": "everyday",
                },
                "garment_type_id": 1,
                "garment_type": {
                    "id": 1,
                    "name": "socks",
                },
                "weather": "hot",
            },
            {
                "activity_id": 1,
                "activity": {
                    "id": 1,
                    "name": "everyday",
                },
                "garment_type_id": 2,
                "garment_type": {
                    "id": 2,
                    "name": "pants",
                },
                "weather": "hot",
            },
            {
                "activity_id": 1,
                "activity": {
                    "id": 1,
                    "name": "everyday",
                },
                "garment_type_id": 3,
                "garment_type": {
                    "id": 3,
                    "name": "tshirt",
                },
                "weather": "cold",
            },
            {
                "activity_id": 1,
                "activity": {
                    "id": 1,
                    "name": "everyday",
                },
                "garment_type_id": 2,
                "garment_type": {
                    "id": 2,
                    "name": "pants",
                },
                "weather": "cold",
            },
        ]

    def test_create_rule(self, client, database_test_session):
        garment_type = self._insert_test_garment_type(
            database_test_session, {"name": "test garment type 1"}
        )
        activity = self._insert_test_activity(
            database_test_session, {"name": "test activity 1"}
        )
        response = client.post(
            "/rules",
            json={
                "activity": activity.name,
                "garment_type": garment_type.name,
                "weather": "hot",
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "activity_id": activity.id,
            "garment_type_id": garment_type.id,
            "weather": "hot",
        }

    def test_get_weather_configuration(self, client, database_test_session):
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "mild",
                "max": 16,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "cold",
                "max": 5,
            },
        )
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "hot",
                "max": 100,
            },
        )
        response = client.get("/weather/configuration")
        assert response.status_code == 200
        assert [
            {
                "name": "cold",
                "max": 5,
            },
            {
                "name": "mild",
                "max": 16,
            },
            {
                "name": "hot",
                "max": 100,
            },
        ]
