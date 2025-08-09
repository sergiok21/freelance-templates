from dataclasses import dataclass
from django.http import HttpRequest
from django.utils.cache import get_cache_key


@dataclass(frozen=True)
class RequestMeta:
    SERVER_NAME: str
    SERVER_PORT: str


class CacheExtension:
    def __init__(self, path: str):
        self._req = HttpRequest()
        self._req.method = 'GET'
        self._req.path = path
        self._req.META = RequestMeta().__dict__

    def get_key_by_prefix(self, key_prefix: str):
        return get_cache_key(self._req, key_prefix=key_prefix)
