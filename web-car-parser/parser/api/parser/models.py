from typing import Dict, List

from api.parser.config import Locker


class ThreadObject:
    _instance = None

    def __new__(cls, *args, **kwargs):
        with Locker():
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._thread: Dict[str, str] = {}  # {thread_id: link}}
            self._initialized = True

    @property
    def thread(self):
        return self._thread

    @thread.setter
    def thread(self, value):
        self._thread = value


class UserObject:
    _instance = None

    def __new__(cls, *args, **kwargs):
        with Locker():
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._user: Dict[str, Dict[str, str]] = {}
            self._link: Dict[str, Dict[str, List[str]]] = {}
            self._initialized = True

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    def reset_key(self, new_key: str, old_key: str, obj_property=None):
        if not obj_property:
            obj_property = self.link
        if new_key not in obj_property:
            obj_property[new_key] = obj_property[old_key]
            del obj_property[old_key]

    def clear_empties_all(self):
        thread_model = ThreadObject()
        threads = {v: k for k, v in thread_model.thread.items()}

        link_keys = list(self.link.keys()).copy()
        for key in link_keys:
            if not self.link.get(key):
                del self.link[key]
                del thread_model.thread[threads.get(key)]

        user_keys = list(self.user.keys()).copy()
        for key in user_keys:
            if not self.user.get(key):
                del self.user[key]


class TargetDataObject:
    def __init__(self):
        self._data: Dict[str, int | str] = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
