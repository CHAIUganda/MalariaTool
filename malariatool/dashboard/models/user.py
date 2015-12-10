from custom_user.models import AbstractEmailUser
from django.db import models

from dashboard.models.implementing_partner import IP


class User(AbstractEmailUser):
    title = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    ip = models.ForeignKey(IP, related_name="ip_user", null=True, blank=True)
