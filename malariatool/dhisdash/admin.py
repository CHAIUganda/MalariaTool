from django.contrib import admin
from dhisdash.models import DataSet, DataElement, CategoryOptionCombo, AgeGroups, Region, District, SubCounty, Facility, \
    DataValue, DataSyncTracker, DataSyncTrackerStatus


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


class DataValueAdmin(admin.ModelAdmin):
    list_display = (
        'get_facility', 'district', 'region', 'data_element', 'get_age_group', 'value', 'original_period', 'category_option_combo')
    search_fields = ('data_element__identifier', 'district__name', 'facility__name')
    list_filter = ('data_element__name', 'period', 'category_option_combo__identifier')

    def get_age_group(self, obj):
        return get_age_group(obj)

    def get_facility(self, obj):
        return obj.facility.name


class DataSyncTrackerAdmin(admin.ModelAdmin):
    list_display = ('period', 'last_downloaded', 'last_parsed', 'get_status')

    def get_status(self, obj):
        if obj.status == DataSyncTrackerStatus.UNKNOWN:
            return 'Unknown'
        elif obj.status == DataSyncTrackerStatus.INIT_PARSE:
            return 'Initial Parse'
        elif obj.status == DataSyncTrackerStatus.INIT_DOWNLOAD:
            return 'Initial Download'
        elif obj.status == DataSyncTrackerStatus.PARSED:
            return 'Parsed'
        elif obj.status == DataSyncTrackerStatus.DOWNLOADED:
            return 'Downloaded'
        else:
            return 'N/A'

admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataElement, DataElementAdmin)
admin.site.register(CategoryOptionCombo, CategoryOptionComboAdmin)
admin.site.register(Region)
admin.site.register(District, DistrictAdmin)
admin.site.register(SubCounty, SubCountyAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(DataValue, DataValueAdmin)
admin.site.register(DataSyncTracker, DataSyncTrackerAdmin)