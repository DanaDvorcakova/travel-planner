from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
from .views import CustomPasswordResetView

urlpatterns = [
    # Public
    path('', views.home, name='home'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Trips
    path('trip/add/', views.add_trip, name='add_trip'),
    path('trip/<int:id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:id>/edit/', views.edit_trip, name='edit_trip'),
    path('trip/<int:id>/delete/', views.delete_trip, name='delete_trip'),
    path('trip/<int:id>/toggle-publish/', views.toggle_publish_trip, name='toggle_publish_trip'),
    

    # Itinerary
    path('trip/<int:trip_id>/add-item/', views.add_itinerary_item, name='add_item'),
    path('item/<int:id>/edit/', views.edit_itinerary_item, name='edit_item'),
    path('item/<int:id>/delete/', views.delete_itinerary_item, name='delete_item'),
    path('trip/<int:trip_id>/planner/', views.itinerary_planner, name='planner'),

    # Saved Places
    path('places/', views.saved_places, name='saved_places'),
    path('places/add/', views.add_saved_place, name='add_saved_place'),
    path('places/<int:id>/delete/', views.delete_saved_place, name='delete_place'),

    # Search + Save
    path('search-places/', views.search_places, name='search_places'),
    path('places/save/', views.save_place_ajax, name='save_place_ajax'),
    path('add-place-to-trip-ajax/', views.add_place_to_trip_ajax, name='add_place_to_trip_ajax'),

    # Reviews
    path('trip/<int:id>/review/', views.add_review, name='add_review'),
    path('review/<int:id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:id>/delete/', views.delete_review, name='delete_review'),

    # Password Reset
    path("accounts/password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
]