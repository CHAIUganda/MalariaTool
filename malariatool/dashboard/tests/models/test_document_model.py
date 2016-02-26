from unittest import TestCase

from dashboard.models import Document


class DocumentModelTest(TestCase):
    def test_conference_benefit_has_all_fields(self):
        document = Document()

        fields = ['display_name', 'description', 'file', 'type', 'display_name']
        for field in fields:
            self.assertTrue(hasattr(document, field))
        self.assertEqual(8, len(document._meta.fields))
