from typing import TypeVar, Generic, Iterable, Dict, Any

from extensions.application.ports.crud import DjangoReadRepositoryPort
from extensions.domain.entities.base import BaseEntity
from pkg.application.services.crud.base import BaseRepositoryService

_Entity = TypeVar('_Entity', bound=BaseEntity)
_Repository = TypeVar('_Repository', bound=DjangoReadRepositoryPort)


class DjangoGetByPkRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository],
):
    def execute(self, pk: int) -> Iterable[_Entity]:
        return self.repository.get_by_pk(pk)


class DjangoSelectRelatedRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository],
):
    def execute(self, fields: Iterable[str]) -> Iterable[_Entity]:
        return self.repository.select_related(fields)


class DjangoSelectRelatedFilterRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository],
):
    def execute(self, fields: Iterable[str], **filters: Dict[str, Any]) -> Iterable[_Entity]:
        return self.repository.select_related_filter(fields, **filters)


class DjangoPrefetchRelatedRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository]
):
    def execute(self, fields: Iterable[str]) -> Iterable[_Entity]:
        return self.repository.prefetch_related(fields)


class DjangoPrefetchRelatedFilterRepositoryService(
    Generic[_Entity, _Repository],
    BaseRepositoryService[_Entity, _Repository],
):
    def execute(self, fields: Iterable[str], **filters: Dict[str, Any]) -> Iterable[_Entity]:
        return self.repository.prefetch_related_filter(fields, **filters)
