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

    POSITIVE_UNDER_FIVE = 'PT9vhPUpxc4'
    POSITIVE_OVER_FOUR = 'Li89EZS6Jss'
    DONE_UNDER_FIVE = 'bSUziAZFlqN'
    DONE_OVER_FOUR = 'snPZPBW4ZW0'

    def filter_on_request(self, request, partial_filter):
        start_period = int(request.GET['from_date'])
        end_period = int(request.GET['to_date'])
        region = int(request.GET['region'])
        district = int(request.GET['district'])
        age_group = int(request.GET['age_group'])
        group_by_column = request.GET['group']

        results = partial_filter.filter(period__gte=start_period, period__lte=end_period,
                                        age_group=age_group) \
            .filter(Q(region=region) | Q(district=district)) \
            .values(group_by_column).annotate(Sum('value'))

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

        data = {}
        data = self.add_to_final(data, rdt_positive, 'rdt_positive', request.GET['group'])
        data = self.add_to_final(data, rdt_done, 'rdt_done', request.GET['group'])
        data = self.add_to_final(data, microscopy_positive, 'microscopy_positive', request.GET['group'])
        data = self.add_to_final(data, microscopy_done, 'microscopy_done', request.GET['group'])
        data = self.add_to_final(data, opd_malaria_total, 'opd_malaria_total', request.GET['group'])

        return HttpResponse(json.dumps(data))