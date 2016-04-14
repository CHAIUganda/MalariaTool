from datetime import date, timedelta
from io import StringIO
from unittest import TestCase
from django.core.management import call_command
from django.utils import timezone
from dhisdash import utils
from dhisdash.common.data_set_parser import DataSetParser
from dhisdash.models import DataSyncTracker, DataSet, DataSyncTrackerStatus
from mock import patch
from dhisdash.tests.helpers import MyTestHelper


class TestDataParse(TestCase):

    def setUp(self):
        self.start_period = '201505'
        self.end_period = date.today().strftime("%Y%m")
        DataSyncTracker.objects.all().delete()

    def test_that_missing_periods_are_automatically_added(self):

        trackers = DataSyncTracker.objects.all()
        self.assertEqual(0, trackers.count())

        call_command('dhis2_data_parse', self.start_period)

        trackers = DataSyncTracker.objects.all()
        results = utils.periods_in_ranges(self.start_period, self.end_period)

        self.assertEqual(len(results), trackers.count())

    def create_old_tracker(self, period, last_parsed_date):
        first = DataSyncTracker()
        first.period = period
        first.last_parsed = last_parsed_date
        first.save()
        return first

    def test_download_is_called_only_on_last_downloaded_older_than_a_day(self):
        three_days_ago = timezone.now() - timedelta(days=2)
        first = self.create_old_tracker(201505, three_days_ago)
        first.status = DataSyncTrackerStatus.DOWNLOADED
        first.save()

        second = self.create_old_tracker(201506, three_days_ago)
        second.status = DataSyncTrackerStatus.DOWNLOADED
        second.save()

        ds1 = MyTestHelper().create_sample_data_set()
        ds2 = MyTestHelper().create_sample_data_set()

        with patch.object(DataSetParser, 'parse', return_value=None) as mock_method:
            call_command('dhis2_data_parse', self.start_period)

        first.delete()
        second.delete()

        total_data_sets = DataSet.objects.count()

        ds1.delete()
        ds2.delete()
        self.assertEqual(2*total_data_sets, mock_method.call_count)

    def test_that_last_parsed_is_updated_after_parse(self):
        current_date = timezone.now()
        three_days_ago = timezone.now() - timedelta(days=2)
        first = self.create_old_tracker(201505, three_days_ago)
        first.status = DataSyncTrackerStatus.DOWNLOADED
        first.save()

        with patch.object(DataSetParser, 'parse', return_value=None) as mock_method:
            with patch.object(timezone, 'now', return_value=current_date) as time_mock:
                call_command('dhis2_data_parse', self.start_period)

        new_first = DataSyncTracker.objects.get(period=201505)


        self.assertNotEqual(first.last_parsed, new_first.last_parsed)
        self.assertEqual(current_date, new_first.last_parsed)

    def test_that_status_is_changed_after_initial_parse(self):
        current_date = timezone.now()
        three_days_ago = timezone.now() - timedelta(days=2)
        first = self.create_old_tracker(201505, three_days_ago)

        with patch.object(DataSetParser, 'parse', return_value=None) as mock_method:
            call_command('dhis2_data_parse', self.start_period)

        new_first = DataSyncTracker.objects.get(period=201505)
        self.assertEqual(DataSyncTrackerStatus.UNKNOWN, new_first.status)

        # Second Run
        new_first.last_downloaded = three_days_ago
        new_first.status = DataSyncTrackerStatus.INIT_DOWNLOAD
        new_first.save()

        with patch.object(DataSetParser, 'parse', return_value=None) as mock_method:
            call_command('dhis2_data_parse', self.start_period)

        new_first = DataSyncTracker.objects.get(period=201505)
        self.assertEqual(DataSyncTrackerStatus.PARSED, new_first.status)

    def test_that_parses_only_after_previous_data_has_been_parsed(self):
        three_days_ago = timezone.now() - timedelta(days=2)
        first = self.create_old_tracker(201505, three_days_ago)
        first.status = DataSyncTrackerStatus.PARSED
        first.save()

        second = self.create_old_tracker(201506, three_days_ago)
        second.status = DataSyncTrackerStatus.DOWNLOADED
        second.save()

        third = self.create_old_tracker(201507, three_days_ago)
        third.status = DataSyncTrackerStatus.INIT_DOWNLOAD
        third.save()

        with patch.object(DataSetParser, 'parse', return_value=None) as mock_method:
            call_command('dhis2_data_parse', self.start_period)

        self.assertEqual(2, mock_method.call_count)
