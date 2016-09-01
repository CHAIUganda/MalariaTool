# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0016_datasynctracker_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='population',
            field=models.IntegerField(default=0),
        ),
    ]
