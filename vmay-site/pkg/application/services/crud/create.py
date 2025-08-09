from typing import TypeVar, Any, Generic

from pkg.application.ports.crud import CreateRepositoryPort
from pkg.application.services.crud.base import BaseRepositoryService
from pkg.application.services.crud.exceptions import is_missed_kwargs

_Entity = TypeVar('_Entity')
_Repository = TypeVar('_Repository', bound=CreateRepositoryPort)


class CreateRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository]
):
    @is_missed_kwargs
    def execute(self, **kwargs: Any) -> _Entity:
        return self.repository.create(**kwargs)
