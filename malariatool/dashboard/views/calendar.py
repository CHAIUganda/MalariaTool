from django.views.generic import TemplateView


class CalendarView(TemplateView):
    template_name = "dashboard/calendar.html"
