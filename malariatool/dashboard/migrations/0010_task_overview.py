# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20151210_0452'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='overview',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
