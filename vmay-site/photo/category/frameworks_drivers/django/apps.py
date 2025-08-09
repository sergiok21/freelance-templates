from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from extensions.frameworks_drivers.django.base_app import BaseAppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'
    verbose_name = _('Категорії')
    path = BaseAppConfig.get_path(__file__)

    def ready(self):
        import category.interface_adapters.presenters.admin

        import category.frameworks_drivers.di
        import category.frameworks_drivers.django.signals
