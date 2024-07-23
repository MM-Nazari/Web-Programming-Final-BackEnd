from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db.models import Value, F, CharField
from django.db.models.functions import Concat

from nzari import settings


class CustomUserManager(UserManager):
    """
    Custom user manager to add custom methods. We add a create_user method and create a superuser method.
    """

    def _create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(password, **extra_fields)

    def update_user(self, user_id, **kwargs):
        user = self.get(pk=user_id)
        if 'password' in kwargs:
            kwargs['password'] = make_password(kwargs['password'])
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user
