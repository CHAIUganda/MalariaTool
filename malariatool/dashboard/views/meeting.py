from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, DeleteView

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
