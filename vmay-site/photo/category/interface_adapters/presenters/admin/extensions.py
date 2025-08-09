class CategoryPreview:
    def show_category(self, obj):
        return obj.category.name if obj.category else "-"
    show_category.short_description = "Категорія"
