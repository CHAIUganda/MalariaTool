from django.forms import ModelForm

from dashboard.models import IP


class IPForm(ModelForm):
    class Meta:
        model = IP
        fields = ['name', 'overview', 'objectives', 'areas_of_operations', 'implementation_period']
