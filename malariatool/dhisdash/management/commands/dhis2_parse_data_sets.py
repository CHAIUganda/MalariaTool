import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from dhisdash import utils
from dhisdash.models import DataSet, DataSetParser, DataSetParserStatus, DataValue, Facility, DataElement, \
    CategoryOptionCombo
from clint.textui import progress

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('period', nargs='+')

    def handle(self, *args, **options):
        period = options['period'][0]

        valid_data_elements = [de.identifier for de in DataElement.objects.all()]

        data_sets = DataSet.objects.all()
        for data_set in data_sets:
            data_set_parser = DataSetParser.objects.filter(data_set=data_set, period=period)

            if data_set_parser:
                if DataSetParserStatus.STARTED == data_set_parser[0].status:
                    self.stdout.write('Parser started for period [%s].' % period)
                elif DataSetParserStatus.COMPLETED == data_set_parser[0].status:
                    self.stdout.write('Parser completed for period [%s].' % period)
                else:
                    self.stdout.write('Parser exists for period [%s] with status unknown.' % period)

                continue

            dsp = DataSetParser()
            dsp.data_set = data_set
            dsp.period = int(period)
            dsp.status = DataSetParserStatus.STARTED
            dsp.save()

            data_set_file_name = utils.get_data_set_file_path(data_set, period)
            data_set_contents = json.load(open(data_set_file_name, "r"))

            for value in progress.bar(data_set_contents['dataValues']):

                try:
                    if value['dataElement'] not in valid_data_elements:
                        continue

                    facility = Facility.objects.get(identifier=value['orgUnit'])
                    district = facility.sub_county.district
                    region = district.region

                    # print 'combo: %s (%s)' % (value['categoryOptionCombo'], value['dataElement'])

                    dv = DataValue()
                    dv.data_set_parser = dsp
                    dv.facility = facility
                    dv.district = district
                    dv.region = region
                    dv.data_element = DataElement.objects.get(identifier=value['dataElement'])
                    dv.category_option_combo = CategoryOptionCombo.objects.get(identifier=value['categoryOptionCombo'])
                    dv.age_group = dv.category_option_combo.age_group
                    dv.period = int(period)
                    dv.value = int(value['value'])
                    dv.save()
                except Exception, e:
                    print e.message
                    print value
                    print '==========='

            dsp.status = DataSetParserStatus.COMPLETED
            dsp.save()
