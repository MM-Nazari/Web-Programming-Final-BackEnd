from django.db import models

from account.models import User
from core.base_exception import BadRequestException


# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    members = models.ManyToManyField('account.User', null=True, blank=True, through='ChatUser')
    owner = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    is_group = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='chat_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clear(self):
        # check if is_group is True then name  and owner is necessary
        if self.is_group:
            if not self.name or not self.owner:
                return False
        # check if is_group is False then members are 2 people exactly
        else:
            if self.members.count() != 2:
                return False
            if not self.name:
                self.name = f'{self.members.first().user_name} and {self.members.last().user_name} chat'
            # check members are not same
            if self.members.first() == self.members.last():
                return False
            # check chat is not exist
            if Chat.objects.filter(members=self.members).exists():
                return False
        return True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChatUser(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='receiver', null=True, )
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.sender == self.receiver:
            raise BadRequestException('sender and receiver are same')
