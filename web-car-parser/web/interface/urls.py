from django.urls import path, include
from rest_framework import routers

from .views import FilterViewSet, UserAPIView

app_name = 'interface'

router = routers.DefaultRouter()
router.register(r'filters', FilterViewSet, basename='filters')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/user/', UserAPIView.as_view(), name='user'),
]
