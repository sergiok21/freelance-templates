from django.urls import path, include

urlpatterns = [
    path('', include('api.urls', namespace='api')),
]
