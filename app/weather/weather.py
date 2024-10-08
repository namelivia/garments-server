import requests


def get_weather(place: str):
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={place.latitude}&longitude={place.longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe%2FBerlin&forecast_days=1"
        )
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
