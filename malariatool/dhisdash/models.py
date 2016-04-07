from django.db import models


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


class DataSetParser(models.Model):
    data_set = models.ForeignKey(DataSet, on_delete=models.SET_NULL, null=True, blank=True)
    period = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return '(%s) %s' % (self.period, self.data_set)


class DataValue(models.Model):
    data_set_parser = models.ForeignKey(DataSetParser, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    data_element = models.ForeignKey(DataElement, on_delete=models.SET_NULL, null=True, blank=True)
    category_option_combo = models.ForeignKey(CategoryOptionCombo, on_delete=models.SET_NULL, null=True, blank=True)
    age_group = models.IntegerField(default=0)
    period = models.IntegerField()
    value = models.IntegerField()
