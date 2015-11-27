from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from dashboard.models import Document


class DocumentListView(ListView):
    model = Document


class DocumentCreateView(CreateView):
    model = Document
    fields = ['display_name', 'file', 'description']
    success_url = reverse_lazy("dashboard:document-list")

    def form_valid(self, form):
        print form.files.get('file').name.split(".")[1].upper()
        print type (form.files.get('file'))
        print dir(form.files.get('file'))
        form.instance.uploader = self.request.user
        form.instance.type = form.files.get('file').name.split(".")[1].upper()

        return super(DocumentCreateView, self).form_valid(form)


class DocumentDetailView(DetailView):
    model = Document
