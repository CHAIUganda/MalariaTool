from datetime import date, timedelta, datetime
from django.core.management import BaseCommand
from django.db.models import Q
from django.utils import timezone
from dhisdash import utils
from dhisdash.common.data_set_downloader import DataSetDownloader
from dhisdash.models import DataSyncTracker, DataSet, DataSyncTrackerStatus


class Command(BaseCommand):
    ROOT_ORG_UNIT = 'akV6429SUqu'

    def add_arguments(self, parser):
        parser.add_argument('period', nargs='+')

    def handle(self, *args, **options):
        start_period = options['period'][0]
        current_period = date.today().strftime("%Y%m")

        DataSyncTracker.update_periods(current_period, start_period)

        one_day_ago = timezone.now() - timedelta(days=1)
        trackers = DataSyncTracker.objects.filter(last_downloaded__lte=one_day_ago) \
            .filter(Q(status=DataSyncTrackerStatus.UNKNOWN) | Q(status=DataSyncTrackerStatus.PARSED)|
                    Q(status=DataSyncTrackerStatus.INIT_PARSE))
        data_sets = DataSet.objects.all()

        for tracker in trackers:
            for data_set in data_sets:
                downloader = DataSetDownloader(data_set, tracker.period, self.ROOT_ORG_UNIT, tracker.status)
                downloader.download()

            tracker.last_downloaded = timezone.now()
            if tracker.status is DataSyncTrackerStatus.UNKNOWN:
                tracker.status = DataSyncTrackerStatus.INIT_DOWNLOAD
            else:
                tracker.status = DataSyncTrackerStatus.DOWNLOADED
            tracker.save()