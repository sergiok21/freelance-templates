from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.urls import reverse

from category.interface_adapters.gateways.models import Category
from extensions.frameworks_drivers.django.signals import CacheExtension


@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    path = reverse('category:categories')
    cache_ext = CacheExtension(path=path)
    key = cache_ext.get_key_by_prefix(key_prefix='category_page')
    if key:
        cache.delete(key)
