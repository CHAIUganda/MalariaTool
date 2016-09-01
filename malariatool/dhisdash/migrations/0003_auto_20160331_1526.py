# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0002_auto_20160331_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='identifier',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='facility',
            name='identifier',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='region',
            name='identifier',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='subcounty',
            name='identifier',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
