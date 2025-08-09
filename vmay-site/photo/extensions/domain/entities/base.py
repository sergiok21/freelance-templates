from abc import ABC
from dataclasses import fields
from typing import Callable, Any

FieldMap = dict[str, str | Callable[[Any], Any]]


class BaseEntity(ABC):
    """Базова сутність з автогенерацією mapper() за metadata['src']."""

    @classmethod
    def mapper(cls) -> FieldMap:
        mapping: FieldMap = {}
        for f in fields(cls):
            src = f.metadata.get("src", f.name)
            mapping[f.name] = src
        return mapping
