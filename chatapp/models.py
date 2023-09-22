from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Message(models.Model):
    value = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='received_messages')

    def __str__(self):
        return f"{self.sender.username} to  {self.receiver.username}"