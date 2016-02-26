from unittest import TestCase

from dashboard.models import Task


class TaskModelTest(TestCase):
    def test_conference_benefit_has_all_fields(self):
        task = Task()

        fields = ['start_date', 'end_date', 'overview', 'type']
        for field in fields:
            self.assertTrue(hasattr(task, field))
        self.assertEqual(8, len(task._meta.fields))
