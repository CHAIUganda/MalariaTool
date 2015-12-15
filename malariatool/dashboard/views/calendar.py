from django.views.generic import TemplateView

from dashboard.models import Meeting


class CalendarView(TemplateView):
    template_name = "dashboard/calendar.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['meetings'] = Meeting.objects.all()
        return context
