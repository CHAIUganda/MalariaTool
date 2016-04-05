from django.core.management import BaseCommand
from dhisdash.models import DataElement, CategoryOptionCombo
from dhisdash.utils import dhis2_request


class Command(BaseCommand):
    help = 'Fetches Category Option Combos for the different Data Elements'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for element in DataElement.objects.all():
            print element.name
            data_elements = dhis2_request('dataElements/%s.json' % element.identifier)

            category_combo = data_elements['categoryCombo']['id']
            category_combos = dhis2_request('categoryCombos/%s.json' % category_combo)
            category_option_combos = category_combos['categoryOptionCombos']

            for category_option_combo in category_option_combos:
                result = dhis2_request('categoryOptionCombos/%s.json' % category_option_combo['id'])

                print '    %s' % result['name']
                selection = raw_input('    Under 5 years(1) 5 years and above (2) others(0): ')

                try:
                    coc = CategoryOptionCombo()
                    coc.data_element = element
                    coc.name = result['name']
                    coc.age_group = int(selection)
                    coc.identifier = category_option_combo['id']
                    # Should be run once
                    coc.save()
                except Exception, e:
                    print e.message