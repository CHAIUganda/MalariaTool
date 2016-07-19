from unittest import TestCase
from dhisdash import utils
from dhisdash.tests.helpers import MyTestHelper


class UtilsTestCase(TestCase):
    def __init__(self, methodName):
        super(UtilsTestCase, self).__init__(methodName)
        self.test_helper = MyTestHelper()

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

    def test_generate_periods_in_rage(self):
        ranges = utils.periods_in_ranges("201508", "201602")
        self.assertEqual(['201508', '201509', '201510', '201511', '201512', '201601', '201602'], ranges)

    def test_that_month_to_weeks_compares_years_too(self):
        weeks = utils.month_to_weeks(2015, 12)
        self.assertEqual(weeks, [50, 51, 52, 53])
