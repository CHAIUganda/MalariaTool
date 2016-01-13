from django.db import models
from model_utils.models import TimeStampedModel


class Member(TimeStampedModel):
    title = models.CharField(max_length=150)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_url = models.FileField(upload_to='images')
