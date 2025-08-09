from typing import Dict, Callable, Tuple

from pkg.interface_adapters.di.container import Container


class DIRegister:
    """
    Клас для реєстрації залежностей у DI-контейнері.

    Методи
    --------
    repository_register(depends) - Реєстрація фабрик або інстансів репозиторіїв у контейнері.
    service_repository_register(depends) - Реєстрація сервісів з інʼєкцією потрібних репозиторіїв у контейнері.
    depends_factory(related_name, cls_type, factory) - Формування залежностей, повернення словника.
    Examples
    --------
    >>> from pkg.frameworks_drivers.di import DIRegister
    >>> DIRegister.repository_register({
    ...     'my_repo': (MyRepo, lambda: MyRepo())
    ... })
    >>> DIRegister.service_repository_register({
    ...     'my_service': (MyService, lambda: MyRepo())
    ... })
    >>> DIRegister.depends_factory(
    ... 'name', MyService, lambda: MyRepo()
    ... )
    """
    @classmethod
    def depends_factory(
            cls,
            related_name: str,
            cls_type: Callable,
            factory: Callable,
    ) -> Dict[str, Tuple[Callable, Callable]]:
        return {
            related_name: (cls_type, factory)
        }

    @classmethod
    def repository_register(
            cls,
            depends: Dict[str, Tuple[type, Callable]],
    ) -> None:

        for related_name, (repo_link, repo_factory) in depends.items():
            Container.register(
                related_name,
                repo_link,
                repo_factory
            )

    @classmethod
    def service_repository_register(
            cls,
            depends: Dict[str, Tuple[type, Callable]]
    ) -> None:

        for related_name, (service_cls, repository_factory) in depends.items():
            Container.register(
                related_name,
                service_cls,
                lambda s_cls=service_cls, r_factory=repository_factory: s_cls(r_factory())
            )
