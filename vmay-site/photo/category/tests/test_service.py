from category.tests.fakes import fake_category_entity, FakeCategoryReadRepository
from extensions.application.services.crud.read import DjangoGetByPkRepositoryService


def test_category_get_by_pk():
    entity = fake_category_entity()
    repo = FakeCategoryReadRepository()
    service = DjangoGetByPkRepositoryService(repo)

    output = service.execute(1)

    assert isinstance(output, type(entity))
