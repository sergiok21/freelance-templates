from typing import Any, TypeVar, Iterable, Dict

from extensions.application.ports.crud import DjangoReadRepositoryPort
from extensions.domain.entities.base import BaseEntity

from extensions.interface_adapters.gateways.repositories.exceptions.get_exception import get_mtd_exception, \
    related_field_exception
from extensions.interface_adapters.gateways.repositories.crud.base import BaseCRUDRepository

from django.db.models import Model

_Model = TypeVar('_Model', bound=Model)
_Entity = TypeVar('_Entity', bound=BaseEntity)


class DjangoReadRepository(
    BaseCRUDRepository[_Model, _Entity],
    DjangoReadRepositoryPort[_Entity],
):
    def get_all(self) -> Iterable[_Model]:
        objects = self.model.objects.all()
        return [
            self.map_to_entity(obj=obj, entity_cls=self.entity)
            for obj in objects
        ]

    @get_mtd_exception
    def get_by_id(self, id_: int) -> _Entity:
        obj = self.model.objects.get(id=id_)
        return self.map_to_entity(obj=obj, entity_cls=self.entity)

    @get_mtd_exception
    def get_by_pk(self, pk: int) -> _Entity:
        obj = self.model.objects.get(pk=pk)
        return self.map_to_entity(obj=obj, entity_cls=self.entity)

    @get_mtd_exception
    def get_by_fields(self, **fields: Dict[str, Any]) -> _Entity:
        obj = self.model.objects.get(**fields)
        return self.map_to_entity(obj=obj, entity_cls=self.entity)

    def filter_by_fields(self, **filters: Any) -> Iterable[_Entity]:
        objects = self.model.objects.filter(**filters)
        return [
            self.map_to_entity(obj=obj, entity_cls=self.entity)
            for obj in objects
        ]

    @related_field_exception
    def select_related(self, fields: Iterable[str]) -> Iterable[_Entity]:
        objects = self.model.objects.select_related(*fields)
        return [
            self.map_to_entity(obj=obj, entity_cls=self.entity)
            for obj in objects
        ]

    @related_field_exception
    def select_related_filter(self, fields, **filters: Any) -> Iterable[_Entity]:
        objects = self.model.objects.select_related(*fields)
        if filters:
            objects = objects.filter(**filters)
        return [
            self.map_to_entity(obj=obj, entity_cls=self.entity)
            for obj in objects
        ]

    @related_field_exception
    def prefetch_related(self, fields: Iterable[str]) -> Iterable[_Entity]:
        objects = self.model.objects.prefetch_related(*fields)
        return [
            self.map_to_entity(obj=obj, entity_cls=self.entity)
            for obj in objects
        ]

    @related_field_exception
    def prefetch_related_filter(self, fields, **filters: Any) -> Iterable[_Entity]:
        objects = self.model.objects.prefetch_related(*fields)
        if filters:
            objects = objects.filter(**filters)
        return [
            self.map_to_entity(obj=obj, entity_cls=self.entity)
            for obj in objects
        ]
