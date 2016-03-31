# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datavalue',
            old_name='org_unit_identifier',
            new_name='district_identifier',
        ),
        migrations.AddField(
            model_name='categoryoptioncombo',
            name='age_group',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='age_group',
            field=models.IntegerField(default=0),
        ),
    ]
