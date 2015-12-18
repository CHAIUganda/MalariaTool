from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView, DeleteView

from dashboard.forms.task import TaskForm, TaskItemForm, TaskNoteForm
from dashboard.models import Task
from dashboard.models.tasks import Item, Note
from dashboard.views.document import FormListView


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse("dashboard:task-add-items", kwargs={'pk': self.object.id})

    def form_valid(self, form):
        districts = form.cleaned_data.get("affected_districts")
        ip = form.cleaned_data.get("ip")
        form.instance.ip = ip
        self.object = form.save()
        districts_list = list(districts)
        for district in districts_list:
            self.object.affected_districts.add(district)
        return super(TaskCreateView, self).form_valid(form)


class TaskListView(FormListView):
    model = Task
    form_class = TaskForm


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

    def get_success_url(self):
        item = Item.objects.get(id=self.kwargs.get('pk'))
        task = item.task
        return reverse("dashboard:task-detail", kwargs={'pk': task.id})

    def form_valid(self, form):
        item = Item.objects.get(pk=self.kwargs.get('pk'))
        item.status = form.cleaned_data.get('status')
        item.save()
        return super(TaskItemUpdateView, self).form_valid(form)


class TaskNoteUpdateView(FormView):
    form_class = TaskNoteForm
    template_name = "dashboard/update_notes.html"

    def get_success_url(self):
        item = Item.objects.get(id=self.kwargs.get('pk'))
        return reverse("dashboard:task-detail", kwargs={'pk': item.task.id})

    def form_valid(self, form):
        item = Item.objects.get(id=self.kwargs.get('pk'))
        print item
        print item.id
        form.instance.item = item
        form.instance.save()
        return super(TaskNoteUpdateView, self).form_valid(form)


class TaskItemNotesListView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(TaskItemNotesListView, self).get_context_data(**kwargs)
        item = Item.objects.filter(id=self.kwargs.get('pk'))
        context['notes'] = Note.objects.filter(item=item)
        return context


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['start_date', 'end_date', 'type', 'overview']
    success_url = reverse_lazy("dashboard:task-list")


class TaskDeleteView(DeleteView):
    template_name = "dashboard/task_list.html"
    model = Task
    success_url = reverse_lazy('dashboard:task-list')
