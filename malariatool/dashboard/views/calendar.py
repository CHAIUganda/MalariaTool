from django.views.generic import FormView

from dashboard.forms.meeting import MeetingForm
from dashboard.models import Meeting


class CalendarView(FormView):
    form_class = MeetingForm
    template_name = "dashboard/calendar.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['meetings'] = Meeting.objects.all()
        return context
