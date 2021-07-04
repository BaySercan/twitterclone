from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from django.db.models.base import Model


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(default=datetime.now())

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myfollows")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


