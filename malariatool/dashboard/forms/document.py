from django.forms import ModelForm

from dashboard.models import Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['display_name', 'file', 'description', 'type']
