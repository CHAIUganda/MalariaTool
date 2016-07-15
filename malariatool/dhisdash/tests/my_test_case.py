import json

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
        self.district2 = self.test_helper.create_district(self.region, identifier='xxxx2')
        self.district3 = self.test_helper.create_district(self.region, identifier='xxxx3')
        self.sub_county = self.test_helper.create_sub_county(self.district, identifier='xxxx')
        self.facility1 = self.test_helper.create_facility(self.sub_county, identifier='xxxx')
        self.facility2 = self.test_helper.create_facility(self.sub_county, identifier='xxxx2')
        self.facility3 = self.test_helper.create_facility(self.sub_county, identifier='xxxx3')
        self.org_unit_data = {'region': self.region, 'district': self.district, 'facility': self.facility1}

        self.data_set = self.test_helper.create_sample_data_set()

        self.rdt_data_element = self.test_helper.create_sample_data_element(identifier="fOZ2QUjRSB7",
                                                                            name="105-7.3 Lab Malaria RDTs")

        self.act_data_element = self.test_helper.create_sample_data_element(identifier="IBuhlkMrwqY",
                                                                            name="105-6 Artemether/ Lumefantrine 100/20mg tablet")

        self.positive_under5 = self.test_helper.create_sample_category_option(self.rdt_data_element,
                                                                              identifier="PT9vhPUpxc4",
                                                                              name="Number Positive, Under 5 years")

        self.positive_over4 = self.test_helper.create_sample_category_option(self.rdt_data_element,
                                                                             identifier="Li89EZS6Jss",
                                                                             name="Number Positive, 5 years and above"
                                                                             )

        self.days_out_of_stock = self.test_helper.create_sample_category_option(self.act_data_element,
                                                                         identifier="Avvv8JaSwGR",
                                                                         name="Days out of stock"
                                                                         )



    def get_value_from_url(self, url, group_key, value_key):
        request = RequestFactory().get(url)
        view = JsonDataView()
        view.im.category_option_combos = {
            "Number Positive, Under 5 years": "PT9vhPUpxc4",
            "Number Positive, 5 years and above": "Li89EZS6Jss",
            "Days out of stock": "Avvv8JaSwGR"
        }

        view.im.data_elements = {
            "105-7.3 Lab Malaria RDTs": "fOZ2QUjRSB7",
            "105-6 Artemether/ Lumefantrine 100/20mg tablet": "IBuhlkMrwqY",
        }

        result = json.loads(view.get(request).getvalue())
        print result
        return result[group_key][value_key]