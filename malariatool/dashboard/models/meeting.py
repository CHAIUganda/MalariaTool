from django.db import models
from model_utils.models import TimeStampedModel

from dashboard.models.user import User


class Meeting(TimeStampedModel):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    attendees = models.ManyToManyField(User, related_name="attendees")
