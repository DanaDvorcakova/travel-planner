# =========================
# DJANGO CORE
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, views as auth_views
from django.contrib import messages
from django.db.models import Q, Avg, F
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.views.decorators.http import require_POST

from datetime import date
from math import floor, ceil
import json
import requests

# =========================
# SERVICES
# =========================
from .services.maps import get_coordinates
from .services.weather import get_weather_and_forecast
from .services.country import get_country_info

# =========================
# MODELS
# =========================
from .models import (
    Trip,
    SavedPlace,
    ItineraryItem,
    Profile,
    Review
)

# =========================
# FORMS
# =========================
from .forms import (
    TripForm,
    SignUpForm,
    ItineraryItemForm,
    SavedPlaceForm,
    ReviewForm,
    UserUpdateForm,
    ProfileUpdateForm,
    StyledPasswordResetForm
)



def get_role(user):
    return user.profile.role if hasattr(user, "profile") else "traveler"

# =========================
# PROFILE PAGE
# =========================
@login_required
def profile(request):

    # Create profile if missing
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=profile
        )

    return render(request, 'trips/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'role': get_role(request.user)
    })

class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = StyledPasswordResetForm
    template_name = "registration/password_reset_form.html"

# =========================
# LANDING PAGE
# =========================
def home(request):
    trips = Trip.objects.filter(is_published=True).annotate(avg_rating=Avg('reviews__rating'))


    # 🔍 SEARCH (FIXED)
    query = request.GET.get('q')
    destination = request.GET.get('destination')
    style = request.GET.get('style')

    # If user types in search bar
    if query:
        trips = trips.filter(
            Q(title__icontains=query) |
            Q(destination__icontains=query)
        )

    # If user clicks destination cards
    if destination:
        trips = trips.filter(destination__icontains=destination)

    if style:
        trips = trips.filter(
            user__profile__travel_style__iexact=style
        )

    trips = trips.order_by('-id')

    paginator = Paginator(trips, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    for trip in page_obj:
        avg = trip.avg_rating or 0
        full_stars = int(avg)
        half_star = 1 if avg - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star

        trip.full_stars_range = range(full_stars)
        trip.half_star = half_star
        trip.empty_stars_range = range(empty_stars)
        trip.avg_rating = avg  # ensures avg_rating is always available

    return render(request, 'trips/landing.html', {
        'page_obj': page_obj,
        'query': query or "",
        'destination': destination or "",
        'style': style or "" 
    })

# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user)

    # =========================
    # 🔍 FILTERS
    # =========================
    query = request.GET.get('q')
    if query:
        trips = trips.filter(
            Q(title__icontains=query) |
            Q(destination__icontains=query)
        )

    destination = request.GET.get('destination')
    if destination:
        trips = trips.filter(destination__icontains=destination)

    start_date = request.GET.get('start_date')
    if start_date:
        trips = trips.filter(start_date__gte=start_date)

    # =========================
    # STATS (BEFORE PAGINATION)
    # =========================
    total_trips = trips.count()
    published_trips = trips.filter(is_published=True).count()
    upcoming_trips = trips.filter(start_date__gte=date.today()).count()

    next_trip = trips.filter(
        start_date__gte=date.today()
    ).order_by('start_date').first()

    days_left = None
    if next_trip and next_trip.start_date:
        days_left = (next_trip.start_date - date.today()).days

    # =========================
    # PAGINATION (IMPORTANT)
    # =========================
    trips = trips.order_by('-id')
    paginator = Paginator(trips, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # =========================
    # RETURN
    # =========================
    return render(request, 'trips/dashboard.html', {
        'page_obj': page_obj,
        'total_trips': total_trips,
        'published_trips': published_trips,
        'upcoming_trips': upcoming_trips,
        'next_trip': next_trip,
        'days_left': days_left,
    })

# =========================
#  ADD TRIP
# =========================
@login_required
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, "Trip created successfully.")
            return redirect('dashboard')
    else:
        form = TripForm()

    return render(request, 'trips/add_trip.html', {'form': form})

# =========================
# EDIT TRIP
# =========================
@login_required
def edit_trip(request, id):
    trip = get_object_or_404(Trip, id=id)

    role = get_role(request.user)

    if trip.user != request.user and role != "admin":
        raise Http404()
    
    if request.method == 'POST':
        old_start_date = trip.start_date
        form = TripForm(request.POST, request.FILES, instance=trip)

        if form.is_valid():
            updated_trip = form.save(commit=False)
            new_start_date = updated_trip.start_date

            updated_trip.save()

            # shift itinerary if date changed
            if old_start_date != new_start_date:
                delta = new_start_date - old_start_date

                for item in trip.itinerary.all():
                    item.date = item.date + delta
                    item.save()
            messages.success(request, "Trip updated successfully.")
            return redirect('dashboard')
    else:
        form = TripForm(instance=trip)

    return render(request, 'trips/edit_trip.html', {'form': form})

# =========================
# DELETE TRIP
# =========================
@login_required
@require_POST
def delete_trip(request, id):
    trip = get_object_or_404(Trip, id=id)

    role = get_role(request.user)

    if trip.user != request.user and role != "admin":
        raise Http404()

    trip.delete()
    messages.warning(request, "Trip deleted.")
    return redirect('dashboard')


# =========================
# PUBLISH / UNPUBLISH TRIP
# =========================
@login_required
@require_POST
def toggle_publish_trip(request, id):

    trip = get_object_or_404(Trip, id=id)

    role = get_role(request.user)

    if trip.user != request.user and role != "admin":
        raise Http404()

    trip.is_published = not trip.is_published
    trip.save()

    if trip.is_published:
        messages.success(request, "Trip published successfully.")
    else:
        messages.warning(request, "Trip unpublished successfully.")

    return redirect('trip_detail', id=trip.id)

# =========================
# SIGNUP
# =========================
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

# =========================
# SAVED PLACES (LIST + SEARCH + PAGINATION)
# =========================
@login_required
def saved_places(request):
    places_list = SavedPlace.objects.filter(user=request.user).order_by('-created_at')

    # 🔍 SEARCH
    query = request.GET.get('q')
    if query:
        places_list = places_list.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    # 📄 PAGINATION (6 per page)
    paginator = Paginator(places_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'trips/saved_places.html', {
        'page_obj': page_obj,
        'query': query
    })

# =========================
# ADD SAVED PLACE (FORM)
# =========================
@login_required
def add_saved_place(request):
    if request.method == 'POST':
        form = SavedPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            return redirect('saved_places')
    else:
        form = SavedPlaceForm()

    return render(request, 'trips/add_saved_place.html', {
        'form': form
    })

# =========================
# SEARCH REAL PLACES (API)
# =========================
@login_required
def search_places(request):
    query = request.GET.get('q')  # ✅ use request.GET.get
    results = []

    if query:
        url = "https://api.opencagedata.com/geocode/v1/json"

        params = {
            "q": query,
            "key": settings.OPENCAGE_API_KEY,
            "limit": 5
        }

        res = requests.get(url, params=params)
        data = res.json()

        if data.get("results"):
            for item in data["results"]:
                results.append({
                    "name": item["formatted"],
                    "lat": item["geometry"]["lat"],
                    "lon": item["geometry"]["lng"]
                })

    return render(request, "trips/search_places.html", {
        "results": results,
        "query": query
    })


# =========================
# ADD PLACE (AJAX)
# =========================
@login_required
def add_place_to_trip_ajax(request):
    if request.method == "POST":
        try:
            place_id = request.POST.get("place_id")
            trip_id = request.POST.get("trip_id")

            place = get_object_or_404(
                SavedPlace,
                id=place_id,
                user=request.user
            )

            trip = get_object_or_404(Trip, id=trip_id)

            role = get_role(request.user)

            # 🔐 Permission check
            if trip.user != request.user and role != "admin":
                return JsonResponse({
                    "success": False,
                    "error": "Permission denied"
                })

            ItineraryItem.objects.create(
                trip=trip,
                title=place.name,
                location=place.location,
                date=trip.start_date,
                latitude=place.latitude,
                longitude=place.longitude
            )

            return JsonResponse({
                "success": True,
                "trip_name": trip.title
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    return JsonResponse({"success": False})


# =========================
# SAVE PLACE (AJAX)
# =========================
@login_required
@require_POST
def save_place_ajax(request):
    try:
        name = request.POST.get("name")
        location = request.POST.get("location") or name
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        if not name:
            return JsonResponse({"success": False, "error": "No name"})

        SavedPlace.objects.create(
            user=request.user,
            name=name,
            location=location,
            latitude=float(lat) if lat else None,
            longitude=float(lon) if lon else None
        )

        return JsonResponse({
            "success": True,
            "message": "Place saved"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

# =========================
# SAVE FROM SEARCH 
# =========================
@login_required
def save_place_from_search(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        SavedPlace.objects.create(
            user=request.user,
            name=name,
            location=location,
            latitude=float(lat) if lat else None,
            longitude=float(lon) if lon else None
        )
        messages.success(request, "Place saved.")
        return redirect('saved_places')

    return redirect('saved_places')  


# =========================
#  EDIT SAVED PLACE
# =========================
@login_required
def edit_saved_place(request, id):
    place = get_object_or_404(SavedPlace, id=id, user=request.user)

    if request.method == "POST":
        form = SavedPlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.success(request, "Place updated.")
            return redirect('saved_places')
    else:
        form = SavedPlaceForm(instance=place)

    return render(request, 'trips/edit_saved_place.html', {
        'form': form,
        'place': place
    })

# =========================
# DELETE SAVED PLACE
# =========================
@login_required
@require_POST
def delete_saved_place(request, id):
    place = get_object_or_404(SavedPlace, id=id, user=request.user)   
    place.delete()
    messages.warning(request, "Place removed.")
    return redirect('saved_places')

    
# =========================
#  ITINERARY ITEM
# =========================
@login_required
def add_itinerary_item(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    role = get_role(request.user)

    if trip.user != request.user and role != "admin":
        raise Http404()

    place_id = request.GET.get('place')

    if place_id:
        place = get_object_or_404(SavedPlace, id=place_id, user=request.user)
        lat, lon = get_coordinates(place.location)

        ItineraryItem.objects.create(
            trip=trip,
            title=place.name,
            location=place.location,
            date=trip.start_date,
            latitude=lat,
            longitude=lon
        )
        messages.success(request, "Place added to your itinerary.")
        return redirect('trip_detail', id=trip.id)

    if request.method == 'POST':
        form = ItineraryItemForm(request.POST, trip=trip)

        if form.is_valid():
            item = form.save(commit=False)

            lat, lon = get_coordinates(item.location)

            item.latitude = lat
            item.longitude = lon
            item.trip = trip

            item.save()
            messages.success(request, "Item added to your itinerary.")
            return redirect('trip_detail', id=trip.id)

    else:
        form = ItineraryItemForm(trip=trip)

    return render(request, 'trips/add_itinerary_item.html', {
        'form': form,
        'trip': trip
    })

# =========================
#  DELETE ITEM
# =========================
@login_required
@require_POST
def delete_itinerary_item(request, id):
    item = get_object_or_404(ItineraryItem, id=id)

    role = get_role(request.user)

    if item.trip.user != request.user and role != "admin":
        raise Http404()
    trip_id = item.trip.id

    item.delete()
    messages.success(request, "Item deleted from itinerary.")
    return redirect('trip_detail', id=trip_id)


# =========================
#  EDIT ITEM
# =========================
@login_required
def edit_itinerary_item(request, id):
    item = get_object_or_404(ItineraryItem, id=id)

    role = get_role(request.user)

    if item.trip.user != request.user and role != "admin":
        raise Http404()

    if request.method == 'POST':
        form = ItineraryItemForm(request.POST, instance=item, trip=item.trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated.")
            return redirect('trip_detail', id=item.trip.id)
    else:
        form = ItineraryItemForm(instance=item, trip=item.trip)

    return render(request, 'trips/edit_itinerary_item.html', {
        'form': form,
        'item': item
    })

# =========================
#  ITINERARY PAGE
# =========================
@login_required
def itinerary_planner(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    role = get_role(request.user)

    if trip.user != request.user and role != "admin":
        raise Http404()

    items = trip.itinerary.all().order_by('date', 'time')

    return render(request, 'trips/itinerary_planner.html', {
        'trip': trip,
        'items': items
    })



# =========================
#  TRIP DETAIL
# =========================
def trip_detail(request, id):

    trip = get_object_or_404(Trip, id=id)

    # 🔐 Access control (only owner can view unpublished trips)
    if not trip.is_published:
        role = get_role(request.user) if request.user.is_authenticated else None

        if (
            not request.user.is_authenticated or
            (
                trip.user != request.user and
                role != "admin"
            )
        ):
            raise Http404()

    # =========================
    # WEATHER
    # =========================
    weather = None
    forecast = []
    weather_message = None

    today = date.today()

    if trip.end_date < today:
        weather_message = "Weather history is unavailable for past trips."

    elif trip.destination:
        weather, forecast = get_weather_and_forecast(
            trip.destination,
            trip.start_date,
            trip.end_date
        )

        if not weather:
            weather_message = "Weather forecast is currently unavailable."

    # =========================
    # 🗺 MAP COORDINATES
    # =========================
    map_lat, map_lon = None, None

    if trip.destination:
        try:
            map_lat, map_lon = get_coordinates(trip.destination)
        except Exception as e:
            print("Map error:", e)

    # =========================
    # COUNTRY INFO
    # =========================
    country_info = None

    if trip.destination:
        try:
            url = "https://api.opencagedata.com/geocode/v1/json"

            params = {
                "q": trip.destination,
                "key": settings.OPENCAGE_API_KEY,
                "limit": 1
            }

            response = requests.get(url, params=params)
            data = response.json()

            if data.get("results"):
                components = data["results"][0].get("components", {})
                country_name = components.get("country")

                if country_name:
                    country_info = get_country_info(country_name)

        except Exception as e:
            print("Country API error:", e)

    # =========================
    # MAP PINS
    # =========================
    places = []

    if map_lat and map_lon:
        places.append({
            "name": trip.destination,
            "title": "Trip Destination",
            "lat": float(map_lat),
            "lon": float(map_lon),
            "date": str(trip.start_date),
            "google_url": f"https://www.google.com/maps?q={map_lat},{map_lon}"
        })

    for item in trip.itinerary.all():
        if item.latitude and item.longitude:
            places.append({
                "name": item.location,
                "title": item.title,
                "lat": float(item.latitude),
                "lon": float(item.longitude),
                "date": item.date.strftime("%Y-%m-%d"),
                "google_url": f"https://www.google.com/maps?q={item.latitude},{item.longitude}"
            })

    # =========================
    #  REVIEWS
    # =========================
    reviews = trip.reviews.select_related('user').all()
    avg_rating = trip.average_rating or 0  # make sure it's not None

    # full, half, empty stars for average
    full_avg = int(floor(avg_rating))
    half_avg = 1 if (avg_rating - full_avg) >= 0.5 else 0
    empty_avg = 5 - full_avg - half_avg

    # individual review stars
    for review in reviews:
        review.full_stars_range = range(int(review.rating))
        review.empty_stars_range = range(5 - int(review.rating))

    # =========================
    # TEMPLATE CONTEXT
    # =========================
    return render(request, 'trips/trip_detail.html', {
        'trip': trip,
        'weather': weather,
        'forecast': forecast,
        'country_info': country_info,
        'places_json': json.dumps(places, cls=DjangoJSONEncoder),
        'map_lat': map_lat,
        'map_lon': map_lon,
        'reviews': reviews,
        'average_rating': avg_rating,
        'full_stars_avg': range(full_avg),
        'half_star_avg': half_avg,
        'empty_stars_avg': range(empty_avg),
        'review_form': ReviewForm() if request.user.is_authenticated else None,
        'weather_message': weather_message,
    })

# =========================
# ADD REVIEW
# =========================
@login_required
def add_review(request, id):  
    trip = get_object_or_404(Trip, id=id, is_published=True)

    # Check if user already reviewed
    existing_review = Review.objects.filter(trip=trip, user=request.user).first()
    if existing_review:
        messages.warning(request, "You have already reviewed this trip.")
        return redirect('trip_detail', id=trip.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.trip = trip
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('trip_detail', id=review.trip.id)
    else:
        form = ReviewForm()

    return render(request, "trips/add_review.html", {
        "form": form,
        "trip": trip
    })
   
# =========================
# EDIT REVIEW
# =========================
@login_required
def edit_review(request, id):
    review = get_object_or_404(Review, id=id)

    role = get_role(request.user)

    # 🔐 Permission check
    if review.user != request.user and role != "admin":
        messages.error(request, "You cannot edit this review.")
        return redirect('trip_detail', id=review.trip.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, "Review updated.")
            return redirect('trip_detail', id=review.trip.id)

    else:
        form = ReviewForm(instance=review)

    return render(request, "trips/edit_review.html", {
        "form": form,
        "trip": review.trip,
        "review": review
    })

# =========================
#  DELETE REVIEW
# =========================
@login_required
@require_POST
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)

    role = get_role(request.user)

    # 🔐 permission check
    if review.user != request.user and role != "admin":
        messages.error(request, "You cannot delete this review.")
        return redirect('trip_detail', id=review.trip.id)

    trip_id = review.trip.id
    review.delete()

    messages.success(request, "Review deleted.")
    return redirect('trip_detail', id=trip_id)





