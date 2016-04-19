from datetime import date, timedelta

from django.core.management import BaseCommand
from django.db.models import Q
from django.utils import timezone

from dhisdash.common.data_set_parser import DataSetParser
from dhisdash.models import DataSyncTracker, DataSet, DataSyncTrackerStatus


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('period', nargs='+')

    def handle(self, *args, **options):
        start_period = options['period'][0]
        current_period = date.today().strftime("%Y%m")

        DataSyncTracker.update_periods(current_period, start_period)

        one_day_ago = timezone.now() - timedelta(days=1)
        trackers = DataSyncTracker.objects.filter(last_parsed__lte=one_day_ago) \
            .filter(Q(status=DataSyncTrackerStatus.INIT_DOWNLOAD) | Q(status=DataSyncTrackerStatus.DOWNLOADED))
        data_sets = DataSet.objects.all()

        for tracker in trackers:
            try:
                for data_set in data_sets:
                    parser = DataSetParser(data_set, tracker.period)
                    parser.parse()

                tracker.last_parsed = timezone.now()
                tracker.status = DataSyncTrackerStatus.PARSED
                tracker.save()
            except Exception, e:
                print e.message