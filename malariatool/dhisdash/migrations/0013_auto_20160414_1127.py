# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0012_auto_20160414_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasynctracker',
            name='last_downloaded',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='datasynctracker',
            name='last_parsed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
