from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from dashboard.models import IP


class IPListView(ListView):
    model = IP


class IPCreateView(CreateView):
    model = IP
    fields = ['name', 'overview', 'objectives', 'areas_of_operations', 'implementation_period']
    success_url = reverse_lazy("dashboard:ip-list")
