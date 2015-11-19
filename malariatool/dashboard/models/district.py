from django.db import models
from model_utils.models import TimeStampedModel


class District(TimeStampedModel):
    name = models.CharField(max_length=255)