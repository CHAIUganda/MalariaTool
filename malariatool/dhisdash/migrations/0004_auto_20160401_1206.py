# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0003_auto_20160331_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.Region', null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='sub_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.SubCounty', null=True),
        ),
        migrations.AddField(
            model_name='subcounty',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.District', null=True),
        ),
    ]
