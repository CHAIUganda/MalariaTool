from django import forms
from django.forms import ModelForm

from dashboard.models import Meeting, IP


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'start', 'end', 'location']


class AddAttendee(forms.Form):
    ip = forms.ModelMultipleChoiceField(queryset=IP.objects.all(), help_text="Start typing out ip")
    extra_attendees = forms.CharField(widget=forms.Textarea,help_text="Enter attendee's email addresses comma separted")
