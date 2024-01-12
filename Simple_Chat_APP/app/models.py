from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.name

class Chat(models.Model):
    content = models.CharField(max_length = 1000)
    timestamp = models.DateTimeField(auto_now_add = True)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.content