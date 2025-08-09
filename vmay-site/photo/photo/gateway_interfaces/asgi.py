import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'photo.settings.{os.getenv("DJANGO_MODE", "dev")}')

application = get_asgi_application()
