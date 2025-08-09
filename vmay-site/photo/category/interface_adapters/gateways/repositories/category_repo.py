from category.domain.entities.category_entity import CategoryEntity
from category.interface_adapters.gateways.models import Category
from extensions.interface_adapters.gateways.repositories.crud import DjangoReadRepository


class CategoryReadRepository(DjangoReadRepository[Category, CategoryEntity]):
    model = Category
    entity = CategoryEntity
