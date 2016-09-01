from unittest import TestCase
from mock import patch

from dhisdash.common.IdentifierManager import IdentifierManager


class IdentifierManagerTestCase(TestCase):
    VALID_VALUE = 'xxxxx'
    VALID_IDENTIFIER = 'valid_identfier'

    def setUp(self):
        self.im = IdentifierManager()
        self.im.data_elements[self.VALID_IDENTIFIER] = self.VALID_VALUE
        self.im.category_option_combos[self.VALID_IDENTIFIER] = self.VALID_VALUE

    def test_raise_error_data_element_not_found(self):
        with patch.object(self.im, 'load_identifiers', return_value=None) as mocked:
            self.assertRaises(Exception, self.im.de, 'invalid_identifier')

    def test_no_error_raise_when_data_element_exists(self):
        with patch.object(self.im, 'load_identifiers', return_value=None) as mocked:
            try:
                self.im.de('valid_identfier')
            except Exception:
                self.fail("Unexpected exception")

    def test_raise_error_category_option_combo_not_found(self):
        with patch.object(self.im, 'load_identifiers', return_value=None) as mocked:
            self.assertRaises(Exception, self.im.coc, 'invalid_identifier')

    def test_no_error_raise_when_category_option_combo_exists(self):
        with patch.object(self.im, 'load_identifiers', return_value=None) as mocked:
            try:
                self.im.coc('valid_identfier')
            except Exception:
                self.fail("Unexpected exception")

    def test_data_element_is_retured(self):
        self.assertEqual(self.VALID_VALUE, self.im.de(self.VALID_IDENTIFIER))

    def test_category_option_combo_is_retured(self):
        self.assertEqual(self.VALID_VALUE, self.im.coc(self.VALID_IDENTIFIER))