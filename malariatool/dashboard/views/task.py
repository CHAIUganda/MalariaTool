from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView

from dashboard.models import Task


class TaskCreateView(CreateView):
    model = Task
    success_url = reverse_lazy("dashboard:home")
    fields = ['start_date', 'end_date', 'type', 'affected_districts', 'ip']


class TaskListView(ListView):
    model = Task
