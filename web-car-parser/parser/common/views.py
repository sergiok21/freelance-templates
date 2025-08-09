import os

from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class PermissionMixin:
    def get_permissions(self):
        request: HttpRequest = self.request
        if request.META.get('HTTP_AUTHORIZATION') in [
            os.environ.get('TELEGRAM_TOKEN_SERVICE'), os.environ.get('WEB_TOKEN_SERVICE'), os.environ.get('ADMIN_TOKEN')
        ]:
            return [AllowAny()]
        return [IsAuthenticatedOrReadOnly()]
