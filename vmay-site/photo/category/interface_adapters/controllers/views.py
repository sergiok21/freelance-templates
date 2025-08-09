from django.views.generic import ListView

from extensions.interface_adapters.controllers.decorators.cache import cache_category
from extensions.interface_adapters.controllers.mixins import TitleMixin
from pkg.application.services.crud import GetAllRepositoryService
from pkg.interface_adapters.di.provider import inject


@cache_category
class CategoryListView(TitleMixin, ListView):
    template_name = 'category/categories.html'
    title = 'vmay - Категорії'

    @inject
    def get_queryset(self, service: GetAllRepositoryService = 'category:get_all'):
        return service()
