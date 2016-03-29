from django.db import models
from model_utils.models import TimeStampedModel


class ExcelDocument(TimeStampedModel):
    name = models.CharField(max_length=120)
    files = models.FileField(upload_to="excel_docs")
