# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_remove_meeting_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='first_name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendee',
            name='last_name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
