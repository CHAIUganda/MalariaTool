from django.views.generic import ListView, DetailView
from dashboard.models import IP


class IPListView(ListView):
    model = IP

class IPDetailView(DetailView):
    model = IP