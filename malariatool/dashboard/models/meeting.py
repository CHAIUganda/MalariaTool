from django.db import models
from model_utils.models import TimeStampedModel

from dashboard.models.user import User


class Meeting(TimeStampedModel):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    attendees = models.ManyToManyField(User)
    location = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.title

