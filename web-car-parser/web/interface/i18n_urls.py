from django.urls import path

from .views import FilterView

app_name = 'interface'

urlpatterns = [
    path('<str:page>/', FilterView.as_view(), name='home'),
    path('filter/<int:filter_id>/', FilterView.as_view(), name='current_filter'),
]
