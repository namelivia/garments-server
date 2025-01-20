from mock import patch, Mock
import uuid
from app.notifications.notifications import Notifications
from app.journaling.journaling import Journaling
from app.weather.models import WeatherRange
from app.weather.weather import get_simplified_weather
from .test_base import (
    database_test_session,
)


class TestServices:
    @patch("requests.post")
    def test_sending_a_notification(self, m_post):
        Notifications.send("Test message")
        m_post.assert_called_with(
            url="http://notifications-service:80",
            json={"body": "Test message"},
        )

    @patch("requests.post")
    def test_creating_a_journal_entry(self, m_post):
        key = uuid.uuid4()
        message = "Test message"
        Journaling.create(key, message)
        m_post.assert_called_with(
            url="http://journaling-service:80/new",
            json={
                "key": str(key),
                "message": message,
            },
        )

    @patch("requests.get")
    def test_retrieving_a_journal_entryset(self, m_get):
        key = uuid.uuid4()
        response_mock = Mock()
        response_mock.text = '{"data": "journaling_data"}'
        response_mock.json = lambda: {"data": "journaling_data"}
        m_get.return_value = response_mock
        response = Journaling.get(key)
        m_get.assert_called_with(
            url=f"http://journaling-service:80/{str(key)}/all",
        )
        assert response["data"] == "journaling_data"

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

    @patch("requests.get")
    def test_get_simplified_weather(self, m_get, database_test_session):
        m_get.return_value.json.return_value = {
            "daily": {
                "time": ["2024-06-08"],
                "temperature_2m_max": [9.4],
                "temperature_2m_min": [6.9],
            },
        }
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
        self._insert_test_weather_range(
            database_test_session,
            {
                "name": "cold",
                "max": 10,
            },
        )
        test_place = Mock()
        test_place.latitude = "0.00001"
        test_place.longitude = "0.0001"
        assert get_simplified_weather(database_test_session, test_place) == "cold"
