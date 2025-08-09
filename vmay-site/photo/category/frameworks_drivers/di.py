from category.interface_adapters.gateways.repositories.category_repo import CategoryReadRepository
from extensions.frameworks_drivers.di import auto_di_register
from pkg.application.services.crud import GetAllRepositoryService, GetByFieldRepositoryService
from pkg.frameworks_drivers.di.register import DIRegister


category_read_repo_factory = lambda: CategoryReadRepository()

category_repo_depends = [
    ('category:read_repo', CategoryReadRepository, category_read_repo_factory),
]
category_service_depends = [
    ('category:get_all', GetAllRepositoryService, category_read_repo_factory),
    ('category:get_by_fields', GetByFieldRepositoryService, category_read_repo_factory),
]

auto_di_register(category_repo_depends, DIRegister.repository_register)
auto_di_register(category_service_depends, DIRegister.service_repository_register)
