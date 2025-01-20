import requests
from . import models
from sqlalchemy.orm import Session


def _get_weather_query(place: str):
    return f"https://api.open-meteo.com/v1/forecast?latitude={place.latitude}&longitude={place.longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe%2FBerlin&forecast_days=1"


def get_complete_weather(place: str):
    try:
        response = requests.get(_get_weather_query(place))
        data = response.json()
        max_temperature = data["daily"]["temperature_2m_max"][0]
        min_temperature = data["daily"]["temperature_2m_min"][0]
        avg_temperature = (max_temperature + min_temperature) / 2
        return {
            "min": min_temperature,
            "avg": avg_temperature,
            "max": max_temperature,
        }
    except Exception as e:
        raise Exception(f"Error getting weather for {place}: {e}") from e


def get_simplified_weather(db: Session, place: str):
    try:
        response = requests.get(_get_weather_query(place))
        data = response.json()
        max_temperature = data["daily"]["temperature_2m_max"][0]
        min_temperature = data["daily"]["temperature_2m_min"][0]
        avg_temperature = (max_temperature + min_temperature) / 2
        for weather_range in (
            db.query(models.WeatherRange).order_by(models.WeatherRange.max).all()
        ):
            if avg_temperature <= weather_range.max:
                return weather_range.name
        raise Exception(f"Temperature {avg_temperature} not found in configuration")
    except Exception as e:
        raise Exception(f"Error getting weather for {place}: {e}") from e
