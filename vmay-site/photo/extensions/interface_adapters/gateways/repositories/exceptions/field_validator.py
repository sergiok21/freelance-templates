from functools import wraps
from typing import Callable, ParamSpec, TypeVar
from django.db import models

P = ParamSpec('P')
T = TypeVar('T')


class InvalidModelFieldError(ValueError):
    def __init__(self, model: type['models.Model'], field: str) -> None:
        super().__init__(f'Field {field!r} does not exist in model: {model.__name__}')
        self.model = model
        self.field = field


def validate_fields(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        self = args[0]
        model: type[models.Model] = self.model

        allowed = {f.name for f in model._meta.get_fields()}
        for key in kwargs:
            if key not in allowed:
                raise InvalidModelFieldError(model, key)

        return func(*args, **kwargs)
    return wrapper
