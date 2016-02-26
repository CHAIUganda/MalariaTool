from django.core.urlresolvers import reverse
from django.test import TestCase

from dashboard.tests.factories.attendee import AttendeeFactory
from dashboard.tests.factories.meeting import MeetingFactory


class MeetingsView(TestCase):
    def setUp(self):
        self.attendee = AttendeeFactory()
        self.attendee1 = AttendeeFactory(email="test1@malariatool.com")
        self.meeting = MeetingFactory.build(attendees=(self.attendee, self.attendee1))
        self.meeting.save()
        self.meeting_two = MeetingFactory(title="Stand up")

    def test_get(self):
        response = self.client.get(reverse("dashboard:calendar-view"))
        self.assertTemplateUsed(response, 'dashboard/calendar.html')
        self.assertEqual(response.status_code, 200)

    def test_meetings_list_view(self):
        response = self.client.get(reverse("dashboard:meeting-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/meeting_list.html")
        self.assertContains(response, self.meeting.title)
        self.assertContains(response, self.meeting_two.title)

    def test_meetings_remove(self):
        response = self.client.post("/meeting/delete/" + str(self.meeting.id), {}, follow=True)
        self.assertRedirects(response, expected_url=reverse("dashboard:meeting-list"))
        self.assertNotContains(response, self.meeting.title)
        self.assertContains(response, self.meeting_two.title)
