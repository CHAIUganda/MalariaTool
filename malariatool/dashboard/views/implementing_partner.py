from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from dashboard.models import IP


class IPListView(ListView):
    model = IP


class IPCreateView(CreateView):
    model = IP
    fields = ['name']
    success_url = reverse_lazy("dashboard:list-ip")
