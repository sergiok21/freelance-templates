from typing import Iterable

import pytest

from pkg.application.services.crud import GetAllRepositoryService
from pkg.frameworks_drivers.di import DIRegister
from pkg.interface_adapters.di.provider import inject
from pkg.tests.fakes import FakeReadRepository, FakeEntity


def base_register():
    test_read_repository_name = 'test:read_repo'
    category_read_repo, category_read_repo_factory = FakeReadRepository, lambda: FakeReadRepository()

    category_repositories = {
        test_read_repository_name: (category_read_repo, category_read_repo_factory),
    }

    category_depends = {
        'test:get_all': (GetAllRepositoryService, category_read_repo_factory),
    }

    DIRegister.repository_register(category_repositories)
    DIRegister.service_repository_register(category_depends)


def test_valid_register():
    @inject
    def func(service: GetAllRepositoryService = 'test:get_all') -> Iterable[FakeEntity]:
        return service()

    base_register()

    result = func()

    assert isinstance(result, list)
    assert isinstance(result[0], FakeEntity)
    assert result[0].number == 1


def test_invalid_register():
    @inject
    def func(service: GetAllRepositoryService = 'test1:get_all') -> Iterable[FakeEntity]:
        return service()

    base_register()

    with pytest.raises(TypeError):
        func()


def test_missed_repository_factory():
    test_read_repository_name = 'test:read_repo'
    category_read_repo = FakeReadRepository

    category_repositories = {
        test_read_repository_name: (category_read_repo,),
    }

    with pytest.raises(ValueError):
        DIRegister.repository_register(category_repositories)

    category_repositories = {
        test_read_repository_name: (None, category_read_repo),
    }

    with pytest.raises(AttributeError):
        DIRegister.repository_register(category_repositories)


def test_missed_service():
    category_read_repo_factory = lambda: FakeReadRepository()

    category_depends = {
        'test:get_all': (category_read_repo_factory, ),
    }

    with pytest.raises(ValueError):
        DIRegister.service_repository_register(category_depends)

    category_depends = {
        'test:get_all': (None, category_read_repo_factory),
    }

    with pytest.raises(AttributeError):
        DIRegister.service_repository_register(category_depends)
