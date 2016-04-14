from django.core.management import BaseCommand

from dhisdash import utils
from dhisdash.common.data_set_downloader import DataSetDownloader

from dhisdash.models import DataSet
from dhisdash.utils import dhis2_request_to_file, get_data_set_file_path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('period', nargs='+')

    def handle(self, *args, **options):
        period = options['period'][0]
        root_org_unit = 'akV6429SUqu'

        data_sets = DataSet.objects.all()

        for data_set in data_sets:
            downloader = DataSetDownloader(data_set, period, root_org_unit)
            downloader.download()