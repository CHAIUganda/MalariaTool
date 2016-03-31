from django.contrib import admin
from dhisdash.models import DataSet, DataElement, CategoryOptionCombo, AgeGroups


class CategoryOptionComboAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_age_group', 'identifier')

    def get_age_group(self, obj):
        if obj.age_group == AgeGroups.over_or_equal_5_years:
            return '5 years and above'
        elif obj.age_group == AgeGroups.under_5_years:
            return 'Under 5 years'
        else:
            return 'Unknown'


class DataElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier')


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('name','identifier')


admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataElement, DataElementAdmin)
admin.site.register(CategoryOptionCombo, CategoryOptionComboAdmin)