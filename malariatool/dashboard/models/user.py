from custom_user.models import AbstractEmailUser
from django.db import models
from model_utils.models import TimeStampedModel


class User(AbstractEmailUser):
    title = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
