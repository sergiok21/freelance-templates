from django.contrib import admin

from category.interface_adapters.gateways.models import Category
from extensions.interface_adapters.presenters.admin import BaseAdmin


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    fields = ['...']
    labels = {
        'name': 'Назва',
        ...: ...
    }
