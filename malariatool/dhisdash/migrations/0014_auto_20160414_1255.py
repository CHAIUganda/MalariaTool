# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0013_auto_20160414_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='datavalue',
            name='data_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.DataSet', null=True),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='original_period',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datasynctracker',
            name='period',
            field=models.IntegerField(unique=True),
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='data_set_parser',
        ),
        migrations.AlterUniqueTogether(
            name='datavalue',
            unique_together=set([('facility', 'original_period', 'data_element', 'category_option_combo')]),
        ),
    ]
