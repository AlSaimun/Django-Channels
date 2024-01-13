from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.name

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length = 1000)
    timestamp = models.DateTimeField(auto_now_add = True)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.content