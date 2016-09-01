# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0017_district_population'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datavalue',
            name='original_period',
            field=models.CharField(max_length=20, db_index=True),
        ),
    ]
