from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView

from dashboard.forms.upload import UploadForm
from dashboard.models.excel_documents import ExcelDocument


class UploadView(FormView):
    form_class = UploadForm
    template_name = "dashboard/upload_form.html"
    success_url = reverse_lazy("dashboard:home")


class XlsList(ListView):
    model = ExcelDocument
