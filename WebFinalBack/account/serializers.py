from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User, Contact
from core.message_txt import MessageTxt
from nzari.settings import SIMPLE_JWT


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user_name', 'password', 'phone', 'first_name', 'last_name', 'bio')
        extra_kwargs = {'password': {'write_only': True}}
        model = User

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        user = User.objects.update_user(instance.id, **validated_data)
        return user


class TokenObtainPairSerializer(TokenObtainSerializer):
    """
    custom TokenObtainSerializer that add role to the response
    """
    default_error_messages = {
        'no_active_account': MessageTxt.LoginFailNoUser401
    }

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_staff'] = self.user.is_admin
        if SIMPLE_JWT["UPDATE_LAST_LOGIN"]:
            update_last_login(None, self.user)
        return data


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'user_id', 'contact_name', 'user')
        extra_kwargs = {'user_id': {'write_only': True}}
