import requests


def get_country_info(destination):
    if not destination:
        return None

    try:
        # STEP 1: get coordinates from your existing service
        from .maps import get_coordinates

        lat, lon = get_coordinates(destination)

        if not lat or not lon:
            return None

        # STEP 2: reverse geocode → get country
        nominatim_url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lon}&format=json"
        )

        headers = {
            "User-Agent": "trip-planner-app"
        }

        res = requests.get(nominatim_url, headers=headers, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()
        address = data.get("address", {})

        country_code = address.get("country_code")

        if not country_code:
            return None

        # STEP 3: get full country data
        country_res = requests.get(
            f"https://restcountries.com/v3.1/alpha/{country_code}",
            timeout=5
        )

        if country_res.status_code != 200:
            return None

        c = country_res.json()[0]

        currencies = c.get("currencies", {})
        currency = list(currencies.keys())[0] if currencies else None

        languages = c.get("languages", {})
        language = list(languages.values())[0] if languages else None

        return {
            "name": c.get("name", {}).get("common"),
            "capital": c.get("capital", [None])[0],
            "region": c.get("region"),
            "population": c.get("population"),
            "flag": c.get("flags", {}).get("png"),
            "currency": currency,
            "language": language,
        }

    except Exception as e:
        print("Country info error:", e)
        return None