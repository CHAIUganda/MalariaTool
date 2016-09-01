# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0008_categoryoptioncombo_data_element'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='datavalue',
            unique_together=set([('facility', 'period', 'data_element', 'category_option_combo')]),
        ),
    ]
