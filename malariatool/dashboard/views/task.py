from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, DetailView, FormView

from dashboard.forms.task import TaskForm, TaskItemForm
from dashboard.models import Task
from dashboard.models.tasks import Item


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse("dashboard:task-add-items", kwargs={'pk': self.object.id})

    def form_valid(self, form):
        districts = form.cleaned_data.get("affected_districts")
        ip = form.cleaned_data.get("ip")
        form.instance.ip = ip
        for district in districts:
            form.instance.affected_districts = district
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


class TaskItemUpdateView(FormView):
    form_class = TaskItemForm
    template_name = "dashboard/update_tasks.html"
    success_url = "/"

    def form_valid(self, form):
        item = Item.objects.get(pk=self.kwargs.get('pk'))
        item.status = form.cleaned_data.get('status')
        item.save()
        return super(TaskItemUpdateView, self).form_valid(form)
