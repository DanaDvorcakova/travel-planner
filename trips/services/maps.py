import requests
from django.conf import settings

BASE_URL = "https://api.opencagedata.com/geocode/v1/json"


def get_coordinates(location):
    params = {
        "q": location,
        "key": settings.OPENCAGE_API_KEY,
        "limit": 1,
        "no_annotations": 1
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data.get("results"):
            geometry = data["results"][0]["geometry"]
            return geometry["lat"], geometry["lng"]

    except requests.RequestException as e:
        print("Geocoding error:", e)

    return None, None


    

 