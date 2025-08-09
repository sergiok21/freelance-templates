from django.contrib.auth.backends import ModelBackend

from .models import User


class TokenBackend(ModelBackend):
    def authenticate(self, request, token=None, **kwargs):
        if token is not None:
            try:
                user = User.objects.get(token=token)
                return user
            except User.DoesNotExist:
                return None
        return None
