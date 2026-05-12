import os
import django
from django.contrib.auth import get_user_model

# Setup Django if running as a standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

User = get_user_model()

# Read credentials from environment variables
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Password123")

# Create or update the admin user
user, created = User.objects.get_or_create(
    username=ADMIN_USERNAME,
    defaults={"email": ADMIN_EMAIL}
)

# Always set the password (safe even if user exists)
user.set_password(ADMIN_PASSWORD)
user.is_staff = True
user.is_superuser = True
user.save()

if created:
    print(f"Admin user '{ADMIN_USERNAME}' created.")
else:
    print(f"Admin user '{ADMIN_USERNAME}' exists. Password updated.")