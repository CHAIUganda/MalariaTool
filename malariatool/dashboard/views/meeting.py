from django.contrib.sites.models import Site, RequestSite
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.template import loader
from django.views.generic import CreateView, FormView, DeleteView, RedirectView

from dashboard.forms.meeting import AddAttendee
from dashboard.models import Meeting
from dashboard.models.meeting import Attendee


class MeetingCreateView(CreateView):
    success_url = reverse_lazy("dashboard:admin")
    model = Meeting
    fields = ['title', 'start', 'end', 'location']

    def get_success_url(self):
        return reverse("dashboard:meeting-add-attendees", kwargs={'pk': self.object.id})


class MeetingAddAttendeesView(FormView):
    form_class = AddAttendee
    template_name = "dashboard/attendee_form.html"

    def get_success_url(self):
        return reverse("dashboard:meeting-add-attendees", kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(MeetingAddAttendeesView, self).get_context_data(**kwargs)
        meeting = Meeting.objects.get(id=self.kwargs.get('pk'))
        context['meeting'] = meeting
        return context

    def form_valid(self, form):
        attendees = []
        ips = form.cleaned_data.get('ip')
        extras = form.cleaned_data.get('extra_attendees')
        extras = extras.split(",")
        attendees.extend(extras)
        for ip in ips:
            attendees.extend(list(ip.ip_user.values_list('email', flat=True)))
        meeting = Meeting.objects.get(id=self.kwargs.get('pk'))
        for attendee in attendees:
            meeting.attendees.add(Attendee.objects.create(email=attendee))
        return super(MeetingAddAttendeesView, self).form_valid(form)


class MeetingAttendeeDeleteView(DeleteView):
    model = Attendee

    def get_success_url(self):
        print self.kwargs.get('meeting_id')
        return reverse("dashboard:meeting-add-attendees", kwargs={'pk': self.kwargs.get('meeting_id')})


class MeetingAttendeesNotifyView(RedirectView):
    permanent = False
    email_template_name = 'dashboard/meeting_email.txt'
    email_subject_template_name = 'dashboard/meeting_email_subject.txt'

    def get_redirect_url(self, *args, **kwargs):
        return reverse("dashboard:meeting-add-attendees", kwargs={'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        meeting = Meeting.objects.get(id=self.kwargs.get('pk'))
        attendees = list(meeting.attendees.all().values_list('email', flat=True))
        for attendee in attendees:
            self.send_notification(attendee, meeting)
        return super(MeetingAttendeesNotifyView, self).get(request, *args, **kwargs)

    def get_site(self):
        if Site._meta.installed:
            return Site.objects.get_current()
        else:
            return RequestSite(self.request)

    def send_notification(self, attendee, meeting):
        context = {
            'site': self.get_site(),
            'meeting': meeting,
            'username': attendee,
            'secure': self.request.is_secure(),
        }
        body = loader.render_to_string(self.email_template_name,
                                       context).strip()
        subject = loader.render_to_string(self.email_subject_template_name,
                                          context).strip()
        send_mail(subject=subject, message=body, from_email="National Malaria Control<me@remosamuel.com>",
                  recipient_list=[attendee], fail_silently=True)
