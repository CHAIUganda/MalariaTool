import factory

from dashboard.models.meeting import Attendee


class AttendeeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Attendee

    email = "test@malariatool.com"
    first_name = "John"
    last_name = "Doe"
