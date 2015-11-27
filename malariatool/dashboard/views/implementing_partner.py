from django.views.generic import ListView

from dashboard.models import IP


class IPListView(ListView):
    model = IP