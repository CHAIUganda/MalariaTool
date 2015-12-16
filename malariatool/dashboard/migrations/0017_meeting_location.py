# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20151215_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='location',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
