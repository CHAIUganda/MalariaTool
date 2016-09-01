from __future__ import division
from time import sleep
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
import sys
from dhisdash.models import Region, District, SubCounty, Facility
from dhisdash.utils import dhis2_request


class Command(BaseCommand):
    help = 'Set the parents for the different org units'

    def add_arguments(self, parser):
        parser.add_argument('unit', nargs='+')

    def show_status(self, parent_position, parent_total, position, total):
        parent_val = (int(parent_position) / int(parent_total)) * 100
        val = (int(position) / int(total)) * 100
        sys.stdout.write('Status: %.2f%% -> %d%%\r' % (parent_val, int(val)))

    def handle(self, *args, **options):
        unit = options['unit'][0]

        if unit == 'district':
            regions = Region.objects.all()
            for region in regions:
                result = dhis2_request('organisationUnits/%s.json' % region.identifier)
                for child in result['children']:
                    try:
                        child_district = District.objects.get(identifier=child['id'])
                        child_district.region = region
                        child_district.save()
                    except ObjectDoesNotExist:
                        pass

        elif unit == 'sub_county':
            districts = District.objects.all()
            total_districts = len(districts)

            for district_idx, district in enumerate(districts):
                result = dhis2_request('organisationUnits/%s.json?pageSize=10000' % district.identifier)

                total_children = len(result['children'])
                for child_idx, child in enumerate(result['children']):
                    try:
                        child_sub_county = SubCounty.objects.get(identifier=child['id'])
                        child_sub_county.district = district
                        child_sub_county.save()
                    except ObjectDoesNotExist:
                        pass

                    self.show_status(district_idx, total_districts, child_idx, total_children)

        elif unit == 'facility':
            sub_counties = SubCounty.objects.all()
            total_sub_counties = len(sub_counties)
            # last_county = 'pnxCSdB9Msk'
            # start = False

            for sub_county_idx, sub_county in enumerate(sub_counties):
                # if start is False:
                #     if sub_county.identifier == last_county:
                #         start = True
                #     else:
                #         continue

                result = dhis2_request('organisationUnits/%s.json?pageSize=10000' % sub_county.identifier)

                total_children = len(result['children'])
                for child_idx, child in enumerate(result['children']):
                    try:
                        child_facility = Facility.objects.get(identifier=child['id'])
                        child_facility.sub_county = sub_county
                        child_facility.save()
                    except ObjectDoesNotExist:
                        pass

                    self.show_status(sub_county_idx, total_sub_counties, child_idx, total_children)

        else:
            pass

