from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from chat.models import Chat
from chat.serializers import ChatSerializer
from core.base_view import CustomGenericMixin


# Create your views here.

class ChatModelViewset(CustomGenericMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        #     # user can read or retrieve his/her own chats ,user in members
        return Chat.objects.filter(chatuser__user=self.request.user)
