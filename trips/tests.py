from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from unittest.mock import patch

from .models import Trip, SavedPlace, ItineraryItem, Profile


# =====================================================
# BASE SETUP
# =====================================================

class BaseSetup(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Avoid duplicate profile issue
        self.profile, _ = Profile.objects.get_or_create(
            user=self.user,
            defaults={"role": "traveler"}
        )

        self.client.login(
            username="testuser",
            password="password123"
        )

        self.trip = Trip.objects.create(
            user=self.user,
            title="Paris Trip",
            destination="Paris",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 5),
            is_published=False
        )

        self.place = SavedPlace.objects.create(
            user=self.user,
            name="Eiffel Tower",
            location="Paris",
            latitude=48.8584,
            longitude=2.2945
        )


# =====================================================
# AUTH TESTS
# =====================================================

class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            username="user",
            password="pass123"
        )

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "user",
                "password": "pass123"
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "user",
                "password": "wrong"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "new@test.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!"
            }
        )

        self.assertEqual(response.status_code, 302)


# =====================================================
# HOME + DASHBOARD
# =====================================================

class HomeDashboardTests(BaseSetup):

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_search(self):
        response = self.client.get(
            reverse("home"),
            {"q": "Paris"}
        )

        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_search(self):
        response = self.client.get(
            reverse("dashboard"),
            {"q": "Paris"}
        )

        self.assertEqual(response.status_code, 200)


# =====================================================
# PROFILE
# =====================================================

