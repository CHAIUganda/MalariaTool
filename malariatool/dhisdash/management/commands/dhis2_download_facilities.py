from django.core.management import BaseCommand
from dhisdash.models import Region, District, SubCounty, Facility
from dhisdash.utils import dhis2_request


class Command(BaseCommand):

    def handle(self, *args, **options):
        regions = [region.identifier for region in Region.objects.all()]
        districts = [district.identifier for district in District.objects.all()]
        sub_counties = [sub_county.identifier for sub_county in SubCounty.objects.all()]

        combined = regions + districts + sub_counties

        facilities = []
        result = dhis2_request('organisationUnits.json?pageSize=7600')
        self.stdout.write('Returned [%s] organisation units' % len(result['organisationUnits']))

        for org_unit in result['organisationUnits']:
            if org_unit['id'] not in combined:
                facilities.append(org_unit['id'])

                f = Facility()
                f.identifier = org_unit['id']
                f.name = org_unit['displayName']
                f.save()

        self.stdout.write('Collected [%s] facilities' % len(facilities))
