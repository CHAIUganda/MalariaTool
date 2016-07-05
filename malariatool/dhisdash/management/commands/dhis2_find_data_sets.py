from django.core.management import BaseCommand

from dhisdash.utils import dhis2_request


class Command(BaseCommand):
    help = 'Find the Data Sets that containe the passed Data Element name'

    def add_arguments(self, parser):
        parser.add_argument('data_element_name', nargs='+')

    def handle(self, *args, **options):
        data_element_name = options['data_element_name'][0]

        result = dhis2_request('dataElements.json?pageSize=50000')
        data_elements = result['dataElements']

        for de in data_elements:
            if de['displayName'].startswith(data_element_name):
                print "%s (%s)" % (de['displayName'], de['id'])

                result = dhis2_request('dataElements/%s.json' % de['id'])
                data_sets = result['dataSets']

                for index, ds in enumerate(data_sets):
                    result = dhis2_request('dataSets/%s.json' % ds['id'])

                    print "  %s. %s (%s) *%s" % (index+1, result['name'], ds['id'], result['periodType'])
