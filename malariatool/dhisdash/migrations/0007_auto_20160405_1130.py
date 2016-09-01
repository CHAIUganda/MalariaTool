# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0006_auto_20160405_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoptioncombo',
            name='identifier',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
