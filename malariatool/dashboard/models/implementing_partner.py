from django.db import models
from model_utils.models import TimeStampedModel


class IP(TimeStampedModel):
    name = models.CharField(max_length=255)
    overview = models.TextField()
    objectives = models.TextField()
    areas_of_operations = models.TextField()
    implementation_period = models.CharField(max_length=255)