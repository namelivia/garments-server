import pytest
from mock import patch, Mock
import uuid
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.garments.models import Garment
from app.garments.schemas import Garment as GarmentSchema
import datetime
from freezegun import freeze_time


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_garment(self, session, garment: dict = {}):
        key = uuid.uuid4()
        data = {
            "name": "Test garment",
            "garment_type": "Shoe",
            "color": "red",
            "status": "ok",
            "journaling_key": key,
        }
        data.update(garment)
        db_garment = Garment(**data)
        session.add(db_garment)
        session.commit()
        return db_garment

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
            "status": "ok",
            "journaling_key": key,
        }
        m_send_notification.assert_called_with(
            "A new garment called Some test garment has been created"
        )

    def test_get_non_existing_garment(self, client):
        response = client.get("/garments/99")
        assert response.status_code == 404

    @pytest.mark.skip(reason="no longer valid")
    def test_get_current_user(self, client):
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
                "status": "ok",
                "image": None,
                "journaling_key": str(key),
            },
            {
                "id": 2,
                "name": "Test garment",
                "garment_type": "Shoe",
                "color": "red",
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
