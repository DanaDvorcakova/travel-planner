from django.contrib import admin
from .models import Trip, Profile, SavedPlace, ItineraryItem, Review


# =========================
# PROFILE
# =========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'travel_style')
    search_fields = ('user__username', 'travel_style')

# =========================
# TRIP
# =========================
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'start_date', 'end_date', 'is_published')
    search_fields = ('title', 'destination', 'user__username')
    list_filter = ('is_published', 'start_date')

# =========================
# SAVED PLACE
# =========================
@admin.register(SavedPlace)
class SavedPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'created_at')
    search_fields = ('name', 'location', 'user__username')

# =========================
# ITINERARY ITEM
# =========================
@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'trip', 'date', 'location')
    search_fields = ('title', 'location', 'trip__title')

# =========================
# REVIEW
# =========================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'rating', 'created_at')
    search_fields = ('user__username', 'trip__title', 'comment')
    list_filter = ('rating',)