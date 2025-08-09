from typing import Generic, TypeVar, Callable, Any, Dict
from django.db.models import Model

from extensions.domain.entities.base import BaseEntity
from extensions.interface_adapters.gateways.mappers.model_convertor import model_to_entity

_Model = TypeVar('_Model', bound=Model)
_Entity = TypeVar('_Entity', bound=BaseEntity)


class BaseCRUDRepository(Generic[_Model, _Entity]):
    model: type[_Model] = None
    entity: type[_Entity] = None
    map_to_entity: Callable = model_to_entity

    def __init__(
            self,
            model: type[_Model] = None,
            entity: type[_Entity] = None,
            map_to_entity: Callable = None,
    ) -> None:
        self.model = model or getattr(self, 'model', None)
        self.entity = entity or getattr(self, 'entity', None)
        self.map_to_entity = map_to_entity or getattr(type(self), 'map_to_entity', model_to_entity)

        assert self.model is not None, 'You must set "model" in constructor or class attribute'
        assert self.entity is not None, 'You must set "entity" in constructor or class attribute'

    def is_exists(self, **fields: Dict[str, Any]) -> bool:
        return self.model.objects.filter(**fields).exists()
