from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from dhisdash import utils


class AgeGroups(object):
    under_5_years = 1
    over_or_equal_5_years = 2

    @staticmethod
    def to_tuple():
        return [(AgeGroups.under_5_years, 'Under 5 years'), (AgeGroups.over_or_equal_5_years, '5 years and above')]


class Region(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    population = models.IntegerField(default=0)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Facility(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class DataSet(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    period_type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DataElement(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    data_set_identifier = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CategoryOptionCombo(models.Model):
    data_element = models.ForeignKey(DataElement)
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    age_group = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class DataSetParserStatus(object):
    UNKNOWN = 0
    STARTED = 1
    COMPLETED = 2


class DataValue(models.Model):
    class Meta:
        unique_together = (('facility', 'original_period', 'data_element', 'category_option_combo'),)

    data_set = models.ForeignKey(DataSet, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    data_element = models.ForeignKey(DataElement, on_delete=models.SET_NULL, null=True, blank=True)
    category_option_combo = models.ForeignKey(CategoryOptionCombo, on_delete=models.SET_NULL, null=True, blank=True)
    age_group = models.IntegerField(default=0)
    period = models.IntegerField()
    original_period = models.CharField(max_length=20)
    value = models.IntegerField()


class DataSyncTrackerStatus(object):
    UNKNOWN = 0
    INIT_DOWNLOAD = 1
    INIT_PARSE = 2
    DOWNLOADED = 3
    PARSED = 4


class DataSyncTracker(models.Model):

    period = models.IntegerField(unique=True)
    last_downloaded = models.DateTimeField(default=timezone.now)
    last_parsed = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)

    @staticmethod
    def update_periods(current_period, start_period):
        periods = utils.periods_in_ranges(start_period, current_period)
        tracked_periods = [str(dst.period) for dst in DataSyncTracker.objects.all()]
        diff = [period for period in periods if period not in tracked_periods]

        two_day_ago = timezone.now() - timedelta(days=2)

        for period in diff:
            tracker = DataSyncTracker()
            tracker.period = int(period)
            tracker.last_downloaded = two_day_ago
            tracker.last_parsed = two_day_ago
            tracker.status = DataSyncTrackerStatus.UNKNOWN
            tracker.save()