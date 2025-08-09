from typing import TypeVar, Any, Iterable, Generic

from pkg.application.ports import ReadRepositoryPort
from pkg.application.services.crud.base import BaseRepositoryService
from pkg.application.services.crud.exceptions import is_missed_kwargs

_Entity = TypeVar('_Entity')
_Repository = TypeVar('_Repository', bound=ReadRepositoryPort)


class GetAllRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository]
):
    """
    Summary of what the class does.

    Detailed description of the class, its purpose, and usage.
    This class is a generic implementation of a repository service that retrieves all entities.
    It extends BaseRepositoryService and uses a generic type for both the entity and the repository.

    :ivar _Entity: Generic type representing the entity.
    :type _Entity: Type
    :ivar _Repository: Generic type representing the repository.
    :type _Repository: Type
    """
    def execute(self) -> Iterable[_Entity]:
        return self.repository.get_all()


class GetByIdRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository]
):
    """
    Summary of what the class does.

    Detailed description of the class, its purpose, and usage.
    This class is a generic implementation of a repository service that retrieves an entity by its ID.
    It extends BaseRepositoryService and uses a generic type for both the entity and the repository.

    :ivar _Entity: Generic type representing the entity.
    :type _Entity: Type
    :ivar _Repository: Generic type representing the repository.
    :type _Repository: Type
    """
    def execute(self, id_: int) -> _Entity:
        return self.repository.get_by_id(id_)


class GetByFieldRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository]
):
    """
    Summary of what the class does.

    Detailed description of the class, its purpose, and usage.
    This class is a generic implementation of a repository service that retrieves an entity by one or more field values.
    It extends BaseRepositoryService and uses a generic type for both the entity and the repository.
    The `execute` method requires at least one keyword argument representing the fields to filter by.

    :ivar _Entity: Generic type representing the entity.
    :type _Entity: Type
    :ivar _Repository: Generic type representing the repository.
    :type _Repository: Type
    """
    @is_missed_kwargs
    def execute(self, **kwargs: Any) -> _Entity:
        return self.repository.get_by_fields(**kwargs)


class FilterByFieldRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository]
):
    """
    Summary of what the class does.

    Detailed description of the class, its purpose, and usage.
    This class is a generic implementation of a repository service that filters entities by one or more field values.
    It extends BaseRepositoryService and uses a generic type for both the entity and the repository.
    The `execute` method requires at least one keyword argument representing the fields to filter by.

    :ivar _Entity: Generic type representing the entity.
    :type _Entity: Type
    :ivar _Repository: Generic type representing the repository.
    :type _Repository: Type
    """
    @is_missed_kwargs
    def execute(self, **kwargs: Any) -> Iterable[_Entity]:
        return self.repository.filter_by_fields(**kwargs)
