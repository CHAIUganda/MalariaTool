from django.db import models
from model_utils.models import TimeStampedModel

from dashboard.models.district import District


class Task(TimeStampedModel):
    duration = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    affected_districts = models.ForeignKey(District, related_name="affected_districts")
    target_output_per_quarter = models.IntegerField()
    target_acutal_per_quarter = models.IntegerField()
