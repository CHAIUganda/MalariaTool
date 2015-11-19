from django.db import models
from model_utils.models import TimeStampedModel

from dashboard.models.user import User


class Meeting(TimeStampedModel):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    attendees = models.ForeignKey(User, related_name="attendee")
