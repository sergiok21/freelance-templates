from django.db import models

from extensions.interface_adapters.gateways.mixins.models import DeleteOldImageModelMixin


class Category(models.Model, DeleteOldImageModelMixin):
    name = models.CharField(max_length=128, unique=True, help_text='Назва послуги')
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='category-images')
    description = models.TextField(help_text='Що входить до послуги')
    slug = models.SlugField(max_length=128, unique=True, help_text="individual, love-story, family...")

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id']

    def __str__(self):
        return f'Категорія: {self.name} | Ціна: {self.price}'
