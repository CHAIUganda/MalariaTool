import json
from unittest import TestCase
from django.test import RequestFactory
from dhisdash.models import Region, District, SubCounty, Facility, CategoryOptionCombo, DataElement, DataSet, DataValue
from dhisdash.tests.helpers import MyTestHelper
from dhisdash.views import JsonDataView


class MyTestCaseHelper(object):

    def reset_environment(self):
        Region.objects.all().delete()
        District.objects.all().delete()
        SubCounty.objects.all().delete()
        Facility.objects.all().delete()
        CategoryOptionCombo.objects.all().delete()
        DataElement.objects.all().delete()
        DataSet.objects.all().delete()
        DataValue.objects.all().delete()

    def setup_environment(self):
        self.reset_environment()

        self.test_helper = MyTestHelper()
        self.region = self.test_helper.create_region(identifier='xxxx')
        self.district = self.test_helper.create_district(self.region, identifier='xxxx')
        self.sub_county = self.test_helper.create_sub_county(self.district, identifier='xxxx')
        self.facility1 = self.test_helper.create_facility(self.sub_county, identifier='xxxx')
        self.org_unit_data = {'region': self.region, 'district': self.district, 'facility': self.facility1}

        self.data_set = self.test_helper.create_sample_data_set()

        self.rdt_data_element = self.test_helper.create_sample_data_element(identifier=JsonDataView.MALARIA_RDT)
        self.positive_under5 = self.test_helper.create_sample_category_option(self.rdt_data_element,
                                                                              identifier=JsonDataView.POSITIVE_UNDER_FIVE)
        self.positive_over4 = self.test_helper.create_sample_category_option(self.rdt_data_element,
                                                                             identifier=JsonDataView.POSITIVE_OVER_FOUR)

    def get_value_from_url(self, url, group_key, value_key):
        request = RequestFactory().get(url)
        view = JsonDataView()
        result = json.loads(view.get(request).getvalue())
        return result[group_key][value_key]