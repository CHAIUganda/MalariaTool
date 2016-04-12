import json
from django.test import TestCase, RequestFactory
from dhisdash import utils
from dhisdash.models import DataValue, Facility, Region, District, SubCounty, DataElement, DataSet, DataSetParser, \
    CategoryOptionCombo, AgeGroups
from dhisdash.views import JsonDataView


class TestHelper(object):
    @staticmethod
    def create_region(identifier='xx', name='central'):
        r = Region()
        r.identifier = identifier
        r.name = name
        r.save()
        return r

    @staticmethod
    def create_district(region, identifier='yy', name='kampala'):
        d = District()
        d.identifier = identifier
        d.name = name
        d.region = region
        d.save()
        return d

    @staticmethod
    def create_sub_county(district, identifier='zz', name='nansana'):
        s = SubCounty()
        s.identifier = identifier
        s.name = name
        s.district = district
        s.save()
        return s

    def create_facility(self, sub_county, identifier='aa', name='Sample Facility'):
        f = Facility()
        f.identifier = identifier
        f.name = name
        f.sub_county = sub_county
        f.save()
        return f

    def create_test_data(self):
        r = self.create_region()
        d = self.create_district(r)
        s = self.create_sub_county(d)
        f = self.create_facility(s)

        return {'facility': f, 'sub_county': s, 'district': d, 'region': r}

    @staticmethod
    def create_sample_data_element(identifier='xx', name='sample element', data_set_identifier='yy'):
        de = DataElement()
        de.identifier = identifier
        de.data_set_identifier = data_set_identifier
        de.name = name
        de.save()
        return de

    def create_sample_data_set(self):
        ds = DataSet()
        ds.identifier = 'xx'
        ds.period_type = 'monthly'
        ds.name = 'sample data set'
        ds.save()
        return ds

    def create_sample_data_set_parser(self, ds):
        dsp = DataSetParser()
        dsp.data_set = ds
        dsp.period = 201505
        dsp.status = 1
        dsp.save()
        return dsp

    def create_sample_category_option(self, de, identifier='xx', name='sample combo'):
        co = CategoryOptionCombo()
        co.name = name
        co.identifier = identifier
        co.data_element = de
        co.save()
        return co

    def create_data_value(self, data, de, co, dsp, period, value, age_group=0):
        dv = DataValue()
        dv.region = data['region']
        dv.district = data['district']
        dv.facility = data['facility']
        dv.data_element = de
        dv.category_option_combo = co
        dv.data_set_parser = dsp
        dv.period = period
        dv.age_group = age_group
        dv.value = value
        dv.save()


class UtilsTestCase(TestCase):
    def __init__(self, methodName):
        super(UtilsTestCase, self).__init__(methodName)
        self.test_helper = TestHelper()

    def test_conversion_of_january_month_to_weeks(self):
        weeks = utils.month_to_weeks(2016, 01)
        self.assertEqual(weeks, [1, 2, 3, 4])

    def test_conversion_of_february_month_to_weeks(self):
        weeks = utils.month_to_weeks(2016, 02)
        self.assertEqual(weeks, [5, 6, 7, 8, 9])

    def test_conversion_of_december_month_to_weeks(self):
        weeks = utils.month_to_weeks(2016, 12)
        self.assertEqual(weeks, [49, 50, 51, 52])

    def test_convert_weeks_to_period_list(self):
        weeks = utils.month_to_weeks(2016, 12)
        period_list = utils.create_period_list(2016, weeks)
        self.assertEqual(period_list, "2016W49,2016W50,2016W51,2016W52")

    def test_data_values_facility_period_data_element_unique_together(self):
        data = self.test_helper.create_test_data()
        de = self.test_helper.create_sample_data_element()
        ds = self.test_helper.create_sample_data_set()
        co = self.test_helper.create_sample_category_option(de)
        dsp = self.test_helper.create_sample_data_set_parser(ds)

        self.test_helper.create_data_value(data, de, co, dsp, 201505, 10)

        error_occurred = False
        try:
            self.test_helper.create_data_value(data, de, co, dsp, 201505, 10)
        except Exception, e:
            # print e.message
            error_occurred = True

        self.assertTrue(error_occurred)


class JsonDataViewTestCase(TestCase):
    def __init__(self, methodName):
        super(JsonDataViewTestCase, self).__init__(methodName)
        self.test_helper = TestHelper()

    def setUp(self):
        self.region = self.test_helper.create_region()
        self.district = self.test_helper.create_district(self.region)
        self.sub_county = self.test_helper.create_sub_county(self.district)
        self.facility1 = self.test_helper.create_facility(self.sub_county)
        self.org_unit_data = {'region': self.region, 'district': self.district, 'facility': self.facility1}

        self.data_set = self.test_helper.create_sample_data_set()
        self.dsp = self.test_helper.create_sample_data_set_parser(self.data_set)

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

    def test_rdt_positive_for_period(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.dsp,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.dsp,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0'
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(28, value)

    def test_rdt_positive_for_period_in_age_group_under_five(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.dsp,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.dsp,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0&age_group=1'
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(10, value)

    def test_rdt_positive_for_period_in_age_group_five_and_above(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.dsp,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.dsp,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201505&group=period&region=0&district=0&age_group=2'
        value = self.get_value_from_url(url, '201505', 'rdt_positive')
        self.assertEqual(18, value)

    def test_rdt_positive_for_district_in_multiple_periods_and_age_five_and_above(self):
        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_under5, self.dsp,
                                           201505, 10, AgeGroups.under_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.dsp,
                                           201505, 18, AgeGroups.over_or_equal_5_years)

        self.test_helper.create_data_value(self.org_unit_data, self.rdt_data_element, self.positive_over4, self.dsp,
                                           201506, 20, AgeGroups.over_or_equal_5_years)

        url = 'path?from_date=201505&to_date=201506&group=district&region=0&district=0&age_group=2'
        value = self.get_value_from_url(url, str(self.district.pk), 'rdt_positive')
        self.assertEqual(38, value)