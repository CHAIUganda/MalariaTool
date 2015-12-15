from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from dashboard.models import Meeting


class MeetingCreateView(CreateView):
    success_url = reverse_lazy("dashboard:admin")
    model = Meeting
    fields = ['title', 'start', 'end', 'attendees']
