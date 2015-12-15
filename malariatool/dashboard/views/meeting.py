from django.views.generic import CreateView

from dashboard.models import Meeting


class MeetingCreateView(CreateView):
    model = Meeting
    fields = ['title', 'start', 'end','attendees']