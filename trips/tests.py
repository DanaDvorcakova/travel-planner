from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import date
from unittest.mock import patch, Mock

from .models import Trip, SavedPlace, ItineraryItem
from .services.weather import get_weather_and_forecast
from .services.maps import get_coordinates
from .services.country import get_country_info

# =========================
# BASE SETUP
# =========================
class BaseSetup(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.trip = Trip.objects.create(
            user=self.user,
            title="Paris Trip",
            destination="Paris",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 5)
        )
        self.place = SavedPlace.objects.create(
            user=self.user,
            name="Eiffel Tower",
            location="Paris",
            latitude=48.8584,
            longitude=2.2945
        )

# =========================
# TRIP TESTS
# =========================
class TripTests(BaseSetup):
    def test_create_trip_invalid_dates(self):
        response = self.client.post(reverse("add_trip"), {
            "title": "Bad Trip",
            "destination": "Rome",
            "start_date": "2026-06-10",
            "end_date": "2026-06-01"
        })
        self.assertEqual(response.status_code, 200)

    def test_edit_trip(self):
        response = self.client.post(reverse("edit_trip", args=[self.trip.id]), {
            "title": "Updated",
            "destination": "Paris",
            "start_date": self.trip.start_date,
            "end_date": self.trip.end_date
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_trip(self):
        response = self.client.post(reverse("delete_trip", args=[self.trip.id]))
        self.assertEqual(response.status_code, 302)

    def test_trip_detail(self):
        response = self.client.get(reverse("trip_detail", args=[self.trip.id]))
        self.assertEqual(response.status_code, 200)

# =========================
# ITINERARY TESTS
# =========================
class ItineraryTests(BaseSetup):
    def test_add_item(self):
        response = self.client.post(reverse("add_item", args=[self.trip.id]), {
            "title": "Louvre",
            "location": "Paris",
            "date": self.trip.start_date
        })
        self.assertEqual(response.status_code, 302)

    def test_add_item_invalid(self):
        response = self.client.post(reverse("add_item", args=[self.trip.id]), {})
        self.assertEqual(response.status_code, 200)

    def test_add_item_outside_trip(self):
        response = self.client.post(reverse("add_item", args=[self.trip.id]), {
            "title": "Invalid",
            "location": "Paris",
            "date": date(2026, 5, 1)
        })
        self.assertEqual(response.status_code, 200)

    def test_add_item_get(self):
        response = self.client.get(reverse("add_item", args=[self.trip.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        item = ItineraryItem.objects.create(trip=self.trip, title="Test", location="Paris", date=self.trip.start_date)
        response = self.client.post(reverse("delete_item", args=[item.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_item_unauthorized(self):
        other = User.objects.create_user("other", password="pass")
        item = ItineraryItem.objects.create(trip=self.trip, title="Test", location="Paris", date=self.trip.start_date)
        self.client.login(username="other", password="pass")
        response = self.client.post(reverse("delete_item", args=[item.id]))
        self.assertNotEqual(response.status_code, 200)

# =========================
# AJAX TESTS
# =========================
class AjaxTests(BaseSetup):
    def test_add_place_to_trip(self):
        response = self.client.post(reverse("add_place_to_trip_ajax"), {
            "place_id": self.place.id,
            "trip_id": self.trip.id
        })
        self.assertTrue(response.json()["success"])

    def test_add_place_invalid(self):
        response = self.client.post(reverse("add_place_to_trip_ajax"), {"place_id": 999})
        self.assertFalse(response.json()["success"])

    def test_save_place(self):
        response = self.client.post(reverse("save_place_ajax"), {
            "name": "Tower Bridge",
            "location": "London",
            "lat": "51",
            "lon": "0"
        })
        self.assertTrue(response.json()["success"])

    def test_save_place_invalid(self):
        response = self.client.post(reverse("save_place_ajax"), {})
        self.assertFalse(response.json()["success"])

# =========================
# AUTH TESTS
# =========================
class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user("user", password="pass123")

    def test_login(self):
        response = self.client.post(reverse("login"), {"username": "user", "password": "pass123"})
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(reverse("login"), {"username": "user", "password": "wrong"})
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post(reverse("signup"), {
            "username": "new",
            "email": "new@test.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!"
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username="user", password="pass123")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

# =========================
# PERMISSIONS
# =========================
class PermissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u1 = User.objects.create_user("u1", password="pass")
        self.u2 = User.objects.create_user("u2", password="pass")
        self.trip = Trip.objects.create(
            user=self.u1,
            title="Private",
            destination="Berlin",
            start_date=date.today(),
            end_date=date.today()
        )
        self.client.login(username="u2", password="pass")

    def test_edit_other_trip(self):
        response = self.client.post(reverse("edit_trip", args=[self.trip.id]), {"title": "Hack"})
        self.assertNotEqual(response.status_code, 200)

    def test_delete_other_trip(self):
        response = self.client.post(reverse("delete_trip", args=[self.trip.id]))
        self.assertNotEqual(response.status_code, 200)

# =========================
# MESSAGES
# =========================
class MessageTests(BaseSetup):
    def test_add_message(self):
        response = self.client.post(reverse("add_item", args=[self.trip.id]), {
            "title": "Msg",
            "location": "Paris",
            "date": self.trip.start_date
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("added" in str(m).lower() for m in messages))

    def test_delete_message(self):
        item = ItineraryItem.objects.create(trip=self.trip, title="Del", location="Paris", date=self.trip.start_date)
        response = self.client.post(reverse("delete_item", args=[item.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("deleted" in str(m).lower() for m in messages))

# =========================
# COVERAGE BOOST + FIXED FAILURES
# =========================
class CoverageBoostTests(BaseSetup):

    def setUp(self):
        super().setUp()
        self.trip = Trip.objects.create(
            user=self.user,
            title="Test Trip",
            destination="Paris",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 10),
            is_published=False
        )

    def test_delete_trip_get(self):
        url = reverse("delete_trip", args=[self.trip.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_delete_item_get(self):
        item = ItineraryItem.objects.create(trip=self.trip, title="Test", location="Paris", date=self.trip.start_date)
        response = self.client.get(reverse("delete_item", args=[item.id]))
        self.assertEqual(response.status_code, 405)

    def test_save_place_missing_fields(self):
        response = self.client.post(reverse("save_place_ajax"), {})
        self.assertFalse(response.json()["success"])

    @patch("trips.views.requests.get")
    def test_search_places_api_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"success": False, "error": "API fail"}
        mock_get.return_value = mock_response

        response = self.client.get(reverse("search_places"), {"q": "Paris"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error")

    @patch("trips.views.get_weather_and_forecast")
    def test_trip_detail_api_failures(self, mock_weather):
        mock_weather.return_value = (None, None)
        response = self.client.get(reverse("trip_detail", args=[self.trip.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.trip.destination)