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

        callbacks = "&callbacks=rdt_positive"
        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0'+callbacks
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(28, value)

    def test_rdt_positive_for_period_in_age_group_under_five(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        callbacks = "&callbacks=rdt_positive"
        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0&age_group=1'+callbacks
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(10, value)

    def test_rdt_positive_for_period_in_age_group_five_and_above(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        callbacks = "&callbacks=rdt_positive"
        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0&age_group=2'+callbacks
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(18, value)

    def test_rdt_positive_for_district_in_multiple_periods_and_age_five_and_above(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201506, 18, AgeGroups.over_or_equal_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.data_set,
                                           201507, 20, AgeGroups.over_or_equal_5_years)

        callbacks = "&callbacks=rdt_positive"
        url = 'path?from_date=201505&to_date=201507&group=district&region=0&district=0&age_group=2'+callbacks
        value = self.get_value_from_url(url, str(self.district.pk), 'rdt_positive')
        self.assertEqual(38, value)

    def test_act_out_of_stock_returns_a_single_facility(self):
        org_data = self.org_unit_data
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201505, 6)

        org_data['facility'] = self.facility2
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201506, 7)

        org_data['facility'] = self.facility3
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201507, 8)

        callbacks = "&callbacks=stock_outs_of_act"
        url = 'path?from_date=201505&to_date=201507&group=district&region=0&district=0' + callbacks
        value = self.get_value_from_url(url, str(self.district.pk), 'stock_outs_of_act')
        self.assertEqual(1, value)

    def test_act_out_of_stock_returns_two_facilities_and_ignores_duplicates(self):
        org_data = self.org_unit_data
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201505, 6)

        org_data['facility'] = self.facility2
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201506, 10)

        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201507, 12)

        org_data['facility'] = self.facility3
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201507, 8)

        callbacks = "&callbacks=stock_outs_of_act"
        url = 'path?from_date=201505&to_date=201507&group=district&region=0&district=0' + callbacks
        value = self.get_value_from_url(url, str(self.district.pk), 'stock_outs_of_act')
        self.assertEqual(2, value)

    def test_act_total_facilities(self):
        org_data = self.org_unit_data
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201505, 6)

        org_data['facility'] = self.facility2
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201506, 10)

        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201507, 12)

        org_data['facility'] = self.facility3
        self.test_helper.create_data_value(org_data, self.act_data_element, self.days_out_of_stock,
                                           self.data_set,
                                           201507, 8)

        callbacks = "&callbacks=submitted_act"
        url = 'path?from_date=201505&to_date=201507&group=district&region=0&district=0' + callbacks
        value = self.get_value_from_url(url, str(self.district.pk), 'submitted_act')
        self.assertEqual(3, value)

    def test_get_population_for_a_single_district(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5,
                                           self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.district.population = 20
        self.district.save()

        self.district2.population = 30
        self.district2.save()

        callbacks = "&callbacks=rdt_positive,population"
        url = 'path?from_date=201505&to_date=201507&group=district&region=0&district=0' + callbacks
        value = self.get_value_from_url(url, str(self.district.pk), 'population')
        self.assertEqual(20, value)

    def test_get_population_for_a_entire_region(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5,
                                           self.data_set,
                                           201505, 10, AgeGroups.under_5_years)

        self.district.population = 20
        self.district.save()

        self.district2.population = 30
        self.district2.save()

        callbacks = "&callbacks=rdt_positive,population"
        url = 'path?from_date=201505&to_date=201507&group=period&region=0&district=0' + callbacks
        value = self.get_value_from_url(url, "201505", 'population')
        self.assertEqual(50, value)

    def test_that_period_data_is_grouped_based_on_the_original_period(self):
        data_value = self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5,
                                                   self.data_set, 201505, 10, AgeGroups.under_5_years)
        data_value.original_period = "2015W2"
        data_value.save()

        callbacks = "&callbacks=rdt_positive"
        url = 'path?from_date=201505&to_date=201507&group=period&region=0&district=0' + callbacks
        value = self.get_value_from_url(url, "2015W2", 'rdt_positive')
        self.assertEqual(10, value)