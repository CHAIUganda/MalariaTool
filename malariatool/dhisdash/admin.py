from django.contrib import admin
from dhisdash.models import DataSet, DataElement, CategoryOptionCombo, AgeGroups, Region, District, SubCounty, Facility, \
    DataSetParser, DataSetParserStatus, DataValue


def get_age_group(obj):
    if obj.age_group == AgeGroups.over_or_equal_5_years:
        return '5 years and above'
    elif obj.age_group == AgeGroups.under_5_years:
        return 'Under 5 years'
    else:
        return 'Unknown'


class CategoryOptionComboAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_element', 'get_age_group', 'identifier')

    def get_age_group(self, obj):
        return get_age_group(obj)


class DataElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier')


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier')


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')


class SubCountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_county')


class DataSetParserAdmin(admin.ModelAdmin):
    list_display = ('data_set', 'period', 'get_status')

    def get_status(self, obj):
        if DataSetParserStatus.STARTED == obj.status:
            return 'Started'
        elif DataSetParserStatus.COMPLETED == obj.status:
            return 'Completed'
        else:
            return 'Unknown'


class DataValueAdmin(admin.ModelAdmin):
    list_display = ('get_facility', 'district', 'region', 'data_element', 'get_age_group', 'value', 'period')

    def get_age_group(self, obj):
        return get_age_group(obj)

    def get_facility(self, obj):
        return obj.facility.name


admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataElement, DataElementAdmin)
admin.site.register(CategoryOptionCombo, CategoryOptionComboAdmin)
admin.site.register(Region)
admin.site.register(District, DistrictAdmin)
admin.site.register(SubCounty, SubCountyAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(DataSetParser, DataSetParserAdmin)
admin.site.register(DataValue, DataValueAdmin)