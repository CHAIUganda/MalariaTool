from django.db import models


class AgeGroups(object):
    under_5_years = 1
    over_or_equal_5_years = 2


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
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age_group = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class DataValue(models.Model):
    region_identifier = models.CharField(max_length=255)
    district_identifier = models.CharField(max_length=255)
    facility_identifier = models.CharField(max_length=255)
    category_option_identifier = models.CharField(max_length=255)
    age_group = models.IntegerField(default=0)
    period = models.IntegerField()
    value = models.IntegerField()


class Region(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Facility(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
