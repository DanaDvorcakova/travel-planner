from django.core.management.base import BaseCommand
from trips.models import Trip, SavedPlace
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Upload existing images to Cloudinary'

    def handle(self, *args, **kwargs):
        for obj in Trip.objects.all():
            if obj.image and not str(obj.image.url).startswith("http"):
                obj.image = File(open(obj.image.path, 'rb'))
                obj.save()
                self.stdout.write(f"Uploaded Trip {obj.title} to Cloudinary")

        for obj in SavedPlace.objects.all():
            if obj.image and not str(obj.image.url).startswith("http"):
                obj.image = File(open(obj.image.path, 'rb'))
                obj.save()
                self.stdout.write(f"Uploaded SavedPlace {obj.name} to Cloudinary")