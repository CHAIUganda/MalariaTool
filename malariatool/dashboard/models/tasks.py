from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel

from dashboard.models import IP
from dashboard.models.district import District


class Task(TimeStampedModel):
    type_choices = (
        ('Training', 'Training'),
        ('Supervision', 'Supervision'),
        ('BCC', 'BCC'),
        ('New Distribution', 'New Distribution'),
        ('IPTp', 'IPTp'),
        ('IRS', 'IRS'),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    affected_districts = models.ManyToManyField(District, related_name="affected_districts")
    overview = models.TextField()
    type = models.CharField(max_length=150, choices=type_choices)
    ip = models.ForeignKey(IP, related_name="ip_tasks")

    def percent_complete(self):
        items = self.taskitems.all()
        done_items_list = []
        total_items = len(items)
        for item in items:
            if item.status == "done":
                done_items_list.append(item)
        if total_items < 1:
            total_items = 1
        percentage = (float(len(done_items_list)) / total_items) * 100
        return round(percentage, 1)

    def __unicode__(self):
        return str(self.id)


class Item(TimeStampedModel):
    STATUS = Choices('not_started', 'ongoing', 'done')
    description = models.TextField()
    estimated_end_date = models.DateField()
    status = StatusField()
    task = models.ForeignKey(Task, related_name="taskitems")

    def notes(self):
        return len(self.taskitemnotes.all())

    def __unicode__(self):
        return str(self.id)


class Note(TimeStampedModel):
    item = models.ForeignKey(Item, related_name="taskitemnotes")
    text = models.TextField()

    def __unicode__(self):
        return str(self.id)
