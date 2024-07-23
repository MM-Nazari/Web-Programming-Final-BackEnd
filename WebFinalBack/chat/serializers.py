import datetime

import contact as contact
import pytz
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account import exceptions
from account.exceptions import InvalidInputException, LoginFailException, UniqueMobileException

from account.models import User, Contact
from account.serializers import UserSerializer
from chat.models import Chat
from core.base_exception import BadRequestException
from core.base_serializer import CustomBaseSerializer

from core.message_txt import MessageTxt
from nzari import settings
from nzari.settings import SIMPLE_JWT


class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    receiver_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Chat
        fields = ('members', 'created_at', 'updated_at', 'receiver_id')

    def validate(self, attrs):
        receiver_id = attrs.pop('receiver_id')
        if not User.objects.filter(id=receiver_id).exists():
            raise InvalidInputException
        memebers_id = [self.context['request'].user.id, receiver_id]
        # check if chat exist
        chat = Chat.objects.filter(members__id__in=memebers_id).distinct()
        if chat.exists():
            raise BadRequestException(MessageTxt.ChatExist)
        attrs['members_id'] = memebers_id

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        members = validated_data.get('members_id')
        chat = Chat.objects.create()
        chat.members.add(*members)
        return chat


