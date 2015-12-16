from django.db import models
from model_utils.models import TimeStampedModel


class Attendee(TimeStampedModel):
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Meeting(TimeStampedModel):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    attendees = models.ManyToManyField(Attendee, related_name="meeting_attendees")
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
