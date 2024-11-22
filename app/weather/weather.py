import requests


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


def get_simplified_weather(place: str):
    try:
        response = requests.get(_get_weather_query(place))
        data = response.json()
        max_temperature = data["daily"]["temperature_2m_max"][0]
        min_temperature = data["daily"]["temperature_2m_min"][0]
        avg_temperature = (max_temperature + min_temperature) / 2
        if avg_temperature < 5:
            return "cold"
        elif avg_temperature < 16:
            return "mild"
        else:
            return "hot"
    except Exception as e:
        raise Exception(f"Error getting weather for {place}: {e}") from e
