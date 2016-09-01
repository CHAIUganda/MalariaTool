from django.core.management import BaseCommand

from dhisdash.utils import dhis2_request


class Command(BaseCommand):
    help = 'Find the Data Elements contained in a particular Data Set'

    def add_arguments(self, parser):
        parser.add_argument('data_set_id', nargs='+')

    def handle(self, *args, **options):
        data_set_id = options['data_set_id'][0]
        result = dhis2_request('dataSets/%s.json' % data_set_id)

        for index, de in enumerate(result['dataElements']):
            result = dhis2_request('dataElements/%s.json' % de['id'])
            print "%s. %s" % (index+1, result['name'])
