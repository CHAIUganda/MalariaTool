import json

from django.db.models import Q, Count
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import View

from dhisdash.common.IdentifierManager import IdentifierManager
from dhisdash.models import DataValue, District
from dhisdash.utils import periods_in_ranges


class JsonDataView(View):

    def __init__(self, **kwargs):
        self.callbacks = {}
        self.im = IdentifierManager()
        self.request = None
        self.facility_count_aggregator = Count('facility', distinct=True)

        super(JsonDataView, self).__init__(**kwargs)

    def get_int_with_default(self, request, name, default):
        try:
            result = int(request.GET.get(name, default))
        except ValueError:
            result = default
        return result

    def filter_on_request(self, request, partial_filter, enable_age_group=True, aggregate=None):
        start_period = int(request.GET['from_date'])
        end_period = int(request.GET['to_date'])
        group_by_column = request.GET['group']

        region = self.get_int_with_default(request, 'region', 0)
        district = self.get_int_with_default(request, 'district', 0)
        age_group = self.get_int_with_default(request, 'age_group', 0)

        if aggregate is None:
            aggregate = Sum('value')

        results = partial_filter.filter(period__gte=start_period, period__lte=end_period) \
            .values(group_by_column).annotate(value_aggregate=aggregate)

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
                results.append({'period': int(period), 'value_aggregate': total_population['population__sum']})

        elif group_by_column == 'district':
            districts = District.objects.all()
            for district in districts:
                results.append({'district': district.pk, 'value_aggregate': district.population})

        return results

    def get_rdt_positive(self, request):
        coc_filters = self.get_coc_filters(
            'Number Positive, Under 5 years',
            'Number Positive, 5 years and above'
        )

        return self.get_values(request, '105-7.3 Lab Malaria RDTs', coc_filters)

    def get_rdt_done(self, request):
        coc_filters = self.get_coc_filters(
            'Number Done, Under 5 years',
            'Number Done, 5 years and above'
        )

        return self.get_values(request, '105-7.3 Lab Malaria RDTs', coc_filters)

    def get_microscopy_positive(self, request):
        coc_filters = self.get_coc_filters(
            'Number Positive, Under 5 years',
            'Number Positive, 5 years and above'
        )

        return self.get_values(request, '105-7.3 Lab Malaria Microscopy', coc_filters)

    def get_microscopy_done(self, request):
        coc_filters = self.get_coc_filters(
            'Number Done, Under 5 years',
            'Number Done, 5 years and above'
        )

        return self.get_values(request, '105-7.3 Lab Malaria Microscopy', coc_filters)

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

    def get_number_receiving_ipt2(self, request):
        coc_filters = self.get_coc_filters(
            '10-19 Years',
            '20-24 Years',
            '>=25 Years'
        )

        return self.get_values(request, '105-2.1 A7:Second dose IPT (IPT2)', coc_filters)

    def get_number_attending_anc1(self, request):
        return self.get_values(request, '105-2.1 A1:ANC 1st Visit for women', None)

    def get_number_of_facilities_with_stock_outs_of_sp(self, request):
        coc_filters = self.get_coc_filters('Days out of stock')

        return self.get_values(request, '105-6 Sulfadoxine / Pyrimethamine tablet',
                               coc_filters, self.facility_count_aggregator, False, value__gt=7)

    def get_number_of_facilities_submitted_sp(self, request):
        coc_filters = self.get_coc_filters('Days out of stock')

        return self.get_values(request, '105-6 Sulfadoxine / Pyrimethamine tablet',
                               coc_filters, self.facility_count_aggregator, False)

    def get_number_of_facilities_with_stock_outs_of_act(self, request):
        coc_filters = self.get_coc_filters('Days out of stock')

        return self.get_values(request, '105-6 Artemether/ Lumefantrine 100/20mg tablet',
                               coc_filters, self.facility_count_aggregator, False, value__gt=7)

    def get_number_of_facilities_submitted_act(self, request):
        coc_filters = self.get_coc_filters('Days out of stock')

        return self.get_values(request, '105-6 Artemether/ Lumefantrine 100/20mg tablet',
                               coc_filters, self.facility_count_aggregator, False)

    def add_to_final(self, data, partial_data, key, group_by_column, create=True):
        for result in partial_data:
            group_column_value = result[group_by_column]

            if group_column_value not in data:
                if not create:
                    continue

                data[group_column_value] = {}

            data[group_column_value][key] = result['value_aggregate']

        return data

    def generate_final(self, callbacks):
        callback_keys = self.request.GET.get('callbacks', None)

        if callback_keys is None:
            callback_keys = callbacks.keys()
        else:
            callback_keys = callback_keys.split(',')

        data = {}
        for key in callback_keys:
            create = True
            if key == "population":
                create=False

            self.add_to_final(data, callbacks[key](self.request), key, self.request.GET['group'], create)

        return data

    def get_coc_filters(self, *names):
        f = None
        for name in names:
            if f is None:
                f = Q(category_option_combo__identifier=self.im.coc(name))
            else:
                f = f | Q(category_option_combo__identifier=self.im.coc(name))
        return f

    def get_values(self, request, data_element, coc_filters, aggregate=None, enable_age_group=True, **extra_filters):
        if coc_filters is not None:
            data_filter = DataValue.objects.filter(data_element__identifier=self.im.de(data_element))\
                .filter(coc_filters)
        else:
            data_filter = DataValue.objects.filter(data_element__identifier=self.im.de(data_element))

        if extra_filters:
            data_filter = data_filter.filter(**extra_filters)

        return self.filter_on_request(request, data_filter, aggregate=aggregate, enable_age_group=enable_age_group)

    def get(self, request):
        self.request = request

        self.callbacks['rdt_positive'] = self.get_rdt_positive
        self.callbacks['rdt_done'] = self.get_rdt_done
        self.callbacks['microscopy_positive'] = self.get_microscopy_positive
        self.callbacks['microscopy_done'] = self.get_microscopy_done
        self.callbacks['inpatient_malaria_deaths'] = self.get_inpatient_malaria_deaths
        self.callbacks['malaria_admissions'] = self.get_malaria_admissions
        self.callbacks['total_inpatient_deaths'] = self.get_total_inpatient_deaths
        self.callbacks['opd_malaria_cases'] = self.get_opd_malaria_cases
        self.callbacks['number_receiving_ipt2'] = self.get_number_receiving_ipt2
        self.callbacks['number_attending_anc1'] = self.get_number_attending_anc1
        self.callbacks['population'] = self.get_population
        self.callbacks['stock_outs_of_sp'] = self.get_number_of_facilities_with_stock_outs_of_sp
        self.callbacks['stock_outs_of_act'] = self.get_number_of_facilities_with_stock_outs_of_act
        self.callbacks['submitted_sp'] = self.get_number_of_facilities_submitted_sp
        self.callbacks['submitted_act'] = self.get_number_of_facilities_submitted_act

        return HttpResponse(json.dumps(self.generate_final(self.callbacks)))