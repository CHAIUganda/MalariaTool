from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from dashboard.models import IP, User


class IPListView(ListView):
    model = IP


class IPCreateView(CreateView):
    model = IP
    fields = ['name', 'overview', 'objectives', 'areas_of_operations', 'implementation_period']
    success_url = reverse_lazy("dashboard:ip-list")


class IPDetailView(DetailView):
    model = IP

    def get_context_data(self, **kwargs):
        context =  super(IPDetailView, self).get_context_data(**kwargs)
        ip = kwargs.get('object')
        context['users']  = User.objects.filter(ip=ip.id)
        return context

