from django.views.generic import CreateView, ListView

from dashboard.models import Task


class TaskCreateView(CreateView):
    model = Task
    fields = ['start_date', 'end_date', 'type', 'affected_districts', 'ip']


class TaskListView(ListView):
    model = Task
