# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0011_auto_20160413_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasynctracker',
            name='last_downloaded',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='datasynctracker',
            name='last_parsed',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
