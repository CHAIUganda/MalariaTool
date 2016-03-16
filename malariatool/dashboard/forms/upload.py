from django.forms import ModelForm

from dashboard.models.excel_documents import ExcelDocuments


class UploadForm(ModelForm):
    class Meta:
        model = ExcelDocuments
        fields = ['name', 'files']
