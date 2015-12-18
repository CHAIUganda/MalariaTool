from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin

from dashboard.forms.document import DocumentForm
from dashboard.models import Document


class FormListView(FormMixin, ListView):
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class DocumentListView(FormListView):
    model = Document
    form_class = DocumentForm


class DocumentCreateView(CreateView):
    model = Document
    fields = ['display_name', 'file', 'description', 'type']
    success_url = reverse_lazy("dashboard:document-list")

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(DocumentCreateView, self).form_valid(form)


class DocumentDetailView(DetailView):
    model = Document
