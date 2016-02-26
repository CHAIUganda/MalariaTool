import datetime

import factory

from dashboard.models import Meeting


class MeetingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Meeting

    title = "Briefing"
    start = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(hours=3)
    location = "Board Room 1"

    @factory.post_generation
    def attendees(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for attendee in extracted:
                self.attendees.add(attendee)
