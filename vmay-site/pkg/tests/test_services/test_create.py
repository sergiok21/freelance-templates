import pytest

from pkg.application.services.crud.create import CreateRepositoryService
from pkg.tests.fakes import FakeCreateRepository, FakeEntity


def test_create():
    repo = FakeCreateRepository()
    service = CreateRepositoryService(repo)

    with pytest.raises(TypeError) as ex:
        service.execute()
    assert str(ex.value) != 'error'
    assert str(ex.value) == 'execute() requires at least one keyword argument'

    result = service.execute(number=1, text='text')

    assert isinstance(result, FakeEntity)
    assert result.number == 1
    assert result.text == 'text'
