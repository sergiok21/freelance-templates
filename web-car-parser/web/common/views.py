import os

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from interface.models import User


class PermissionMixin:
    def get_permissions(self):
        if self.request.META.get('HTTP_AUTHORIZATION') in [
            os.environ.get('PARSER_TOKEN_SERVICE'),
            os.environ.get('TELEGRAM_TOKEN_SERVICE'),
            os.environ.get('ADMIN_TOKEN')
        ] or self.request.user or self.request.user.is_superuser:
            return [AllowAny()]
        return [IsAuthenticatedOrReadOnly()]


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            if token in [
                os.environ.get('PARSER_TOKEN_SERVICE'),
                os.environ.get('TELEGRAM_TOKEN_SERVICE'),
                os.environ.get('ADMIN_TOKEN')
            ]:
                return None, None
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return user, None
