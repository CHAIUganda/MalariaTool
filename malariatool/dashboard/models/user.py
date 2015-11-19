from django.contrib.auth.models import AbstractUser
from django.db import models

from implementing_partner import IP


class User(AbstractUser):
    title = models.CharField(max_length=150)
    IP = models.ForeignKey(IP)
