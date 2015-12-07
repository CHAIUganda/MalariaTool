from django import forms
from django.forms import ModelForm

from dashboard.models import Task, District, IP


class TaskForm(ModelForm):
    affected_districts = forms.ModelMultipleChoiceField(queryset=District.objects.all())
    type = forms.ChoiceField(choices=Task.type_choices)
    ip = forms.ModelChoiceField(queryset=IP.objects.all(), empty_label=None)

    class Meta:
        model = Task
        fields = ['start_date', 'end_date',]
