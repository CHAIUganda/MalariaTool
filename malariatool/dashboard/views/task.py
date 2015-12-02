from django.views.generic import CreateView, ListView

from dashboard.models import Task


class TaskCreateView(CreateView):
    model = Task
    fields = ['start_date', 'end_date','target_acutal_per_quarter', 'target_output_per_quarter', 'affected_districts', 'duration']


class TaskListView(ListView):
    pass
