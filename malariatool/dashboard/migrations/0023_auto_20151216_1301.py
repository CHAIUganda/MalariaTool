# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20151216_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='attendees',
            field=models.ManyToManyField(related_name='meeting_attendees', to='dashboard.Attendee'),
        ),
    ]
