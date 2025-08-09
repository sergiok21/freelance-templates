import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .telegram import Telegram, Verifier
from .serializers import TelegramAPISerializer

logger = logging.getLogger(__name__)


class TelegramAPIView(APIView):

    def __init__(self):
        super().__init__()

        self.telegram = Telegram()
        self.verifier = Verifier()

    def get_permissions(self):
        user_id, token = self.request.META.get('HTTP_USER_ID'), self.request.META.get('HTTP_AUTHORIZATION')
        if token and user_id:
            user_token = self.verifier.check_user_id_and_token(user_id, token)
            return [AllowAny()] if user_token else [IsAuthenticatedOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def post(self, request):
        serializer = TelegramAPISerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            user_id = self.request.META.get('HTTP_USER_ID')
            self.telegram.send_message(user_id=user_id, instance=instance)
            logger.info(f'Car data was sent to {user_id}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
