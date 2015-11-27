from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from dashboard.models import Document


class DocumentListView(ListView):
    model = Document


class DocumentCreateView(CreateView):
    model = Document
    fields = ['display_name', 'file', 'description']
    success_url = reverse_lazy("dashboard:document-list")

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(DocumentCreateView, self).form_valid(form)
