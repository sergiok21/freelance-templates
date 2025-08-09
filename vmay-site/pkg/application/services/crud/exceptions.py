from functools import wraps
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec('P')
T = TypeVar('T')


def is_missed_kwargs(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if not kwargs:
            raise TypeError('execute() requires at least one keyword argument')
        return func(*args, **kwargs)
    return wrapper
