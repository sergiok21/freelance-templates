from loguru import logger
from typing import Callable, Any


class Container:
    """
    DI-контейнер для реєстрації та виконання залежностей за ключем і типом.

    Основні можливості
    -----------------
    Реєстрація provider-функцій для залежностей (factory/fn).
    Отримання (resolve) залежностей за ключем і типом.
    Підтримка singleton або фабрик (через provider-функцію).
    Логування реєстрації та резолву для відладки.

    Examples
    --------
    >>> class MyRepo:
    ...     pass
    >>> Container.register('my_repo', MyRepo, lambda: MyRepo())
    >>> repo = Container.resolve('my_repo', MyRepo)
    """

    _providers: dict[tuple[Any, type], Callable[[], Any]] = {}

    @classmethod
    def register(cls, key: Any, iface: type, provider: Callable[[], Any]):
        logger.debug(f'[DI] Register: {key} for {iface.__name__} via {provider}')
        cls._providers[(key, iface)] = provider

    @classmethod
    def resolve(cls, key: Any, iface: type):
        logger.debug(f'[DI] Resolving: {key} as {iface.__name__}')
        try:
            obj = cls._providers[(key, iface)]()
            logger.debug(f'[DI] Resolved: {obj.__class__.__name__}')
            return obj
        except KeyError as exc:
            raise RuntimeError(f'No provider for {key=!r} / {iface}') from exc
