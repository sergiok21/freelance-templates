from functools import wraps
from typing import ParamSpec, TypeVar, Callable

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, FieldError

P = ParamSpec('P')
T = TypeVar('T')


def get_mtd_exception(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as ex:
            raise ObjectDoesNotExist(f'Object does not exist! Exception: "{ex}"')
    return wrapper


def related_field_exception(func: Callable[P, T]) -> Callable[P, T]:
    """TODO: implement method"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except FieldError as ex:
            raise FieldError(f'Field(-s) does not exist. Exception: {ex}')
    return wrapper
