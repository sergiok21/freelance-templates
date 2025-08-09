import logging
import os

import requests
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status

from .models import Filter, User
from .serializers import FilterSerializer, UserSerializer

from common.views import PermissionMixin, CustomTokenAuthentication
from .processors.user import UserDataProcessor

logger = logging.getLogger(__name__)


class FilterView(UserDataProcessor, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            page_data = self.process_user_data(request, **kwargs)
            if page_data:
                return render(**{k: v for k, v in page_data.items()})
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


class FilterViewSet(UserDataProcessor, PermissionMixin, ModelViewSet):
    serializer_class = FilterSerializer
    authentication_classes = [CustomTokenAuthentication]

    def get_queryset(self):
        if self.request.META.get('HTTP_AUTHORIZATION') in [
            os.environ.get('PARSER_TOKEN_SERVICE'), os.environ.get('TELEGRAM_TOKEN_SERVICE')
        ]:
            user_id = self.request.META.get('HTTP_USER_ID')
            if user_id:
                return Filter.objects.filter(user__t_id=int(user_id))
            return Filter.objects.exclude(status=False)
        return Filter.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_AUTHORIZATION') in [
            os.environ.get('PARSER_TOKEN_SERVICE'), os.environ.get('TELEGRAM_TOKEN_SERVICE')
        ]:
            service = "Parser" \
                if self.request.META.get("HTTP_AUTHORIZATION") == os.environ.get("PARSER_TOKEN_SERVICE") \
                else "Telegram"
            logger.info(f'Get data into API by {service} service.')
            return super().list(request, *args, **kwargs)
        if not self.request.user or not self.request.user.id:
            return Response({'error': 'Does not authenticate'}, status=403)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(token=self.request.user.token)
            serializer = self.get_serializer(data=request.data)
            serializer.user_id = user.t_id
            if serializer.is_valid():
                try:
                    if request.method == 'POST':
                        serializer.clean(user=user, link=serializer.validated_data['link'])
                except ValidationError as ex:
                    logger.info(f'{ex.message} ({user.t_id})')
                    return Response({'errors': ex.message}, status=status.HTTP_400_BAD_REQUEST)
                return self._save_data(request=request, serializer=serializer, user=user)
            logger.critical(f'Bad request to create filter: {serializer.errors}')
            return Response({'error': 'Check your data.'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            logger.warning(f'User does not exist with token {self.request.user.token}')
            return Response({'error': 'Check your data.'}, status=status.HTTP_400_BAD_REQUEST)

    def _save_data(self, request, serializer, user):
        serializer.save(user=user)
        if self.is_started(request):
            logger.info(f'User bot {user.t_id} started')
            response_status = self._send_data_to_parser(serializer=serializer, t_id=user.t_id)
            if response_status != status.HTTP_200_OK:
                return Response({'errors': 'Service is not responding'}, status=response_status)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _send_data_to_parser(self, serializer, t_id):
        try:
            response = requests.post(
                url=f'{os.environ.get("PARSER_URL")}/api/parser/',
                headers={'Authorization': os.environ.get('WEB_TOKEN_SERVICE')},
                json={
                    'user_id': str(t_id),
                    'link': serializer.validated_data['link'],
                    'name': serializer.validated_data['name']
                },
            )
            if response.status_code == 200:
                logger.info(f'User data {t_id} was sent to parser')
                return response.status_code
            logger.critical(f'Data did not send to parser service. '
                            f'Status code - {response.status_code}')
            return response.status_code
        except requests.exceptions.ConnectionError or requests.exceptions.ConnectTimeout:
            logger.critical(f'Parser service does not work.')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id, link = instance.user.t_id, instance.link
            requests.delete(
                url=f'{os.environ.get("PARSER_URL")}/api/parser/',
                headers={'Authorization': os.environ.get('WEB_TOKEN_SERVICE')},
                json={'user_id': user_id, 'link': link},
            )
            self.perform_destroy(instance)
            logger.info(f'Data was destroyed for user {instance.user.t_id}. Name: {instance.name}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.error(f'Bad request to delete data: {ex}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(UserDataProcessor, PermissionMixin, APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'User was created with ID {serializer.data["t_id"]}')
            return Response(status=status.HTTP_201_CREATED)
        logger.warning(f'Bad request to create a user {request.data["t_id"]}: {serializer.errors}.')
        return Response({'error': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = User.objects.get(t_id=request.data.get('t_id'))
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        logger.warning(f'Bad request to update a user {user.t_id}: {serializer.errors}.')
        return Response({'error': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = User.objects.get(t_id=request.data.get('t_id'))
        user.token = None
        user.save()
        logger.info(f'Deleted user token {user.t_id}')
        return Response(status=status.HTTP_204_NO_CONTENT)
