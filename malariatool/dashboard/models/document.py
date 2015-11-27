from django.db import models
from model_utils.models import TimeStampedModel

from dashboard.models.user import User


class Document(TimeStampedModel):
    display_name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='documents/%Y/%m/%d')
    type = models.CharField(max_length=50)
    uploader = models.ForeignKey(User, related_name='uploader')
