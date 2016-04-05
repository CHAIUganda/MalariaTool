# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0007_auto_20160405_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryoptioncombo',
            name='data_element',
            field=models.ForeignKey(default=0, to='dhisdash.DataElement'),
            preserve_default=False,
        ),
    ]
