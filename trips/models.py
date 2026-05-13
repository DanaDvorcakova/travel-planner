from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# =========================
# PROFILE
# =========================
class Profile(models.Model):

    ROLE_CHOICES = [
        ('traveler', 'Traveler'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    travel_style = models.CharField(
        max_length=100,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='traveler'
    )

    def __str__(self):
        return f"{self.user.username} Profile"


# =========================
# AUTO CREATE PROFILE
# =========================
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# =========================
# TRIP
# =========================
class Trip(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='trips'
    )
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='trips/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.destination})"

    @property
    def average_rating(self):
        from django.db.models import Avg
        review_stats = self.reviews.aggregate(avg_rating=Avg('rating'))
        return float(review_stats['avg_rating'] or 0)


# =========================
# SAVED PLACE
# =========================
class SavedPlace(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_places'
    )

    name = models.CharField(max_length=200)

    location = models.CharField(
        max_length=200,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='places/',
        blank=True,
        null=True
    )

    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# =========================
# ITINERARY ITEM
# =========================
class ItineraryItem(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='itinerary'
    )

    title = models.CharField(max_length=200)

    location = models.CharField(
        max_length=200,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    date = models.DateField()

    time = models.TimeField(
        blank=True,
        null=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.trip.title} - {self.title}"

    def save(self, *args, **kwargs):

        if (
            self.location and
            (
                self.latitude is None or
                self.longitude is None
            )
        ):
            try:
                from .services.maps import get_coordinates

                lat, lon = get_coordinates(self.location)

                if lat is not None and lon is not None:
                    self.latitude = lat
                    self.longitude = lon

            except Exception as e:
                print("Geocoding error:", e)

        super().save(*args, **kwargs)


# =========================
# REVIEW
# =========================
class Review(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    comment = models.TextField()

    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trip', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.trip.title} ({self.rating}★)"



class Place(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='places/')