class ProfileTests(BaseSetup):

    def test_profile_get(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        response = self.client.post(
            reverse("profile"),
            {
                "username": "updateduser",
                "email": "updated@test.com",
                "role": "traveler"
            }
        )

        self.assertIn(response.status_code, [200, 302])


# =====================================================
# TRIP TESTS
# =====================================================

class TripTests(BaseSetup):

    def test_add_trip(self):
        response = self.client.post(
            reverse("add_trip"),
            {
                "title": "Rome Trip",
                "destination": "Rome",
                "start_date": "2026-06-10",
                "end_date": "2026-06-15"
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_trip(self):
        response = self.client.post(
            reverse("edit_trip", args=[self.trip.id]),
            {
                "title": "Updated Trip",
                "destination": "Paris",
                "start_date": self.trip.start_date,
                "end_date": self.trip.end_date
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_trip(self):
        response = self.client.post(
            reverse("delete_trip", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_trip_detail(self):
        response = self.client.get(
            reverse("trip_detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_trip_detail_404(self):
        response = self.client.get(
            reverse("trip_detail", args=[9999])
        )

        self.assertEqual(response.status_code, 404)

    def test_toggle_publish(self):
        response = self.client.post(
            reverse("toggle_publish_trip", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 302)

        self.trip.refresh_from_db()

        self.assertTrue(self.trip.is_published)


# =====================================================
# ITINERARY TESTS
# =====================================================

class ItineraryTests(BaseSetup):

    def test_add_item(self):
        response = self.client.post(
            reverse("add_item", args=[self.trip.id]),
            {
                "title": "Louvre",
                "location": "Paris",
                "date": self.trip.start_date
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_item(self):
        item = ItineraryItem.objects.create(
            trip=self.trip,
            title="Museum",
            location="Paris",
            date=self.trip.start_date
        )

        response = self.client.post(
            reverse("delete_item", args=[item.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_item(self):
        item = ItineraryItem.objects.create(
            trip=self.trip,
            title="Old",
            location="Paris",
            date=self.trip.start_date
        )

        response = self.client.post(
            reverse("edit_item", args=[item.id]),
            {
                "title": "New",
                "location": "Paris",
                "date": self.trip.start_date
            }
        )

        self.assertIn(response.status_code, [200, 302])

    def test_planner(self):
        response = self.client.get(
            reverse("planner", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)


# =====================================================
# SAVED PLACES
# =====================================================

class SavedPlacesTests(BaseSetup):

    def test_saved_places(self):
        response = self.client.get(reverse("saved_places"))
        self.assertEqual(response.status_code, 200)

    def test_add_saved_place_get(self):
        response = self.client.get(reverse("add_saved_place"))
        self.assertEqual(response.status_code, 200)

    def test_add_saved_place_post(self):
        response = self.client.post(
            reverse("add_saved_place"),
            {
                "name": "Museum",
                "location": "Paris",
                "latitude": 1,
                "longitude": 1
            }
        )

        self.assertIn(response.status_code, [200, 302])

    def test_delete_saved_place(self):
        response = self.client.post(
            reverse("delete_place", args=[self.place.id])
        )

        self.assertEqual(response.status_code, 302)


# =====================================================
# AJAX TESTS
# =====================================================

class AjaxTests(BaseSetup):

    def test_add_place_to_trip_ajax(self):
        response = self.client.post(
            reverse("add_place_to_trip_ajax"),
            {
                "place_id": self.place.id,
                "trip_id": self.trip.id
            }
        )

        self.assertTrue(response.json()["success"])

    def test_save_place_ajax(self):
        response = self.client.post(
            reverse("save_place_ajax"),
            {
                "name": "Tower Bridge",
                "location": "London",
                "lat": "51",
                "lon": "0"
            }
        )

        self.assertTrue(response.json()["success"])


# =====================================================
# SEARCH PLACES
# =====================================================

class SearchPlacesTests(BaseSetup):

    @patch("requests.get")
    def test_search_places_success(self, mock_get):

        mock_response = mock_get.return_value

        mock_response.json.return_value = {
            "results": [
                {
                    "formatted": "Paris, France",
                    "geometry": {
                        "lat": 48,
                        "lng": 2
                    }
                }
            ]
        }

        response = self.client.get(
            reverse("search_places"),
            {"q": "Paris"}
        )

        self.assertEqual(response.status_code, 200)

    def test_search_places_empty(self):
        response = self.client.get(reverse("search_places"))
        self.assertEqual(response.status_code, 200)


# =====================================================
# REVIEWS
# =====================================================

class ReviewTests(BaseSetup):

    def test_add_review(self):

        self.trip.is_published = True
        self.trip.save()

        response = self.client.post(
            reverse("add_review", args=[self.trip.id]),
            {
                "rating": 5,
                "comment": "Amazing"
            }
        )

        self.assertIn(response.status_code, [200, 302])


# =====================================================
# PERMISSIONS
# =====================================================

class PermissionTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.owner = User.objects.create_user(
            username="owner",
            password="pass"
        )

        self.other = User.objects.create_user(
            username="other",
            password="pass"
        )

        self.trip = Trip.objects.create(
            user=self.owner,
            title="Private",
            destination="Berlin",
            start_date=date.today(),
            end_date=date.today()
        )

    def test_other_user_cannot_edit_trip(self):

        self.client.login(
            username="other",
            password="pass"
        )

        response = self.client.post(
            reverse("edit_trip", args=[self.trip.id]),
            {"title": "Hack"}
        )

        self.assertEqual(response.status_code, 404)


# =====================================================
# TRIP DETAIL COVERAGE
# =====================================================

class TripDetailCoverageTests(BaseSetup):

    def test_trip_detail_no_destination(self):

        self.trip.destination = ""
        self.trip.save()

        response = self.client.get(
            reverse("trip_detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)

    @patch("trips.views.get_weather_and_forecast")
    def test_trip_detail_weather_none(self, mock_weather):

        mock_weather.return_value = (None, [])

        response = self.client.get(
            reverse("trip_detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)

    @patch("trips.views.get_coordinates", side_effect=Exception("fail"))
    def test_trip_detail_map_failure(self, mock_geo):

        response = self.client.get(
            reverse("trip_detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)

    @patch("trips.views.get_country_info")
    @patch("trips.views.get_weather_and_forecast")
    def test_trip_detail_country_failure(
        self,
        mock_weather,
        mock_country
    ):

        mock_weather.return_value = ({}, [])
        mock_country.side_effect = Exception("API fail")

        response = self.client.get(
            reverse("trip_detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)

    @patch("trips.views.get_weather_and_forecast")
    @patch("trips.views.get_country_info")
    @patch("trips.views.get_coordinates")
    def test_trip_detail_full_mock(
        self,
        mock_coords,
        mock_country,
        mock_weather
    ):

        mock_coords.return_value = (48.85, 2.35)

        mock_country.return_value = {
            "name": "France"
        }

        mock_weather.return_value = (
            {"temp": 20},
            [{"day": "Mon"}]
        )

        response = self.client.get(
            reverse("trip_detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)