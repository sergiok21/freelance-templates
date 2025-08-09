from dataclasses import dataclass
from typing import Iterable, Dict, Any

from pkg.application.ports import ReadRepositoryPort
from pkg.application.ports.crud import CreateRepositoryPort


@dataclass
class FakeEntity:
    number: int = 0
    text: str = ''


class FakeReadRepository(ReadRepositoryPort[FakeEntity]):
    def get_all(self) -> Iterable[FakeEntity]:
        return [FakeEntity(number=1, text='text')]

    def get_by_id(self, id_: int) -> FakeEntity:
        return FakeEntity(number=1, text='text')

    def get_by_fields(self, **fields: Dict[str, Any]) -> FakeEntity:
        return FakeEntity(number=1, text='text')

    def filter_by_fields(self, **filters: Any) -> Iterable[FakeEntity]:
        return [FakeEntity(number=1, text='text')]


class FakeCreateRepository(CreateRepositoryPort[FakeEntity]):
    def create(self, **fields: Dict[str, Any]) -> FakeEntity:
        return FakeEntity(number=1, text='text')
