from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

_Entity = TypeVar('_Entity')
_Repository = TypeVar('_Repository')


class BaseRepositoryService(Generic[_Entity, _Repository], ABC):
    def __init__(self, repository: _Repository) -> None:
        self.repository = repository

    def __call__(self, *args: Any, **kwargs: Any) -> _Entity:
        return self.execute(*args, **kwargs)

    @abstractmethod
    def execute(self, *args, **kwargs: Any) -> _Entity:
        raise NotImplementedError
