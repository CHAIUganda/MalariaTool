from unittest import TestCase

from mock import patch

from dhisdash.common.data_set_parser import DataSetParser
from dhisdash.models import DataValue
from dhisdash.tests.my_test_case import MyTestCaseHelper


class TestDataSetParser(TestCase, MyTestCaseHelper):
    def setUp(self):
        self.setup_environment()

    def test_data_value_is_updated_if_integrity_error_occurs(self):
        # Create data value
        period = 201505

        parser = DataSetParser(self.data_set, period)
        parser.save_data_value({'dataElement': self.rdt_data_element.identifier,
                                'categoryOptionCombo': self.positive_under5.identifier,
                                'orgUnit': self.facility1.identifier,
                                'period': 'xx',
                                'value': 10})

        parser.save_data_value({'dataElement': self.rdt_data_element.identifier,
                                'categoryOptionCombo': self.positive_under5.identifier,
                                'orgUnit': self.facility1.identifier,
                                'period': 'xx',
                                'value': 20})

        dv = DataValue.objects.get(facility=self.facility1, data_element=self.rdt_data_element,
                                   category_option_combo=self.positive_under5, period=period)

        self.assertEqual(20, dv.value)

    def test_that_invalid_data_element_is_ignored(self):
        period = 201505
        test_data_values = [{'dataElement': 'wrong'}]

        with patch.object(DataSetParser, 'get_data_values', return_value=test_data_values) as mock_get_values:
            with patch.object(DataSetParser, 'save_data_value', return_value=test_data_values) as mock_method:
                parser = DataSetParser(self.data_set, period)
                parser.parse()

        assert not mock_method.called

    def test_that_valid_data_element_is_saved(self):
        period = 201505
        test_data_values = [{'dataElement': self.rdt_data_element.identifier}]

        with patch.object(DataSetParser, 'get_data_values', return_value=test_data_values) as mock_get_values:
            with patch.object(DataSetParser, 'save_data_value', return_value=None) as mock_method:
                parser = DataSetParser(self.data_set, period)
                parser.parse()

        assert mock_method.called