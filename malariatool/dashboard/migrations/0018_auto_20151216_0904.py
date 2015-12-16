# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_meeting_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='attendees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='location',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
