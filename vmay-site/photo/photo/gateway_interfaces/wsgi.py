import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'photo.settings.{os.getenv("DJANGO_MODE", "dev")}')

application = get_wsgi_application()
