from django.forms import ModelForm

from dashboard.models.excel_documents import ExcelDocument


class UploadForm(ModelForm):
    class Meta:
        model = ExcelDocument
        fields = ['name', 'files']
