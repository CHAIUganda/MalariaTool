import json

from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import View

from dhisdash.common.IdentifierManager import IdentifierManager
from dhisdash.models import DataValue, District
from dhisdash.utils import periods_in_ranges


class JsonDataView(View):
    MALARIA_RDT = 'fOZ2QUjRSB7'
    MALARIA_MICROSCOPY = 'STF7P24RAqC'

    OPD_MALARIA_TOTAL = 'Q62QyMDzm3h'
    ACT_CONSUMED = 'IBuhlkMrwqY'

    A1_FIRST_VISIT = 'eGSUL2aL0zW'
    A6_FIRST_DOSE = 'YNkTlREfRJj'
    A7_FIRST_DOSE = 'lNohgsiZ1lr'

    MALARIA_TREATED = 'ZgPtploqq0L'

    POSITIVE_UNDER_FIVE = 'PT9vhPUpxc4'
    POSITIVE_OVER_FOUR = 'Li89EZS6Jss'
    DONE_UNDER_FIVE = 'bSUziAZFlqN'
    DONE_OVER_FOUR = 'snPZPBW4ZW0'

    def __init__(self, **kwargs):
        self.im = IdentifierManager()
        super(JsonDataView, self).__init__(**kwargs)

    def get_int_with_default(self, request, name, default):
        try:
            result = int(request.GET.get(name, default))
        except ValueError:
            result = default
        return result

    def filter_on_request(self, request, partial_filter, enable_age_group=True):
        start_period = int(request.GET['from_date'])
        end_period = int(request.GET['to_date'])
        group_by_column = request.GET['group']

        region = self.get_int_with_default(request, 'region', 0)
        district = self.get_int_with_default(request, 'district', 0)
        age_group = self.get_int_with_default(request, 'age_group', 0)

        results = partial_filter.filter(period__gte=start_period, period__lte=end_period) \
            .values(group_by_column).annotate(Sum('value'))

        if region > 0 and district > 0:
            results = results.filter(Q(region=region) | Q(district=district))
        elif region == 0 and district > 0:
            results = results.filter(district=district)
        elif district == 0 and region > 0:
            results = results.filter(region=region)

        if enable_age_group and age_group != 0:
            results = results.filter(age_group=age_group)

        return results

    def get_population(self, request):
        start_period = request.GET['from_date']
        end_period = request.GET['to_date']
        group_by_column = request.GET['group']

        region = self.get_int_with_default(request, 'region', 0)
        district = self.get_int_with_default(request, 'district', 0)

        results = []
        if group_by_column == 'period':
            total_population = District.objects

            if region == 0 and district > 0:
                total_population = total_population.filter(pk=district)
            elif district == 0 and region > 0:
                total_population = total_population.filter(region=region)

            total_population = total_population.aggregate(Sum('population'))

            for period in periods_in_ranges(start_period, end_period):
                results.append({'period': int(period), 'value__sum': total_population['population__sum']})

        elif group_by_column == 'district':
            districts = District.objects.all()
            for district in districts:
                results.append({'district': district.pk, 'value__sum': district.population})

        return results

    def get_rdt_positive(self, request):
        rdt_positive_filter = DataValue.objects.filter(data_element__identifier=self.MALARIA_RDT) \
            .filter(Q(category_option_combo__identifier=self.POSITIVE_UNDER_FIVE) |
                    Q(category_option_combo__identifier=self.POSITIVE_OVER_FOUR))

        return self.filter_on_request(request, rdt_positive_filter)

    def get_rdt_done(self, request):
        rdt_done_filter = DataValue.objects.filter(data_element__identifier=self.MALARIA_RDT) \
            .filter(Q(category_option_combo__identifier=self.DONE_UNDER_FIVE) |
                    Q(category_option_combo__identifier=self.DONE_OVER_FOUR))

        return self.filter_on_request(request, rdt_done_filter)

    def get_microscopy_positive(self, request):
        microscopy_positive_filter = DataValue.objects.filter(data_element__identifier=self.MALARIA_MICROSCOPY) \
            .filter(Q(category_option_combo__identifier=self.POSITIVE_UNDER_FIVE) |
                    Q(category_option_combo__identifier=self.POSITIVE_OVER_FOUR))

        return self.filter_on_request(request, microscopy_positive_filter)

    def get_microscopy_done(self, request):
        microscopy_done_filter = DataValue.objects.filter(data_element__identifier=self.MALARIA_MICROSCOPY) \
            .filter(Q(category_option_combo__identifier=self.DONE_UNDER_FIVE) |
                    Q(category_option_combo__identifier=self.DONE_OVER_FOUR))

        return self.filter_on_request(request, microscopy_done_filter)

    def get_opd_malaria_total(self, request):
        opd_malaria_total_filter = DataValue.objects.filter(data_element__identifier=self.OPD_MALARIA_TOTAL)
        return self.filter_on_request(request, opd_malaria_total_filter)

    def get_opd_malaria_total_all_ages(self, request):
        opd_malaria_total_filter = DataValue.objects.filter(data_element__identifier=self.OPD_MALARIA_TOTAL)
        return self.filter_on_request(request, opd_malaria_total_filter, enable_age_group=False)

    def get_act_consumed(self, request):
        act_consumed_filter = DataValue.objects.filter(data_element__identifier=self.ACT_CONSUMED)
        return self.filter_on_request(request, act_consumed_filter, enable_age_group=False)

    def get_a1_first_visit(self, request):
        a1_first_visit_filter = DataValue.objects.filter(data_element__identifier=self.A1_FIRST_VISIT)
        return self.filter_on_request(request, a1_first_visit_filter)

    def get_a6_first_dose(self, request):
        a6_first_dose_filter = DataValue.objects.filter(data_element__identifier=self.A6_FIRST_DOSE)
        return self.filter_on_request(request, a6_first_dose_filter)

    def get_a7_first_dose(self, request):
        a7_first_dose_filter = DataValue.objects.filter(data_element__identifier=self.A7_FIRST_DOSE)
        return self.filter_on_request(request, a7_first_dose_filter)

    def get_malaria_treated(self, request):
        malaria_treated_filter = DataValue.objects.filter(data_element__identifier=self.MALARIA_TREATED)
        return self.filter_on_request(request, malaria_treated_filter, enable_age_group=False)

    def get_inpatient_malaria_deaths(self, request):
        coc_filters = self.get_coc_filters(
            'Under 5 years, Death, Female',
            'Under 5 years, Death, Male',
            '5 years and above, Death, Female',
            '5 years and above, Death, Male'
        )

        return self.get_values(request, '108-6 Malaria total', coc_filters)

    def get_malaria_admissions(self, request):
        coc_filters = self.get_coc_filters(
            'Under 5 years, Case, Female',
            'Under 5 years, Case, Male',
            '5 years and above, Case, Female',
            '5 years and above, Case, Male'
        )

        return self.get_values(request, '108-6 Malaria total', coc_filters)

    def get_total_inpatient_deaths(self, request):
        return self.get_values(request, '108-1 Deaths', None)

    def get_opd_malaria_cases(self, request):
        return self.get_values(request, '105-1.3 OPD Malaria (Total)', None)

    def add_to_final(self, data, partial_data, key, group_by_column, create=True):
        for result in partial_data:
            group_column_value = result[group_by_column]

            if group_column_value not in data:
                if not create:
                    continue

                data[group_column_value] = {}

            data[group_column_value][key] = result['value__sum']

        return data

    def get_coc_filters(self, *names):
        f = None
        for name in names:
            if f is None:
                f = Q(category_option_combo__identifier=self.im.coc(name))
            else:
                f = f | Q(category_option_combo__identifier=self.im.coc(name))
        return f

    def get_values(self, request, data_element, coc_filters):
        if coc_filters is not None:
            data_filter = DataValue.objects.filter(data_element__identifier=self.im.de(data_element))\
                .filter(coc_filters)
        else:
            data_filter = DataValue.objects.filter(data_element__identifier=self.im.de(data_element))

        return self.filter_on_request(request, data_filter)

    def get(self, request):
        rdt_positive = self.get_rdt_positive(request)
        rdt_done = self.get_rdt_done(request)

        microscopy_positive = self.get_microscopy_positive(request)
        microscopy_done = self.get_microscopy_done(request)

        opd_malaria_total = self.get_opd_malaria_total(request)
        opd_malaria_total_all_ages = self.get_opd_malaria_total_all_ages(request)
        act_consumed = self.get_act_consumed(request)

        a1_first_visit = self.get_a1_first_visit(request)
        a6_first_dose = self.get_a6_first_dose(request)
        a7_first_dose = self.get_a7_first_dose(request)

        malaria_treated = self.get_malaria_treated(request)
        inpatient_malaria_deaths = self.get_inpatient_malaria_deaths(request)
        malaria_admissions = self.get_malaria_admissions(request)
        total_inpatient_deaths = self.get_total_inpatient_deaths(request)
        opd_malaria_cases = self.get_opd_malaria_cases(request)
        population = self.get_population(request)

        data = {}
        data = self.add_to_final(data, rdt_positive, 'rdt_positive', request.GET['group'])
        data = self.add_to_final(data, rdt_done, 'rdt_done', request.GET['group'])
        data = self.add_to_final(data, microscopy_positive, 'microscopy_positive', request.GET['group'])
        data = self.add_to_final(data, microscopy_done, 'microscopy_done', request.GET['group'])
        data = self.add_to_final(data, opd_malaria_total, 'opd_malaria_total', request.GET['group'])
        data = self.add_to_final(data, opd_malaria_total_all_ages, 'opd_malaria_total_all_ages', request.GET['group'])
        data = self.add_to_final(data, act_consumed, 'act_consumed', request.GET['group'])
        data = self.add_to_final(data, a1_first_visit, 'a1_first_visit', request.GET['group'])
        data = self.add_to_final(data, a6_first_dose, 'a6_first_dose', request.GET['group'])
        data = self.add_to_final(data, a7_first_dose, 'a7_first_dose', request.GET['group'])
        data = self.add_to_final(data, malaria_treated, 'malaria_treated', request.GET['group'])
        data = self.add_to_final(data, inpatient_malaria_deaths, 'inpatient_malaria_deaths', request.GET['group'])
        data = self.add_to_final(data, malaria_admissions, 'malaria_admissions', request.GET['group'])
        data = self.add_to_final(data, total_inpatient_deaths, 'total_inpatient_deaths', request.GET['group'])
        data = self.add_to_final(data, opd_malaria_cases, 'opd_malaria_cases', request.GET['group'])
        data = self.add_to_final(data, population, 'population', request.GET['group'], False)

        return HttpResponse(json.dumps(data))