import operator
from django.views.generic import TemplateView

from dhisdash import utils
from dhisdash.common.ContentAreaManager import ContentAreaManager
from dhisdash.common.TabManager import TabManager
from dhisdash.common.ToggleManager import Toggle
from dhisdash.models import Region, District, AgeGroups


class HomePageView(TemplateView):
    template_name = 'dhisdash/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['regions_list'] = Region.objects.all()

        districts_list = [{'id': d.id, 'name': d.name} for d in District.objects.all()]
        context['districts_list'] = sorted(districts_list, key=operator.itemgetter('name'))

        context['age_groups'] = AgeGroups.to_tuple()
        context['from_dates_iteritems'] = utils.generate_dates_to_now(2015, 2)
        context['to_dates_iteritems'] = utils.generate_dates_to_now(2015, 2)

        act_stock_status_description = 'Proportion of health facilities that reported no stocks outs of first line anti-malarial medicines (ACTs) lasting more than 7 days in the previous month'

        tab_manager = TabManager()
        tab_manager.set_default_tab('malaria-cases')

        tab_manager.add('malaria-cases', 'MALARIA CASES', 'Malaria cases per 1000 population',
                        'big_metric.malaria_cases')

        tab_manager.add('ipt2-uptake', 'IPT2 UPTAKE', 'Proportion of women who came for IPT2b',
                        'big_metric.ipt2_rate')

        tab_manager.add('weekly-reporting-rate', 'REPORTING RATE', 'Facilities reporting',
                        'big_metric.positivity_rate')

        tab_manager.add('act-stock-status', 'ACT STOCK STATUS', act_stock_status_description,
                        'big_metric.act_stock_status')

        context['tab_manager'] = tab_manager

        ca_manager = ContentAreaManager()

        # CASE MANAGEMENT

        t1 = Toggle('case-mgt-rate', 'Malaria Cases',
                    ['Malaria Cases', 'Testing Rate', 'Positivity Rate', 'Malaria Deaths', 'Mortality Rate'])

        ca_manager.add(t1, 'malaria-deaths',
                       ['Malaria Death Rate', 'Inpatient Malaria Deaths', 'Malaria Admissions'])

        ca_manager.add(t1, 'death-proportion',
                       ['Death Proportion', 'Inpatient Malaria Deaths', 'Total Inpatient Deaths'])

        ca_manager.add(t1, 'malaria-cases',
                       ['Malaria Cases', 'Malaria Cases * 1000', 'Population'])

        # ca_manager.add(t1, 'testing-rate',
        #                ['Testing Rate', 'Total Tests', 'Malaria OPD'])

        ca_manager.add(t1, 'positivity-rate',
                       ['Positivity Rate', 'Tested Positive', 'Number Tested'])

        ca_manager.add(t1, 'mortality-rate',
                       ['Mortality Rate', 'Inpatient Malaria Deaths', 'Total Inpatient Deaths'])

        # PREVENTION

        t2 = Toggle('prevention-rate', '', [])

        ca_manager.add(t2, 'ipt2-uptake',
                       ['Testing Rate', 'Total Tests', 'Malaria OPD'])

        # # POSITIVITY
        #
        # t3 = Toggle('positivity-rate', 'Weekly Positivity', ['Weekly Positivity', 'Monthly Positivity'])
        #
        # ca_manager.add(t3, 'weekly-positivity',
        #                ['Positivity Rate', 'Total Positive', 'Total Tests'])
        #
        # ca_manager.add(t3, 'monthly-positivity',
        #                ['Positivity Rate', 'Total Positive', 'Total Tests'])

        # REPORTING

        # t3 = Toggle('reporting-rate', 'Weekly Reporting Rate', ['Weekly Reporting Rate', 'Monthly Reporting Rate'])
        #
        # ca_manager.add(t3, 'weekly-reporting-rate',
        #                ['Positivity Rate', 'Total Positive', 'Total Tests'])
        #
        # ca_manager.add(t3, 'monthly-reporting-rate',
        #                ['Positivity Rate', 'Total Positive', 'Total Tests'])

        # LOGISTICS

        t4 = Toggle('logistics-rate', 'ACT Stock Status', ['ACT Stock Status', 'SP Stock Status'])

        ca_manager.add(t4, 'sp-stock-status',
                       ['Consumption Rate', 'ACT Consumed', 'Malaria OPD'])

        ca_manager.add(t4, 'act-stock-status',
                       ['Positivity Rate', 'Total Positive', 'Total Tests'])

        context['ca_manager'] = ca_manager

        return context
