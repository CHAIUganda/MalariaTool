# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0009_auto_20160412_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSyncTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.IntegerField()),
                ('last_download', models.DateTimeField(auto_now=True)),
                ('last_parse', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
