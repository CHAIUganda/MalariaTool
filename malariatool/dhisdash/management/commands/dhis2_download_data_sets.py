from django.core.management import BaseCommand
from dhisdash import utils

from dhisdash.models import DataSet
from dhisdash.utils import dhis2_request_to_file
from malariatool.settings import BASE_DIR


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('period', nargs='+')

    def handle(self, *args, **options):
        period = options['period'][0]
        root_org_unit = 'akV6429SUqu'

        data_sets = DataSet.objects.all()
        for data_set in data_sets:

            if data_set.period_type.lower() == 'weekly':
                year = int(period[0:4])
                month = int(period[4:])

                weeks = utils.month_to_weeks(year, month)
                period_list = utils.create_period_list(year, weeks)
            else:
                period_list = period

            file_name = "%s/dhisdash/downloads/data_set_%s_%s.json" % (BASE_DIR, data_set.identifier, period)
            result = dhis2_request_to_file(
                'dataValueSets.json?dataSet=%s&orgUnit=%s&period=%s&children=true' % (
                    data_set.identifier, root_org_unit, period_list), file_name)