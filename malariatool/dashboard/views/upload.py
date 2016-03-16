from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView

from dashboard.forms.upload import UploadForm


class UploadView(FormView):
    form_class = UploadForm
    template_name = "dashboard/upload_form.html"
    success_url = reverse_lazy("dashboard:home")

