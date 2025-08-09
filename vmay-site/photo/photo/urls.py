import os
from distutils.util import strtobool

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .settings import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.frameworks_drivers.django.urls', namespace='home')),
    path('', include('portfolio.frameworks_drivers.django.urls.default', namespace='portfolio')),
    path('', include('category.frameworks_drivers.django.urls', namespace='category')),
    path('', include('condition.frameworks_drivers.django.urls', namespace='condition')),
    path('', include('contact.frameworks_drivers.django.urls', namespace='contact')),
]

if strtobool(os.getenv('DEBUG', 'False')):
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
