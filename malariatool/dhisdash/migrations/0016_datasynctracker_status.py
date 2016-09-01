# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0015_auto_20160414_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasynctracker',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
