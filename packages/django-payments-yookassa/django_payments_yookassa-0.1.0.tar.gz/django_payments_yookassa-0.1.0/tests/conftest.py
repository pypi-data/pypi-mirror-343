import os
import django

# Configure Django settings before django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.django_settings")

# Setup Django
django.setup() 