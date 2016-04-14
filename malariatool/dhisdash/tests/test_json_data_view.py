from django.test import TestCase

from dhisdash.models import AgeGroups

from dhisdash.tests.helpers import MyTestHelper
from dhisdash.tests.my_test_case import MyTestCaseHelper


class JsonDataViewTestCase(TestCase, MyTestCaseHelper):
    def __init__(self, methodName):
        super(JsonDataViewTestCase, self).__init__(methodName)
        self.test_helper = MyTestHelper()

    def setUp(self):
        self.setup_environment()

    def test_data_values_facility_period_data_element_unique_together(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        error_occurred = False
        try:
            self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5,
                                               self.data_set, 201505, 10, AgeGroups.under_5_years)

        except Exception, e:
            # print e.message
            error_occurred = True

        self.assertTrue(error_occurred)

    def test_rdt_positive_for_period(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0'
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(28, value)

    def test_rdt_positive_for_period_in_age_group_under_five(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0&age_group=1'
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(10, value)

    def test_rdt_positive_for_period_in_age_group_five_and_above(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0&age_group=2'
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(18, value)

    def test_rdt_positive_for_district_in_multiple_periods_and_age_five_and_above(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201506, 18, AgeGroups.over_or_equal_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201507, 20, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201507&group=district&region=0&district=0&age_group=2'
        value = self.get_value_from_url(url, str(self.district.pk), 'rdt_positive')
        self.assertEqual(38, value)