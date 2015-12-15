# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20151215_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='date',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='time',
        ),
        migrations.AddField(
            model_name='meeting',
            name='end',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='start',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='attendees',
        ),
        migrations.AddField(
            model_name='meeting',
            name='attendees',
            field=models.ManyToManyField(related_name='attendees', to=settings.AUTH_USER_MODEL),
        ),
    ]
