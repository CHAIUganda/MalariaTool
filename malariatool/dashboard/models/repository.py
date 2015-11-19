from django.db import models
from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    document_type = models.CharField(max_length=255)
