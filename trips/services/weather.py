import requests
import datetime
from django.conf import settings

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather_and_forecast(destination, start_date=None, end_date=None):
    weather = None
    forecast = []

    if not destination:
        return None, []

    try:
        # =========================
        # CURRENT WEATHER
        # =========================
        current_params = {
            "q": destination,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
        }

        current_res = requests.get(
            BASE_CURRENT_URL,
            params=current_params,
            timeout=5
        )

        if current_res.status_code == 200:
            current_data = current_res.json()

            weather = {
                "temp": round(current_data["main"]["temp"]),
                "description": current_data["weather"][0]["description"].title(),
                "icon": current_data["weather"][0]["icon"],
                "city": current_data.get("name", destination),
            }

        # =========================
        # FORECAST
        # =========================
        forecast_params = {
            "q": destination,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
        }

        forecast_res = requests.get(
            BASE_FORECAST_URL,
            params=forecast_params,
            timeout=5
        )

        if forecast_res.status_code == 200:
            forecast_data = forecast_res.json()

            seen_dates = set()
            day_index = 0

            for item in forecast_data.get("list", []):
                dt = datetime.datetime.fromtimestamp(item["dt"])
                day = dt.date()

                # filter by trip range (optional)
                if start_date and end_date:
                    if not (start_date <= day <= end_date):
                        continue

                # only one entry per day
                if day in seen_dates:
                    continue

                seen_dates.add(day)
                day_index += 1

                forecast.append({
                    "day_label": f"Day {day_index}",
                    "date": day.strftime("%a, %b %d"),
                    "temp": round(item["main"]["temp"]),
                    "icon": item["weather"][0]["icon"],
                })

    except requests.RequestException as e:
        print("Weather API error:", e)

    return weather, forecast