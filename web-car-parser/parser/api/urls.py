from django.urls import path, re_path

from api.views import ParserAPIView, StatusAPIView

app_name = 'api'

urlpatterns = [
    path('api/parser/', ParserAPIView.as_view(), name='parser'),
    re_path(r'^api/parser/status(?:/(?P<user_id>\w+))?/', StatusAPIView.as_view(), name='status'),
]
