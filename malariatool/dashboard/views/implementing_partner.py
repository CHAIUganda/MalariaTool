from braces.views import JSONResponseMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView

from dashboard.forms.implementing_partner import IPForm
from dashboard.models import IP, User, Task, District
from dashboard.views.document import FormListView


class IPListView(FormListView):
    model = IP
    form_class = IPForm


class IPCreateView(CreateView):
    model = IP
    fields = ['name', 'overview', 'objectives', 'areas_of_operations', 'implementation_period']
    success_url = reverse_lazy("dashboard:ip-list")


class IPDetailView(DetailView):
    model = IP

    def get_context_data(self, **kwargs):
        context = super(IPDetailView, self).get_context_data(**kwargs)
        ip = kwargs.get('object')
        context['users'] = User.objects.filter(ip=ip.id)
        return context


class IPFilterView(JSONResponseMixin, View):
    json_dumps_kwargs = {u"indent": 2}

    def dispatch(self, request, *args, **kwargs):
        ip = IP.objects.get(id=kwargs.get('pk'))
        districts_ids = Task.objects.filter(ip=ip).values_list('affected_districts', flat=True)
        districts = District.objects.filter(pk__in=districts_ids).values_list('name', flat=True)
        return self.render_json_response(list(districts))


class IPDeleteView(DeleteView):
    model = IP
    success_url = reverse_lazy("dashboard:ip-list")
