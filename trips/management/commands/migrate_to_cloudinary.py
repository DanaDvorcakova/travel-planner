from django.core.management.base import BaseCommand
from trips.models import Profile, Trip, SavedPlace, Place

class Command(BaseCommand):
    help = "Upload all images from local storage to Cloudinary"

    def handle(self, *args, **kwargs):
        models_with_images = [Profile, Trip, SavedPlace, Place]

        for model in models_with_images:
            # Get all ImageFields in this model
            image_fields = [f.name for f in model._meta.fields if f.get_internal_type() == 'ImageField']

            for obj in model.objects.all():
                for field_name in image_fields:
                    image_field = getattr(obj, field_name)
                    if image_field:
                        obj.save()  # triggers Cloudinary upload
                        self.stdout.write(f"Uploaded {model.__name__}.{field_name} for object {obj.pk}")

        self.stdout.write(self.style.SUCCESS("All images uploaded to Cloudinary!"))