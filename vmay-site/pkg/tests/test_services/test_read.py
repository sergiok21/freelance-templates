import pytest

from pkg.application.services.crud import (
    GetAllRepositoryService,
    GetByIdRepositoryService,
    GetByFieldRepositoryService,
    FilterByFieldRepositoryService
)
from pkg.tests.fakes import FakeReadRepository, FakeEntity


def test_get_all():
    repo = FakeReadRepository()
    service = GetAllRepositoryService(repo)
    result = service.execute()

    assert isinstance(result, list)
    assert isinstance(result[0], FakeEntity)
    assert result[0].number == 1


def test_get_by_id():
    repo = FakeReadRepository()
    service = GetByIdRepositoryService(repo)
    with pytest.raises(TypeError):
        service.execute()

    result = service.execute(1)

    assert isinstance(result, FakeEntity)
    assert result.number == 1


def test_get_by_fields():
    repo = FakeReadRepository()
    service = GetByFieldRepositoryService(repo)

    with pytest.raises(TypeError) as ex:
        service.execute()
    assert str(ex.value) == 'execute() requires at least one keyword argument'

    result = service.execute(number=1)

    assert isinstance(result, FakeEntity)
    assert result.number == 1


def test_filter_by_fields():
    repo = FakeReadRepository()
    service = FilterByFieldRepositoryService(repo)

    with pytest.raises(TypeError) as ex:
        service.execute()
    assert str(ex.value) == 'execute() requires at least one keyword argument'

    result = service.execute(number=1)

    assert isinstance(result, list)
    assert isinstance(result[0], FakeEntity)
    assert result[0].number == 1
