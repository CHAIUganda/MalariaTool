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

        districts_list = [{'id': d. id, 'name': d.name} for d in District.objects.all()]
        context['districts_list'] = sorted(districts_list, key=operator.itemgetter('name'))

        context['age_groups'] = AgeGroups.to_tuple()
        context['from_dates_iteritems'] = utils.generate_dates_to_now(2015, 2)
        context['to_dates_iteritems'] = utils.generate_dates_to_now(2015, 2)

        tab_manager = TabManager()
        tab_manager.set_default_tab('death-proportion')
        tab_manager.add('death-proportion', 'DEATH PROPORTION', '#', 'big_metric.death_proportion')
        tab_manager.add('ipt2-rate', 'IPT2 RATE', '#', 'big_metric.ipt2_rate')
        tab_manager.add('weekly-positivity', 'POSITIVITY RATE', '#', 'big_metric.positivity_rate')
        tab_manager.add('sp-stock-out', 'SP STOCK OUT RATE', '#', 'big_metric.sp_stock_out_rate')

        context['tab_manager'] = tab_manager

        ca_manager = ContentAreaManager()

        # CASE MANAGEMENT

        t1 = Toggle('case-mgt-rate', 'Death Proportion', ['Infant Deaths', 'Death Proportion', 'Malaria Cases'])

        ca_manager.add(t1, 'infant-deaths',
                       'infant_deaths_data_table_results',
                       ['Infant Deaths Rate', 'Inpatient Malaria Deaths', 'Malaria Admissions'],
                       ['infant_death_rate', 'inpatient_malaria_deaths', 'malaria_admissions'])

        ca_manager.add(t1, 'death-proportion',
                       'death_proportion_data_table_results',
                       ['Death Proportion', 'Inpatient Malaria Deaths', 'Total Inpatient Deaths'],
                       ['death_proportion', 'inpatient_malaria_deaths', 'total_inpatient_deaths'])

        ca_manager.add(t1, 'malaria-cases',
                       'testing_data_table_results',
                       ['Testing Rate', 'Total Tests', 'Malaria OPD'],
                       ['testing_rate', 'total_tests', 'malaria_total'])

        # PREVENTION

        t2 = Toggle('prevention-rate', '', [])

        ca_manager.add(t2, 'ipt2-rate',
                       'testing_data_table_results',
                       ['Testing Rate', 'Total Tests', 'Malaria OPD'],
                       ['testing_rate', 'total_tests', 'malaria_total'])

        # POSITIVITY

        t3 = Toggle('positivity-rate', 'Weekly Positivity', ['Weekly Positivity', 'Monthly Positivity'])

        ca_manager.add(t3, 'weekly-positivity',
                       'positivity_data_table_results',
                       ['Positivity Rate', 'Total Positive', 'Total Tests'],
                       ['positivity_rate', 'total_positive', 'reported_cases'])

        ca_manager.add(t3, 'monthly-positivity',
                       'positivity_data_table_results',
                       ['Positivity Rate', 'Total Positive', 'Total Tests'],
                       ['positivity_rate', 'total_positive', 'reported_cases'])

        # LOGISTICS

        t4 = Toggle('logistics-rate', 'SP Stock Out', ['SP Stock Out', 'ACT Stock Out'])

        ca_manager.add(t4, 'sp-stock-out',
                       'consumption_data_table_results',
                       ['Consumption Rate', 'ACT Consumed', 'Malaria OPD'],
                       ['consumption_rate', 'act_consumed', 'malaria_total'])

        ca_manager.add(t4, 'act-stock-out',
                       'positivity_data_table_results',
                       ['Positivity Rate', 'Total Positive', 'Total Tests'],
                       ['positivity_rate', 'total_positive', 'reported_cases'])

        context['ca_manager'] = ca_manager

        return context
