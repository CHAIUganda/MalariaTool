from unittest import TestCase
from datetime import timedelta
from django.utils import timezone
from dhisdash.common.data_set_downloader import DataSetDownloader
from dhisdash.models import DataSyncTrackerStatus
from dhisdash.tests.my_test_case import MyTestCaseHelper


class TestDataSetDownloader(TestCase, MyTestCaseHelper):
    def setUp(self):
        self.setup_environment()

    def test_that_download_url_has_not_lastUpdated_field_at_beginning(self):
        downloader = DataSetDownloader(self.data_set, 201505, 'xxxx', DataSyncTrackerStatus.UNKNOWN)
        url = downloader.get_download_url()

        self.assertTrue('lastUpdated' not in url)

    def test_that_download_url_has_lastUpdated_if_status_of_tracker_changed(self):
        five_days_ago = timezone.now() - timedelta(days=5)

        downloader = DataSetDownloader(self.data_set, 201505, 'xxxx', DataSyncTrackerStatus.INIT_DOWNLOAD)
        url = downloader.get_download_url()


        self.assertTrue(('lastUpdated=%s&' % five_days_ago.strftime('%Y-%m-%d')) in url)