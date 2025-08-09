from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.manager import RequestManager, ThreadManager
from api.parser.models import UserObject, ThreadObject
from api.serializers import StatusSerializer, ParserSerializer
from common.views import PermissionMixin


class ParserAPIView(PermissionMixin, RequestManager, APIView):
    def post(self, request: Request):
        serializer = ParserSerializer(data=request.data)
        if serializer.is_valid():
            self.thread.start_thread(**serializer.data)
            return Response({'status': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        serializer = ParserSerializer(data=request.data)
        if serializer.is_valid():
            self.thread.stop_thread(**serializer.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusAPIView(PermissionMixin, RequestManager, APIView):
    _user_model = UserObject()
    _thread_model = ThreadObject()
    _thread_manager = ThreadManager()

    def get(self, request: Request, user_id: str = None):
        if user_id:
            return self._get_current_user(user_id=user_id)
        users, links, threads = self._user_model.user, self._user_model.link, list(self._thread_model.thread.keys())
        result = {'threads': {'list': threads, 'count': len(threads)}, 'users': users, 'links': links}
        return Response(result, status=status.HTTP_200_OK)

    def _get_current_user(self, user_id: str):
        links = self._user_model.user.get(user_id)
        if links:
            user_data = {user_id: links}
            return Response(user_data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request: Request, user_id: str = None):
        if user_id:
            return Response(
                {'errors': 'URL path "user_id" could not be proceeded in POST method'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            self.manage(data=serializer.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, user_id: str = None):
        errors = {}

        if not user_id:
            return Response(
                {'errors': 'URL path "user_id" must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_links = self._user_model.user.get(user_id)
        if not self._user_model.user or user_id not in self._user_model.user or not user_links:
            errors['errors'].update(
                {'user_model': f'User with ID {user_id} does not exist in user model or model is empty'}
            )

        if errors.get('errors'):
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, user_id: str = None):
        errors = {'errors': {}}

        if not user_id:
            return Response(
                {'errors': 'URL path "user_id" must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        link = request.data.get('link')
        if not link:
            errors['errors'].update(
                {'link': 'Required field does not exist'}
            )
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if not self._user_model.user.get(user_id):
            errors['errors'].update(
                {'user_model': f'User with ID {user_id} does not exist in user model or model is empty'}
            )

        users_in_link = self._user_model.link.get(link)
        if not users_in_link or user_id not in users_in_link:
            errors['errors'].update(
                {'link_model': f'Link does not exist in link model or model is empty'}
            )

        if errors.get('errors'):
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        self._thread_manager.stop_thread(user_id=user_id, link=link)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
