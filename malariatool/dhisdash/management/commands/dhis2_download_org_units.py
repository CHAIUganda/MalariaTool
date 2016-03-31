from django.core.management import BaseCommand
from dhisdash.models import Region, District, SubCounty, Facility
from dhisdash.utils import dhis2_request


def store_children(parent_org_unit, child_model):
    for child_org_unit in parent_org_unit['children']:
        result = dhis2_request('organisationUnits/%s.json' % child_org_unit['id'])

        child_model_instance = child_model()
        child_model_instance.identifier = child_org_unit['id']
        child_model_instance.name = result['name']
        child_model_instance.save()


class Command(BaseCommand):
    help = 'Download the Org Units, Regions, Districts, Sub Counties and Facilities'

    def add_arguments(self, parser):
        parser.add_argument('unit', nargs='+')

    def handle(self, *args, **options):
        root_org_unit = 'akV6429SUqu'  # MOH - Uganda
        unit = options['unit'][0]

        if unit == 'region':
            root_org_unit = dhis2_request('organisationUnits/%s.json' % root_org_unit)
            store_children(root_org_unit, Region)

        elif unit == 'district':
            regions = Region.objects.all()
            for region in regions:
                region_org_unit = dhis2_request('organisationUnits/%s.json' % region.identifier)
                store_children(region_org_unit, District)

        elif unit == 'subcounty':
            districts = District.objects.all()
            for district in districts:
                district_org_unit = dhis2_request('organisationUnits/%s.json' % district.identifier)
                store_children(district_org_unit, SubCounty)

        elif unit == 'facility':
            sub_counties = SubCounty.objects.all()
            for sub_county in sub_counties:
                sub_county_org_unit = dhis2_request('organisationUnits/%s.json' % sub_county.identifier)
                store_children(sub_county_org_unit, Facility)

        else:
            self.stdout.write(self.style.NOTICE('Unknown unit [%s]' % options['unit']))

