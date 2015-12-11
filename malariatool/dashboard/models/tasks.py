from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel

from dashboard.models import IP
from dashboard.models.district import District


class Task(TimeStampedModel):
    type_choices = (
        ('training', 'Training'),
        ('supervision', 'Supervision'),
        ('bcc', 'BCC'),
        ('net_distribution', 'New Distribution'),
        ('iptp', 'IPTp'),
        ('irs', 'IRS'),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    affected_districts = models.ForeignKey(District, related_name="affected_districts")
    overview = models.TextField()
    type = models.CharField(max_length=150, choices=type_choices)
    ip = models.ForeignKey(IP, related_name="ip_tasks")


class Item(TimeStampedModel):
    STATUS = Choices('not started', 'ongoing', 'done')
    description = models.TextField()
    estimated_end_date = models.DateField()
    status = StatusField()
    task = models.ForeignKey(Task, related_name="taskitems")
