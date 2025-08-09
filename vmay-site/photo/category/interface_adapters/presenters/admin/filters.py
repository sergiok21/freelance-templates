from django.contrib.admin import SimpleListFilter


class HasCategoryFilter(SimpleListFilter):
    title = 'Наявність категорії'
    parameter_name = 'has_category'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Є категорія'),
            ('no', 'Без категорії'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(category__isnull=False)
        if self.value() == 'no':
            return queryset.filter(category__isnull=True)
        return queryset


class CategoryFilter(SimpleListFilter):
    title = 'Категорія'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        from category.interface_adapters.gateways.models import Category
        return [(cat.id, cat.name) for cat in Category.objects.all()]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(category__id=value)
        return queryset
