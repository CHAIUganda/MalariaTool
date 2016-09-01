from django.views.generic import TemplateView

from dashboard.models import Member, Meeting


class AboutUs(TemplateView):
    template_name = "about-us.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUs, self).get_context_data(**kwargs)
        context['members'] = Member.objects.all()
        context['meetings'] = Meeting.objects.all()[:5]
        return context


