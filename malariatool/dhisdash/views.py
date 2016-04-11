import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
import operator
from dhisdash import utils
from dhisdash.models import Region, District, AgeGroups, DataValue


class HomePageView(TemplateView):
    template_name = 'dhisdash/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['regions_list'] = Region.objects.all()

        districts_list = [{'id': d.id, 'name': d.name} for d in District.objects.all()]
        context['districts_list'] = sorted(districts_list, key=operator.itemgetter('name'))

        context['age_groups'] = AgeGroups.to_tuple()
        context['from_dates_iteritems'] = utils.generate_dates_to_now(2014, 8)
        context['to_dates_iteritems'] = utils.generate_dates_to_now(2014, 8)

        return context


class JsonDistrictsView(View):
    def get(self, request):
        districts = District.objects.all()
        result = [(d.id, d.name) for d in districts]
        return HttpResponse(json.dumps(dict(result)))


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

    def add_to_final(self, data, partial_data, key, group_by_column):
        for result in partial_data:
            group_column_value = result[group_by_column]

            if group_column_value not in data:
                data[group_column_value] = {}

            data[group_column_value][key] = result['value__sum']

        return data

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

        return HttpResponse(json.dumps(data))