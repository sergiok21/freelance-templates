from functools import wraps
from inspect import signature, Parameter

from pkg.interface_adapters.di.container import Container


def inject(func):
    """
    Декоратор для автоматичної інʼєкції залежностей у функцію.

    Parameters
    ----------
    func : Callable
        Функція, у яку потрібно інʼєктувати залежності.

    Returns
    -------
    Callable
        Функція-обгортка з автоматичною інʼєкцією залежностей.

    Examples
    --------
    >>> @inject
    ... def my_func(service: MyService = 'my_service'):
    ...     service.do_something()
    """

    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)

        for name, param in sig.parameters.items():
            if name in bound.arguments:
                continue

            iface = param.annotation
            if iface is Parameter.empty:
                continue

            key = (
                param.default
                if param.default is not Parameter.empty
                else iface
            )

            try:
                bound.arguments[name] = Container.resolve(key, iface)
            except RuntimeError:
                pass

        return func(*bound.args, **bound.kwargs)
    return wrapper
