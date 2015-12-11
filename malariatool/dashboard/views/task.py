from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, DetailView

from dashboard.forms.task import TaskForm
from dashboard.models import Task
from dashboard.models.tasks import Item


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm

    def form_invalid(self, form):
        return super(TaskCreateView, self).form_invalid(form)

    def form_valid(self, form):
        districts = form.cleaned_data.get("affected_districts")
        ip = form.cleaned_data.get("ip")
        form.instance.ip = ip
        for district in districts:
            form.instance.affected_districts = district
        form.instance.save()
        return super(TaskCreateView, self).form_valid(form)


class TaskListView(ListView):
    model = Task


class TaskItemCreateView(CreateView):
    model = Item
    template_name = "dashboard/additems.html"
    fields = ['description', 'estimated_end_date']

    def get_success_url(self):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        return reverse("dashboard:task-add-items", kwargs={'pk': task.id})

    def get_context_data(self, **kwargs):
        context = super(TaskItemCreateView, self).get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs.get('pk'))
        context['task'] = task
        context['items'] = Item.objects.filter(task=task)
        return context

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        form.instance.task = task
        return super(TaskItemCreateView, self).form_valid(form)


class TaskDetailView(DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs.get('pk'))
        context['task'] = task
        context['sub_tasks'] = Item.objects.filter(task=task)
        return context
