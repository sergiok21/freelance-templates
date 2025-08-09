from typing import Any, TypeVar, List, Iterable
from django.db import models

from extensions.domain.entities.base import BaseEntity

_Model = TypeVar('_Model', bound=models.Model)
_Entity = TypeVar('_Entity', bound=BaseEntity)


def _dig(obj: Any, dotted: str) -> Any:
    for part in dotted.split("."):
        obj = getattr(obj, part)
        if obj is None:
            break
    return obj


def _one(model: _Model, entity_cls: type[_Entity]) -> _Entity:
    d: dict[str, Any] = {}
    for dst, src in entity_cls.mapper().items():
        if callable(src):
            d[dst] = src(getattr(model, dst))
        else:
            d[dst] = _dig(model, src)
    return entity_cls(**d)


def model_to_entity(
    obj: _Model | Iterable[_Model],
    *,
    entity_cls: type[_Entity],
) -> _Entity | List[_Entity]:

    if isinstance(obj, Iterable) and not isinstance(obj, models.Model):
        return [_one(m, entity_cls) for m in obj]

    return _one(obj, entity_cls)
