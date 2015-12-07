from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView

from dashboard.forms.task import TaskForm
from dashboard.models import Task


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("dashboard:home")


class TaskListView(ListView):
    model = Task
