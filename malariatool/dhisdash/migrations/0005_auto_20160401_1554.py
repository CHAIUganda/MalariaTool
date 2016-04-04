# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0004_auto_20160401_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datavalue',
            name='category_option_identifier',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='district_identifier',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='facility_identifier',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='region_identifier',
        ),
        migrations.AddField(
            model_name='datavalue',
            name='category_option_combo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.CategoryOptionCombo', null=True),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='data_element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.DataElement', null=True),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.District', null=True),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.Facility', null=True),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.Region', null=True),
        ),
    ]
