from unittest import TestCase

from dashboard.models import User


class UserModelTest(TestCase):
    def test_conference_benefit_has_all_fields(self):
        user = User()

        fields = ['title', 'ip', 'first_name', 'last_name']
        for field in fields:
            self.assertTrue(hasattr(user, field))
        self.assertEqual(12, len(user._meta.fields))
