import pytest
from mock import patch, Mock
import uuid
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.garments.models import Garment
from app.places.models import Place
from app.garment_types.models import GarmentType
from freezegun import freeze_time


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_garment(self, session, garment: dict = {}):
        key = uuid.uuid4()
        data = {
            "name": "Test garment",
            "garment_type": "Shoe",
            "color": "red",
            "place": "home",
            "status": "ok",
            "journaling_key": key,
        }
        data.update(garment)
        db_garment = Garment(**data)
        session.add(db_garment)
        session.commit()
        return db_garment

    def _insert_test_place(self, session, place: dict = {}):
        data = {
            "name": "Test place",
        }
        data.update(place)
        db_place = Place(**data)
        session.add(db_place)
        session.commit()
        return db_place

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
    @patch("app.notifications.notifications.Notifications.send")
    def test_create_garment(self, m_send_notification, m_uuid, client):
        key = "271c973a-638f-4e01-9a79-308c880e3d11"
        m_uuid.return_value = key
        response = client.post(
            "/garments",
            json={
                "name": "Some test garment",
                "garment_type": "shirt",
                "color": "white",
                "place": "home",
                "status": "ok",
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
            "status": "ok",
            "journaling_key": key,
        }
        m_send_notification.assert_called_with(
            "A new garment called Some test garment has been created"
        )

    def test_get_non_existing_garment(self, client):
        response = client.get("/garments/99")
        assert response.status_code == 404

    @patch("app.users.jwt.JWT.get_current_user_info")
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
        response = client.get("/users/me")
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
            "status": "ok",
            "image": None,
            "journaling_key": str(key),
        }

    def test_create_garment_invalid(self, client):
        response = client.post("/garments", json={"payload": "Invalid"})
        assert response.status_code == 422

    def test_get_all_garments(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        self._insert_test_garment(database_test_session, {"journaling_key": key})
        response = client.get("/garments")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "home",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
            },
            {
                "id": 2,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
                "place": "home",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
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
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Some test place",
        }

    def test_get_all_places(self, client, database_test_session):
        self._insert_test_place(database_test_session, {"name": "test place 1"})
        self._insert_test_place(database_test_session, {"name": "test place 2"})
        response = client.get("/places")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "test place 1",
            },
            {
                "id": 2,
                "name": "test place 2",
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
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
            }
        ]

    def test_get_garments_by_place_and_type(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_garment(
            database_test_session,
            {
                "place": "place1",
                "garment_type": "garment_type_1",
                "journaling_key": key,
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
        response = client.get("/garments?place=place1&garment_type=garment_type_1")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test garment",
                "garment_type": "garment_type_1",
                "color": "red",
                "place": "place1",
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
            }
        ]
