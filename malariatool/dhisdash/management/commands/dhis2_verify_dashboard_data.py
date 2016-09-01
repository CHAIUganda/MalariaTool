import json

from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.test import RequestFactory

from dhisdash.utils import dhis2_request
from dhisdash.views import JsonDataView


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_set = "Cm5cTKifbLA"
        period = "201603"

        dhis2_total = 0

        print ">>>> Fetching Data Set Report from DHIS2"
        report = dhis2_request('dataSetReport.json?ds=%s&pe=%s&ou=akV6429SUqu' % (data_set, period), False)
        soup = BeautifulSoup(report, 'html.parser')

        dhis2_inpatient_malaria_deaths = self.get_total("malaria total", soup, [3, 4, 7, 8])
        dhis2_malaria_admissions = self.get_total("malaria total", soup, [1, 2, 5, 6])
        dhis2_total_inpatient_deaths = self.get_total("(D) Deaths", soup, [19])

        print ">>>> Fetching Dashboard Data"

        url = "path?from_date=201603&to_date=201604&group=period&region=0&district=0"
        request = RequestFactory().get(url)
        view = JsonDataView()
        result = json.loads(view.get(request).getvalue())

        dashboard_inpatient_malaria_deaths = float(result[period]['inpatient_malaria_deaths'])
        dashboard_malaria_admissions = float(result[period]['malaria_admissions'])
        dashboard_total_inpatient_deaths = float(result[period]['total_inpatient_deaths'])


        print "Inpatient Malaria deaths: DHIS2 (%s), Dashboard (%s)" % (dhis2_inpatient_malaria_deaths,
                                                                dashboard_inpatient_malaria_deaths)

        print "Malaria Admissions: DHIS2 (%s), Dashboard (%s)" % (dhis2_malaria_admissions,
                                                                dashboard_malaria_admissions)

        print "Total Inpatient Deaths: DHIS2 (%s), Dashboard (%s)" % (dhis2_total_inpatient_deaths,
                                                                      dashboard_total_inpatient_deaths)

        assert dhis2_inpatient_malaria_deaths == dashboard_inpatient_malaria_deaths
        assert dhis2_malaria_admissions == dashboard_malaria_admissions
        assert dhis2_total_inpatient_deaths == dashboard_total_inpatient_deaths

    def get_total(self, data_element, soup, sum_columns):
        for table_row in soup.find_all('tr'):
            total = 0
            match_found = False

            for index, column in enumerate(table_row.find_all('td')):
                if data_element.lower() in column.get_text().lower():
                    match_found = True
                    print column.get_text()
                    continue

                if match_found:
                    if index in sum_columns:
                        total += float(column.get_text())

            if match_found:
                return total