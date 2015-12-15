# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20151214_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='affected_districts',
        ),
        migrations.AddField(
            model_name='task',
            name='affected_districts',
            field=models.ManyToManyField(related_name='affected_districts', to='dashboard.District'),
        ),
    ]
