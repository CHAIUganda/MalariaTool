from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView

from dashboard.forms.task import TaskForm
from dashboard.models import Task


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("dashboard:home")

    def form_invalid(self, form):
        print "invalid"
        print form
        return super(TaskCreateView, self).form_invalid(form)

    def form_valid(self, form):
        districts = form.cleaned_data.get("affected_districts")
        ip = form.cleaned_data.get("ip")
        print "------------------------------------------"
        print form.cleaned_data
        print ip
        form.instance.ip = ip
        for district in districts:
            form.instance.affected_districts = district
        form.instance.save()
        return super(TaskCreateView, self).form_valid(form)


class TaskListView(ListView):
    model = Task
