from django.views.generic import TemplateView

from dashboard.models import Member, Meeting


class Home(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['members'] = Member.objects.all()
        context['meetings'] = Meeting.objects.all()[:5]
        return context


