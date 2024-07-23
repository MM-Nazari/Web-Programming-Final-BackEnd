from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from account.managers import CustomUserManager
from core.message_txt import MessageTxt


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40, )
    last_name = models.CharField(max_length=40, )
    phone = models.CharField(max_length=11, unique=True,  error_messages={'unique': MessageTxt.UniqueMobile})
    user_name = models.CharField(max_length=40, unique=True,  error_messages={'unique': MessageTxt.UniqueUserName400})
    bio = models.TextField(max_length=40, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_admin(self):
        return self.is_superuser


class Contact(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_id')
    contact_name = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = ('user_id', 'contact_id')
