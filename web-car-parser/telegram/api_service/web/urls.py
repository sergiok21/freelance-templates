from django.urls import path

from .views import TelegramAPIView

app_name = 'web'

urlpatterns = [
    path('api/telegram/', TelegramAPIView.as_view()),
]
