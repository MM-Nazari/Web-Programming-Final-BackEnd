from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

from account import exceptions

UserModel = get_user_model()


class AuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their mobile,national_code or username.
    """

    def authenticate(self, request, user_name=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(user_name=user_name) | Q(phone=user_name), is_active=False)
        except UserModel.DoesNotExist:
            raise exceptions.LoginFailException
        except MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(user_name=user_name) | Q(phone=user_name)).order_by(
                'id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
