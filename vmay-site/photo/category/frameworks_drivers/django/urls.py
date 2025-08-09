from django.urls import path

from category.interface_adapters.controllers.views import CategoryListView

app_name = 'category'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
]
