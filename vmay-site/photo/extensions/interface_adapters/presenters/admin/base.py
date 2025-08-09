from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from extensions.interface_adapters.presenters.admin.forms import SimpleUrlFieldAdmin
from extensions.interface_adapters.presenters.mixins.pagination import BaseAdminPagination


class BaseAdmin(BaseAdminPagination, SimpleUrlFieldAdmin, admin.ModelAdmin):
    labels: dict[str, str] = {}

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        for field, label in self.labels.items():
            if field in self.list_display:
                self._patch_short_description(field, label)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field, label in self.labels.items():
            if field in form.base_fields:
                form.base_fields[field].label = _(label)
        return form

    def _patch_short_description(self, field: str, label: str) -> None:
        """
        Якщо `field` — атрибут моделі -> ставимо verbose_name.
        Якщо `field` — метод / callable -> перезаписуємо short_description.
        """
        attr = getattr(self, field, None) or getattr(self.model, field, None)
        if attr is None:
            return

        trans_label = _(label)

        # метод / функція
        if callable(attr):
            attr.short_description = trans_label
        # поле моделі
        elif hasattr(attr, 'field') and hasattr(attr.field, 'verbose_name'):
            attr.field.verbose_name = trans_label
