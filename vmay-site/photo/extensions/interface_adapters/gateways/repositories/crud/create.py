from typing import Any, TypeVar, Dict

from django.db.models import Model

from extensions.application.ports.crud import DjangoCreateRepositoryPort
from extensions.domain.entities.base import BaseEntity

from extensions.interface_adapters.gateways.repositories.crud.base import BaseCRUDRepository

_Model = TypeVar('_Model', bound=Model)
_Entity = TypeVar('_Entity', bound=BaseEntity)


class DjangoCreateRepository(
    BaseCRUDRepository[_Model, _Entity],
    DjangoCreateRepositoryPort[_Entity],
):
    def create(self, **fields: Dict[str, Any]) -> _Entity:
        obj = self.model.objects.create(**fields)
        return self.map_to_entity(obj=obj, entity_cls=self.entity)
