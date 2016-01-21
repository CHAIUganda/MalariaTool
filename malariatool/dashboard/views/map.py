from django.views.generic import TemplateView

from dashboard.models import IP, Task


class MapView(TemplateView):
    template_name = "dashboard/maps.html"

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['ips'] = IP.objects.all()
        context['tasks'] = Task.objects.all()
        return context
