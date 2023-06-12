from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(models.Model):
    nickname = models.CharField(max_length=10)
    win = models.IntegerField()
    defeat = models.IntegerField()
class User(AbstractUser):
    pass